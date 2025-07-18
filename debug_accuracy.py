#!/usr/bin/env python3
"""
Debug script to test Ollama response parsing and accuracy calculation.
"""

from src.agent import OllamaProvider, AndroidWorldAgent
from src.prompts import render_prompt

def test_single_prediction():
    """Test a single prediction to debug accuracy issues."""
    
    print("=== Testing Single Prediction ===\n")
    
    # Simple test case
    goal = "Uninstall the Slack app"
    observation = {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]}
    ground_truth = "CLICK(\"Apps\")"
    
    print(f"Goal: {goal}")
    print(f"Observation: {observation}")
    print(f"Ground Truth: {ground_truth}")
    
    try:
        # Initialize provider
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        
        # Test with different prompts
        prompts = {
            "simple": render_prompt(goal, observation, "simple"),
            "enhanced": render_prompt(goal, observation, "enhanced"),
            "cot": render_prompt(goal, observation, "cot")
        }
        
        for prompt_type, prompt in prompts.items():
            print(f"\n--- Testing {prompt_type.upper()} prompt ---")
            print(f"Prompt:\n{prompt[:200]}...")
            
            # Get prediction
            prediction = provider.generate_action(goal, observation, prompt)
            print(f"Raw Response: {prediction}")
            
            # Check accuracy
            is_correct = prediction.strip() == ground_truth.strip()
            print(f"Correct: {is_correct}")
            print(f"Expected: {ground_truth}")
            print(f"Got: {prediction}")
            
            # Test the extraction method
            extracted = provider._extract_action(prediction)
            print(f"Extracted: {extracted}")
            extracted_correct = extracted.strip() == ground_truth.strip()
            print(f"Extracted Correct: {extracted_correct}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_agent_step():
    """Test the agent step function."""
    
    print("\n=== Testing Agent Step ===\n")
    
    try:
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        agent = AndroidWorldAgent(provider, prompt_template="enhanced")
        
        goal = "Uninstall the Slack app"
        observation = {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]}
        ground_truth = "CLICK(\"Apps\")"
        
        print(f"Goal: {goal}")
        print(f"Observation: {observation}")
        print(f"Ground Truth: {ground_truth}")
        
        step = agent.step(goal, observation, ground_truth)
        
        print(f"\nStep Results:")
        print(f"  Predicted: {step.predicted_action}")
        print(f"  Ground Truth: {step.ground_truth_action}")
        print(f"  Is Correct: {step.is_correct}")
        print(f"  Observation: {step.observation}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_episode():
    """Test a complete episode."""
    
    print("\n=== Testing Complete Episode ===\n")
    
    episode_data = {
        "goal": "Uninstall the Slack app",
        "observations": [
            {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]},
            {"app": "Apps", "ui_elements": ["Slack", "Chrome", "Maps"]}
        ],
        "ground_truth_actions": [
            "CLICK(\"Apps\")",
            "CLICK(\"Slack\")"
        ],
        "task_name": "debug_uninstall_slack",
        "params": {}
    }
    
    try:
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        agent = AndroidWorldAgent(provider, prompt_template="enhanced")
        
        episode = agent.load_episode(episode_data)
        result = agent.run_episode(episode)
        
        print(f"Episode Results:")
        print(f"  Task: {result['episode_id']}")
        print(f"  Goal: {result['goal']}")
        print(f"  Total Steps: {result['total_steps']}")
        print(f"  Correct Steps: {result['correct_steps']}")
        print(f"  Step Accuracy: {result['step_accuracy']:.2%}")
        
        print(f"\nDetailed Steps:")
        for i, step in enumerate(result['steps']):
            print(f"  Step {i+1}:")
            print(f"    Observation: {step.observation}")
            print(f"    Predicted: {step.predicted_action}")
            print(f"    Ground Truth: {step.ground_truth_action}")
            print(f"    Correct: {step.is_correct}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_prediction()
    test_agent_step()
    test_episode() 