#!/usr/bin/env python3
"""
Quick test to verify the prompt rendering fix.
"""

from src.agent import OllamaProvider, AndroidWorldAgent
from src.prompts import render_prompt

def test_prompt_rendering():
    """Test that prompts are rendered correctly."""
    
    print("=== Testing Prompt Rendering Fix ===\n")
    
    # Test case
    goal = "Uninstall the Slack app"
    observation = {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]}
    ground_truth = "CLICK(\"Apps\")"
    
    print(f"Goal: {goal}")
    print(f"Observation: {observation}")
    print(f"Ground Truth: {ground_truth}")
    
    try:
        # Test with enhanced prompt
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        agent = AndroidWorldAgent(provider, prompt_template="enhanced")
        
        # Test single step
        step = agent.step(goal, observation, ground_truth)
        
        print(f"\nResults:")
        print(f"  Predicted: {step.predicted_action}")
        print(f"  Ground Truth: {step.ground_truth_action}")
        print(f"  Correct: {step.is_correct}")
        
        if step.is_correct:
            print("✅ Fix successful! Agent is working correctly.")
        else:
            print("❌ Still having issues. Let's debug further.")
            print(f"  Raw prediction: {step.predicted_action}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_simple_prompt():
    """Test with simple prompt to compare."""
    
    print("\n=== Testing Simple Prompt ===\n")
    
    goal = "Uninstall the Slack app"
    observation = {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]}
    ground_truth = "CLICK(\"Apps\")"
    
    try:
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        agent = AndroidWorldAgent(provider, prompt_template="simple")
        
        step = agent.step(goal, observation, ground_truth)
        
        print(f"Simple Prompt Results:")
        print(f"  Predicted: {step.predicted_action}")
        print(f"  Ground Truth: {step.ground_truth_action}")
        print(f"  Correct: {step.is_correct}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_prompt_rendering()
    test_simple_prompt() 