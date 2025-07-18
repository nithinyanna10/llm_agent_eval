from typing import Dict, Any, List

# Few-shot examples for better prompting
FEW_SHOT_EXAMPLES = [
    {
        "goal": "Open the camera app",
        "observation": {"app": "Home", "ui_elements": ["Camera", "Messages", "Settings"]},
        "action": "CLICK(\"Camera\")",
        "reasoning": "The goal is to open camera, and Camera is available in the UI elements."
    },
    {
        "goal": "Send a text message to John",
        "observation": {"app": "Messages", "ui_elements": ["New Message", "Search", "John"]},
        "action": "CLICK(\"John\")",
        "reasoning": "The goal is to send a message to John, and John is available in the contacts list."
    },
    {
        "goal": "Uninstall the Slack app",
        "observation": {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]},
        "action": "CLICK(\"Apps\")",
        "reasoning": "To uninstall an app, I need to go to Apps section in Settings first."
    },
    {
        "goal": "Take a screenshot",
        "observation": {"app": "Camera", "ui_elements": ["Capture", "Gallery", "Settings"]},
        "action": "CLICK(\"Capture\")",
        "reasoning": "To take a screenshot, I need to capture the current screen."
    }
]

# Enhanced prompt template with few-shot examples
ENHANCED_PROMPT_TEMPLATE = """You are an Android agent that can perform actions on mobile apps. Your goal is to help users accomplish tasks by interacting with UI elements.

Here are some examples of how to respond:

{examples}

Goal: {goal}
Current Observation:
- App: {app}
- UI Elements: {ui_elements}

Based on the goal and available UI elements, what is the next best action? 

Respond in exactly this format:
CLICK("<element>") or TYPE("<element>", "<text>")

Think step by step:
1. What is the goal?
2. What UI elements are available?
3. Which element should I interact with to progress toward the goal?
4. What type of interaction is needed (click or type)?

Action:"""

# Self-reflection prompt template
SELF_REFLECTION_TEMPLATE = """You are an Android agent that just performed an action. Please reflect on your decision:

Goal: {goal}
Observation: {observation}
Action Taken: {action_taken}
Ground Truth: {ground_truth}
Was Action Correct: {was_correct}

Please analyze your decision:

1. **Understanding**: Did I correctly understand the goal and available options?
2. **Strategy**: Was my approach logical and aligned with the goal?
3. **Execution**: Did I choose the right UI element and action type?
4. **Learning**: What would I do differently next time?

Reflection:"""

# Chain-of-thought prompt template
COT_PROMPT_TEMPLATE = """You are an Android agent that needs to think through problems step by step.

Goal: {goal}
Observation:
- App: {app}
- UI Elements: {ui_elements}

Let me think through this step by step:

1. **Goal Analysis**: What am I trying to accomplish?
2. **Context Understanding**: What app am I in and what options do I have?
3. **Strategy Planning**: What's the logical next step toward my goal?
4. **Action Selection**: Which UI element should I interact with and how?

Based on this reasoning, my action should be:

Action: CLICK("<element>") or TYPE("<element>", "<text>")"""

def format_few_shot_examples() -> str:
    """Format few-shot examples for the prompt."""
    formatted_examples = []
    for example in FEW_SHOT_EXAMPLES:
        formatted_examples.append(
            f"Goal: {example['goal']}\n"
            f"Observation: App: {example['observation']['app']}, UI Elements: {example['observation']['ui_elements']}\n"
            f"Action: {example['action']}\n"
            f"Reasoning: {example['reasoning']}\n"
        )
    return "\n".join(formatted_examples)

def render_prompt(goal: str, observation: Dict[str, Any], template: str = "enhanced") -> str:
    """Render a prompt with the given template type."""
    if template == "enhanced":
        return ENHANCED_PROMPT_TEMPLATE.format(
            examples=format_few_shot_examples(),
            goal=goal,
            app=observation.get("app", "Unknown"),
            ui_elements=observation.get("ui_elements", [])
        )
    elif template == "cot":
        return COT_PROMPT_TEMPLATE.format(
            goal=goal,
            app=observation.get("app", "Unknown"),
            ui_elements=observation.get("ui_elements", [])
        )
    else:
        # Default simple template
        return DEFAULT_PROMPT_TEMPLATE.format(
            goal=goal,
            app=observation.get("app", "Unknown"),
            ui_elements=observation.get("ui_elements", [])
        )

def render_reflection_prompt(goal: str, observation: Dict[str, Any], action_taken: str, 
                           ground_truth: str, was_correct: bool) -> str:
    """Render a self-reflection prompt."""
    return SELF_REFLECTION_TEMPLATE.format(
        goal=goal,
        observation=observation,
        action_taken=action_taken,
        ground_truth=ground_truth,
        was_correct="Yes" if was_correct else "No"
    )

# Keep the original template for backward compatibility
DEFAULT_PROMPT_TEMPLATE = (
    "Goal: {goal}\n"
    "Observation:\n"
    "- App: {app}\n"
    "- UI Elements: {ui_elements}\n"
    "What is the next best action? Respond in the format:\n"
    "CLICK(\"<element>\") or TYPE(\"<element>\", \"<text>\")"
)