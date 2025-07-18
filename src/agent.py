import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
from datetime import datetime

# Optional: import openai and anthropic if you plan to use them
try:
    import openai
except ImportError:
    openai = None
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import ollama
except ImportError:
    ollama = None

@dataclass
class Episode:
    """Represents an Android World episode with goal, observations, and actions."""
    goal: str
    observations: List[Dict[str, Any]]
    ground_truth_actions: List[str]
    task_name: str
    params: Dict[str, Any]

@dataclass
class AgentStep:
    """Represents a single agent step with observation and action."""
    observation: Dict[str, Any]
    predicted_action: str
    ground_truth_action: str
    is_correct: bool

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    @abstractmethod
    def generate_action(self, goal: str, observation: Dict[str, Any], prompt_template: str) -> str:
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI GPT-4 provider."""
    def __init__(self, model: str = "gpt-4-turbo-preview", api_key: Optional[str] = None):
        if openai is None:
            raise ImportError("openai package is not installed.")
        self.model = model
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    def generate_action(self, goal: str, observation: Dict[str, Any], prompt_template: str) -> str:
        prompt = prompt_template.format(
            goal=goal,
            app=observation.get("app", "Unknown"),
            ui_elements=observation.get("ui_elements", [])
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an Android agent that can perform actions on mobile apps."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider."""
    def __init__(self, model: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None):
        if Anthropic is None:
            raise ImportError("anthropic package is not installed.")
        self.model = model
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    def generate_action(self, goal: str, observation: Dict[str, Any], prompt_template: str) -> str:
        prompt = prompt_template.format(
            goal=goal,
            app=observation.get("app", "Unknown"),
            ui_elements=observation.get("ui_elements", [])
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

class OllamaProvider(LLMProvider):
    """Ollama local model provider."""
    def __init__(self, model: str = "gemma3:12b-it-qat", base_url: str = "http://localhost:11434"):
        if ollama is None:
            raise ImportError("ollama package is not installed.")
        self.model = model
        self.base_url = base_url
        # Test connection
        try:
            ollama.list()
        except Exception as e:
            raise ConnectionError(f"Could not connect to Ollama at {base_url}. Make sure Ollama is running.")
    
    def generate_action(self, goal: str, observation: Dict[str, Any], prompt_template: str) -> str:
        # prompt_template is now already formatted, so use it directly
        prompt = prompt_template
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an Android agent. You must respond with EXACTLY one action in this format: CLICK(\"element_name\") or TYPE(\"element_name\", \"text\"). Do not add any explanation or extra text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.0,  # More deterministic
                    "num_predict": 30
                }
            )
            response_text = response['message']['content'].strip()
            
            # Clean up the response to extract just the action
            return self._extract_action(response_text)
            
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return "CLICK(\"Unknown\")"  # Fallback response
    
    def _extract_action(self, response_text: str) -> str:
        """Extract the action from the response text."""
        import re
        
        # Look for CLICK or TYPE patterns
        click_pattern = r'CLICK\s*\(\s*"([^"]+)"\s*\)'
        type_pattern = r'TYPE\s*\(\s*"([^"]+)"\s*,\s*"([^"]*)"\s*\)'
        
        # Try to find CLICK first
        click_match = re.search(click_pattern, response_text, re.IGNORECASE)
        if click_match:
            element = click_match.group(1)
            return f'CLICK("{element}")'
        
        # Try to find TYPE
        type_match = re.search(type_pattern, response_text, re.IGNORECASE)
        if type_match:
            element = type_match.group(1)
            text = type_match.group(2)
            return f'TYPE("{element}", "{text}")'
        
        # If no pattern found, try to extract any quoted text
        quoted_match = re.search(r'"([^"]+)"', response_text)
        if quoted_match:
            element = quoted_match.group(1)
            return f'CLICK("{element}")'
        
        # Last resort - return first available element or unknown
        return "CLICK(\"Unknown\")"

class AndroidWorldAgent:
    """Main agent class for Android World evaluation."""
    def __init__(self, llm_provider: LLMProvider, prompt_template: str = "enhanced", enable_reflection: bool = False):
        self.llm_provider = llm_provider
        self.prompt_template = prompt_template
        self.enable_reflection = enable_reflection
        self.step_history: List[AgentStep] = []
        self.reflection_history: List[Dict[str, Any]] = []
    def load_episode(self, episode_data: Dict[str, Any]) -> Episode:
        return Episode(
            goal=episode_data["goal"],
            observations=episode_data["observations"],
            ground_truth_actions=episode_data["ground_truth_actions"],
            task_name=episode_data.get("task_name", "unknown"),
            params=episode_data.get("params", {})
        )
    def step(self, goal: str, observation: Dict[str, Any], ground_truth_action: str) -> AgentStep:
        # Render the prompt using the appropriate template
        from .prompts import render_prompt
        formatted_prompt = render_prompt(goal, observation, self.prompt_template)
        
        predicted_action = self.llm_provider.generate_action(
            goal=goal,
            observation=observation,
            prompt_template=formatted_prompt
        )
        is_correct = predicted_action.strip() == ground_truth_action.strip()
        step = AgentStep(
            observation=observation,
            predicted_action=predicted_action,
            ground_truth_action=ground_truth_action,
            is_correct=is_correct
        )
        self.step_history.append(step)
        
        # Add self-reflection if enabled
        if self.enable_reflection:
            reflection = self._generate_reflection(goal, observation, step)
            self.reflection_history.append(reflection)
        
        return step
    
    def _generate_reflection(self, goal: str, observation: Dict[str, Any], step: AgentStep) -> Dict[str, Any]:
        """Generate self-reflection on the agent's decision."""
        from .prompts import render_reflection_prompt
        
        reflection_prompt = render_reflection_prompt(
            goal=goal,
            observation=observation,
            action_taken=step.predicted_action,
            ground_truth=step.ground_truth_action,
            was_correct=step.is_correct
        )
        
        try:
            reflection_response = self.llm_provider.generate_action(
                goal=goal,
                observation=observation,
                prompt_template=reflection_prompt
            )
        except Exception as e:
            reflection_response = f"Reflection generation failed: {e}"
        
        return {
            'step_index': len(self.step_history) - 1,
            'reflection': reflection_response,
            'was_correct': step.is_correct,
            'timestamp': datetime.now().isoformat()
        }
    def run_episode(self, episode: Episode) -> Dict[str, Any]:
        self.step_history = []
        correct_steps = 0
        total_steps = len(episode.observations)
        for observation, ground_truth_action in zip(episode.observations, episode.ground_truth_actions):
            step = self.step(episode.goal, observation, ground_truth_action)
            if step.is_correct:
                correct_steps += 1
        return {
            "episode_id": episode.task_name,
            "goal": episode.goal,
            "total_steps": total_steps,
            "correct_steps": correct_steps,
            "step_accuracy": correct_steps / total_steps if total_steps > 0 else 0,
            "steps": self.step_history
        }
    def get_metrics(self) -> Dict[str, float]:
        if not self.step_history:
            return {"step_accuracy": 0.0}
        correct_steps = sum(1 for step in self.step_history if step.is_correct)
        total_steps = len(self.step_history)
        return {
            "step_accuracy": correct_steps / total_steps,
            "total_steps": total_steps,
            "correct_steps": correct_steps
        }

def load_episode_from_json(path: str) -> Episode:
    with open(path, "r") as f:
        data = json.load(f)
    return Episode(
        goal=data["goal"],
        observations=data["observations"],
        ground_truth_actions=data["ground_truth_actions"],
        task_name=data.get("task_name", "unknown"),
        params=data.get("params", {})
    )

DEFAULT_PROMPT_TEMPLATE = (
    "Goal: {goal}\n"
    "Observation:\n"
    "- App: {app}\n"
    "- UI Elements: {ui_elements}\n"
    "What is the next best action? Respond in the format:\n"
    "CLICK(\"<element>\") or TYPE(\"<element>\", \"<text>\")"
)

def render_prompt(goal: str, observation: Dict[str, Any], template: str = DEFAULT_PROMPT_TEMPLATE) -> str:
    return template.format(
        goal=goal,
        app=observation.get("app", "Unknown"),
        ui_elements=observation.get("ui_elements", [])
    ) 