#!/usr/bin/env python3
"""
Test script for Ollama integration with Android World agent.
"""

import json
from src.agent import OllamaProvider, AndroidWorldAgent, Episode
from src.prompts import DEFAULT_PROMPT_TEMPLATE

def test_ollama_integration():
    """Test Ollama integration with a sample episode."""
    
    # Sample episode data
    sample_episode = {
        "goal": "Uninstall the Slack app",
        "observations": [
            {"app": "Settings", "ui_elements": ["Apps", "Search", "Battery"]},
            {"app": "Apps", "ui_elements": ["Slack", "Chrome", "Maps"]},
            {"app": "App Info", "ui_elements": ["Uninstall", "Force Stop", "Storage"]}
        ],
        "ground_truth_actions": [
            "CLICK(\"Apps\")",
            "CLICK(\"Slack\")", 
            "CLICK(\"Uninstall\")"
        ],
        "task_name": "uninstall_slack",
        "params": {}
    }
    
    try:
        # Initialize Ollama provider with your model
        print("Initializing Ollama provider...")
        ollama_provider = OllamaProvider(model="gemma3:27b-it-qat")
        print(f"✅ Connected to Ollama with model: {ollama_provider.model}")
        
        # Create agent
        agent = AndroidWorldAgent(ollama_provider, DEFAULT_PROMPT_TEMPLATE)
        
        # Load episode
        episode = agent.load_episode(sample_episode)
        print(f"✅ Loaded episode: {episode.task_name}")
        print(f"Goal: {episode.goal}")
        
        # Test single step
        print("\n--- Testing Single Step ---")
        first_observation = episode.observations[0]
        first_ground_truth = episode.ground_truth_actions[0]
        
        print(f"Observation: {first_observation}")
        print(f"Ground truth: {first_ground_truth}")
        
        step = agent.step(episode.goal, first_observation, first_ground_truth)
        print(f"Predicted: {step.predicted_action}")
        print(f"Correct: {step.is_correct}")
        
        # Run full episode
        print("\n--- Running Full Episode ---")
        results = agent.run_episode(episode)
        
        print(f"Episode Results:")
        print(f"  Total steps: {results['total_steps']}")
        print(f"  Correct steps: {results['correct_steps']}")
        print(f"  Accuracy: {results['step_accuracy']:.2%}")
        
        # Show detailed steps
        print("\n--- Detailed Steps ---")
        for i, step in enumerate(results['steps']):
            print(f"Step {i+1}:")
            print(f"  Observation: {step.observation}")
            print(f"  Ground truth: {step.ground_truth_action}")
            print(f"  Predicted: {step.predicted_action}")
            print(f"  Correct: {step.is_correct}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ollama_integration() 