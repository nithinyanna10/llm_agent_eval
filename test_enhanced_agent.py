#!/usr/bin/env python3
"""
Enhanced test script demonstrating Phase 3 features:
- Few-shot prompting
- Self-reflection
- Comprehensive evaluation metrics
"""

import json
import time
from src.agent import OllamaProvider, AndroidWorldAgent, Episode
from src.prompts import render_prompt, ENHANCED_PROMPT_TEMPLATE, COT_PROMPT_TEMPLATE
from src.evaluation import EvaluationAnalyzer

def create_test_episodes():
    """Create multiple test episodes for comprehensive evaluation."""
    episodes = [
        # Original 11 episodes...
        {
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
        },
        {
            "goal": "Open the camera and take a photo",
            "observations": [
                {"app": "Home", "ui_elements": ["Camera", "Messages", "Settings"]},
                {"app": "Camera", "ui_elements": ["Capture", "Gallery", "Settings"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Camera\")",
                "CLICK(\"Capture\")"
            ],
            "task_name": "take_photo",
            "params": {}
        },
        {
            "goal": "Send a message to John",
            "observations": [
                {"app": "Messages", "ui_elements": ["New Message", "Search", "John"]},
                {"app": "Chat", "ui_elements": ["Text Input", "Send", "Attach"]},
                {"app": "Chat", "ui_elements": ["Text Input", "Send", "Attach"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"John\")",
                "TYPE(\"Text Input\", \"Hello John!\")",
                "CLICK(\"Send\")"
            ],
            "task_name": "send_message",
            "params": {}
        },
        {
            "goal": "Search for Wi-Fi networks",
            "observations": [
                {"app": "Settings", "ui_elements": ["Network & Internet", "Bluetooth", "Display"]},
                {"app": "Network & Internet", "ui_elements": ["Wi-Fi", "Mobile", "Data Usage"]},
                {"app": "Wi-Fi", "ui_elements": ["Available Networks", "Add Network", "Scan"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Network & Internet\")",
                "CLICK(\"Wi-Fi\")",
                "CLICK(\"Scan\")"
            ],
            "task_name": "search_wifi",
            "params": {}
        },
        {
            "goal": "Set an alarm for 7 AM",
            "observations": [
                {"app": "Home", "ui_elements": ["Clock", "Calendar", "Weather"]},
                {"app": "Clock", "ui_elements": ["Alarm", "Timer", "Stopwatch"]},
                {"app": "Alarm", "ui_elements": ["Add Alarm", "Edit", "Delete"]},
                {"app": "Add Alarm", "ui_elements": ["Time Picker", "Save", "Cancel"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Clock\")",
                "CLICK(\"Alarm\")",
                "CLICK(\"Add Alarm\")",
                "TYPE(\"Time Picker\", \"07:00\")",
                "CLICK(\"Save\")"
            ],
            "task_name": "set_alarm",
            "params": {}
        },
        {
            "goal": "Check battery usage",
            "observations": [
                {"app": "Settings", "ui_elements": ["Battery", "Display", "Sound"]},
                {"app": "Battery", "ui_elements": ["Battery Usage", "Battery Saver", "Adaptive Battery"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Battery\")",
                "CLICK(\"Battery Usage\")"
            ],
            "task_name": "check_battery",
            "params": {}
        },
        {
            "goal": "Turn on Bluetooth",
            "observations": [
                {"app": "Settings", "ui_elements": ["Network & Internet", "Bluetooth", "Display"]},
                {"app": "Bluetooth", "ui_elements": ["On/Off Switch", "Pair New Device", "Saved Devices"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Bluetooth\")",
                "CLICK(\"On/Off Switch\")"
            ],
            "task_name": "turn_on_bluetooth",
            "params": {}
        },
        {
            "goal": "Open Chrome and search for 'weather'",
            "observations": [
                {"app": "Home", "ui_elements": ["Chrome", "Maps", "Camera"]},
                {"app": "Chrome", "ui_elements": ["Search Bar", "Tabs", "Menu"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Chrome\")",
                "TYPE(\"Search Bar\", \"weather\")"
            ],
            "task_name": "search_weather_chrome",
            "params": {}
        },
        {
            "goal": "Add a new contact named Alice",
            "observations": [
                {"app": "Home", "ui_elements": ["Contacts", "Phone", "Messages"]},
                {"app": "Contacts", "ui_elements": ["Add Contact", "Search", "Favorites"]},
                {"app": "Add Contact", "ui_elements": ["Name Field", "Phone Field", "Save"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Contacts\")",
                "CLICK(\"Add Contact\")",
                "TYPE(\"Name Field\", \"Alice\")",
                "CLICK(\"Save\")"
            ],
            "task_name": "add_contact_alice",
            "params": {}
        },
        {
            "goal": "Mute the phone",
            "observations": [
                {"app": "Settings", "ui_elements": ["Sound", "Display", "Notifications"]},
                {"app": "Sound", "ui_elements": ["Volume", "Vibrate", "Mute"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Sound\")",
                "CLICK(\"Mute\")"
            ],
            "task_name": "mute_phone",
            "params": {}
        },
        {
            "goal": "Open Maps and get directions to the airport",
            "observations": [
                {"app": "Home", "ui_elements": ["Maps", "Chrome", "Camera"]},
                {"app": "Maps", "ui_elements": ["Search", "Directions", "Menu"]},
                {"app": "Maps", "ui_elements": ["Airport", "Home", "Work"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Maps\")",
                "CLICK(\"Directions\")",
                "TYPE(\"Search\", \"Airport\")"
            ],
            "task_name": "directions_airport",
            "params": {}
        },
        # 9 new, more challenging episodes:
        {
            "goal": "Change wallpaper to a downloaded image",
            "observations": [
                {"app": "Home", "ui_elements": ["Settings", "Gallery", "Files"]},
                {"app": "Settings", "ui_elements": ["Display", "Wallpaper", "Themes"]},
                {"app": "Wallpaper", "ui_elements": ["Choose Image", "Default", "Gallery"]},
                {"app": "Gallery", "ui_elements": ["Downloaded", "Camera", "Screenshots"]},
                {"app": "Downloaded", "ui_elements": ["beach.jpg", "mountain.jpg", "city.jpg"]},
                {"app": "beach.jpg", "ui_elements": ["Set as Wallpaper", "Share", "Delete"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Settings\")",
                "CLICK(\"Wallpaper\")",
                "CLICK(\"Choose Image\")",
                "CLICK(\"Gallery\")",
                "CLICK(\"Downloaded\")",
                "CLICK(\"beach.jpg\")",
                "CLICK(\"Set as Wallpaper\")"
            ],
            "task_name": "change_wallpaper",
            "params": {}
        },
        {
            "goal": "Share a photo via email",
            "observations": [
                {"app": "Gallery", "ui_elements": ["Camera", "Downloads", "Vacation"]},
                {"app": "Vacation", "ui_elements": ["photo1.jpg", "photo2.jpg", "photo3.jpg"]},
                {"app": "photo2.jpg", "ui_elements": ["Share", "Delete", "Edit"]},
                {"app": "Share", "ui_elements": ["Email", "Messages", "Drive"]},
                {"app": "Email", "ui_elements": ["To Field", "Subject Field", "Send"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Vacation\")",
                "CLICK(\"photo2.jpg\")",
                "CLICK(\"Share\")",
                "CLICK(\"Email\")",
                "TYPE(\"To Field\", \"friend@example.com\")",
                "CLICK(\"Send\")"
            ],
            "task_name": "share_photo_email",
            "params": {}
        },
        {
            "goal": "Enable dark mode",
            "observations": [
                {"app": "Settings", "ui_elements": ["Display", "Sound", "Notifications"]},
                {"app": "Display", "ui_elements": ["Brightness", "Dark Mode", "Font Size"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Display\")",
                "CLICK(\"Dark Mode\")"
            ],
            "task_name": "enable_dark_mode",
            "params": {}
        },
        {
            "goal": "Update the system software",
            "observations": [
                {"app": "Settings", "ui_elements": ["System", "About Phone", "Software Update"]},
                {"app": "System", "ui_elements": ["Software Update", "Reset", "Backup"]},
                {"app": "Software Update", "ui_elements": ["Check for Updates", "Install Now", "Schedule"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"System\")",
                "CLICK(\"Software Update\")",
                "CLICK(\"Check for Updates\")"
            ],
            "task_name": "update_software",
            "params": {}
        },
        {
            "goal": "Connect to a Bluetooth speaker named 'JBL Flip'",
            "observations": [
                {"app": "Settings", "ui_elements": ["Bluetooth", "Wi-Fi", "Display"]},
                {"app": "Bluetooth", "ui_elements": ["On/Off Switch", "Pair New Device", "Saved Devices"]},
                {"app": "Pair New Device", "ui_elements": ["JBL Flip", "Sony WH", "Bose QC"]},
                {"app": "JBL Flip", "ui_elements": ["Connect", "Forget", "Rename"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Bluetooth\")",
                "CLICK(\"Pair New Device\")",
                "CLICK(\"JBL Flip\")",
                "CLICK(\"Connect\")"
            ],
            "task_name": "connect_bluetooth_speaker",
            "params": {}
        },
        {
            "goal": "Block a spam number",
            "observations": [
                {"app": "Phone", "ui_elements": ["Recents", "Contacts", "Spam"]},
                {"app": "Spam", "ui_elements": ["1234567890", "9876543210", "Block"]},
                {"app": "1234567890", "ui_elements": ["Block", "Call", "Message"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Spam\")",
                "CLICK(\"1234567890\")",
                "CLICK(\"Block\")"
            ],
            "task_name": "block_spam_number",
            "params": {}
        },
        {
            "goal": "Turn on airplane mode",
            "observations": [
                {"app": "Settings", "ui_elements": ["Network & Internet", "Connections", "Airplane Mode"]},
                {"app": "Network & Internet", "ui_elements": ["Wi-Fi", "Mobile", "Airplane Mode"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Network & Internet\")",
                "CLICK(\"Airplane Mode\")"
            ],
            "task_name": "turn_on_airplane_mode",
            "params": {}
        },
        {
            "goal": "Delete all alarms",
            "observations": [
                {"app": "Clock", "ui_elements": ["Alarm", "Timer", "Stopwatch"]},
                {"app": "Alarm", "ui_elements": ["Edit", "Delete All", "Add Alarm"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Alarm\")",
                "CLICK(\"Delete All\")"
            ],
            "task_name": "delete_all_alarms",
            "params": {}
        },
        {
            "goal": "Reply to an email from Bob",
            "observations": [
                {"app": "Email", "ui_elements": ["Inbox", "Sent", "Bob"]},
                {"app": "Bob", "ui_elements": ["Reply", "Forward", "Delete"]},
                {"app": "Reply", "ui_elements": ["Text Input", "Send", "Attach"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Bob\")",
                "CLICK(\"Reply\")",
                "TYPE(\"Text Input\", \"Thanks Bob!\")",
                "CLICK(\"Send\")"
            ],
            "task_name": "reply_email_bob",
            "params": {}
        },
        {
            "goal": "Change language to Spanish",
            "observations": [
                {"app": "Settings", "ui_elements": ["System", "Languages & Input", "About Phone"]},
                {"app": "Languages & Input", "ui_elements": ["Languages", "Keyboard", "Spell Checker"]},
                {"app": "Languages", "ui_elements": ["Add Language", "Spanish", "French"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Languages & Input\")",
                "CLICK(\"Languages\")",
                "CLICK(\"Spanish\")"
            ],
            "task_name": "change_language_spanish",
            "params": {}
        },
        # Recipe/Broccoli app tasks (user-provided)
        {
            "goal": "Add the recipes from recipes.jpg in Simple Gallery Pro to the Broccoli recipe app.",
            "observations": [
                {"app": "Simple Gallery Pro", "ui_elements": ["recipes.jpg", "Camera", "Albums"]},
                {"app": "recipes.jpg", "ui_elements": ["Share", "Edit", "Delete"]},
                {"app": "Share", "ui_elements": ["Broccoli", "Email", "Drive"]},
                {"app": "Broccoli", "ui_elements": ["Add Recipe", "Import", "Settings"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"recipes.jpg\")",
                "CLICK(\"Share\")",
                "CLICK(\"Broccoli\")",
                "CLICK(\"Import\")"
            ],
            "task_name": "RecipeAddMultipleRecipesFromImage",
            "params": {"difficulty": "hard", "skills": ["transcription", "screen_reading", "data_entry", "complex_ui_understanding", "parameterized"]}
        },
        {
            "goal": "Add the recipes from recipes.txt in Markor to the Broccoli recipe app.",
            "observations": [
                {"app": "Markor", "ui_elements": ["recipes.txt", "Notes", "Tasks"]},
                {"app": "recipes.txt", "ui_elements": ["Share", "Edit", "Delete"]},
                {"app": "Share", "ui_elements": ["Broccoli", "Email", "Drive"]},
                {"app": "Broccoli", "ui_elements": ["Add Recipe", "Import", "Settings"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"recipes.txt\")",
                "CLICK(\"Share\")",
                "CLICK(\"Broccoli\")",
                "CLICK(\"Import\")"
            ],
            "task_name": "RecipeAddMultipleRecipesFromMarkor",
            "params": {"difficulty": "hard", "skills": ["data_entry", "multi_app", "screen_reading", "memorization", "parameterized"]}
        },
        {
            "goal": "Add the recipes from recipes.txt in Markor that take {prep_time} to prepare into the Broccoli recipe app.",
            "observations": [
                {"app": "Markor", "ui_elements": ["recipes.txt", "Notes", "Tasks"]},
                {"app": "recipes.txt", "ui_elements": ["Filter", "Share", "Edit"]},
                {"app": "Filter", "ui_elements": ["Prep Time", "Ingredient", "Cuisine"]},
                {"app": "Share", "ui_elements": ["Broccoli", "Email", "Drive"]},
                {"app": "Broccoli", "ui_elements": ["Add Recipe", "Import", "Settings"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"recipes.txt\")",
                "CLICK(\"Filter\")",
                "CLICK(\"Prep Time\")",
                "CLICK(\"Share\")",
                "CLICK(\"Broccoli\")",
                "CLICK(\"Import\")"
            ],
            "task_name": "RecipeAddMultipleRecipesFromMarkor2",
            "params": {"difficulty": "hard", "skills": ["parameterized", "screen_reading", "complex_ui_understanding", "repetition", "multi_app", "data_entry", "information_retrieval"]}
        },
        {
            "goal": "Add the following recipes into the Broccoli app: {recipe}",
            "observations": [
                {"app": "Broccoli", "ui_elements": ["Add Recipe", "Import", "Settings"]},
                {"app": "Add Recipe", "ui_elements": ["Recipe Name", "Ingredients", "Save"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Add Recipe\")",
                "TYPE(\"Recipe Name\", \"{recipe}\")",
                "CLICK(\"Save\")"
            ],
            "task_name": "RecipeAddSingleRecipe",
            "params": {"difficulty": "easy", "skills": ["data_entry", "parameterized"]}
        },
        {
            "goal": "Delete all but one of any recipes in the Broccoli app that are exact duplicates, ensuring at least one instance of each unique recipe remains",
            "observations": [
                {"app": "Broccoli", "ui_elements": ["Recipes", "Search", "Delete"]},
                {"app": "Recipes", "ui_elements": ["Duplicate1", "Duplicate2", "Unique"]},
                {"app": "Duplicate1", "ui_elements": ["Delete", "Edit", "Back"]},
                {"app": "Duplicate2", "ui_elements": ["Delete", "Edit", "Back"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Recipes\")",
                "CLICK(\"Duplicate1\")",
                "CLICK(\"Delete\")",
                "CLICK(\"Duplicate2\")",
                "CLICK(\"Delete\")"
            ],
            "task_name": "RecipeDeleteDuplicateRecipes",
            "params": {"difficulty": "easy", "skills": ["search", "data_edit", "screen_reading", "repetition", "parameterized"]}
        },
        {
            "goal": "Delete all but one of any recipes in the Broccoli app that are exact duplicates, ensuring at least one instance of each unique recipe remains (medium)",
            "observations": [
                {"app": "Broccoli", "ui_elements": ["Recipes", "Search", "Delete"]},
                {"app": "Recipes", "ui_elements": ["Duplicate1", "Duplicate2", "Unique"]},
                {"app": "Duplicate1", "ui_elements": ["Delete", "Edit", "Back"]},
                {"app": "Duplicate2", "ui_elements": ["Delete", "Edit", "Back"]}
            ],
            "ground_truth_actions": [
                "CLICK(\"Recipes\")",
                "CLICK(\"Duplicate1\")",
                "CLICK(\"Delete\")",
                "CLICK(\"Duplicate2\")",
                "CLICK(\"Delete\")"
            ],
            "task_name": "RecipeDeleteDuplicateRecipes2",
            "params": {"difficulty": "medium", "skills": ["repetition", "data_edit", "parameterized"]}
        }
    ]
    return episodes

def test_different_prompting_strategies():
    """Test different prompting strategies and compare performance."""
    print("=== Testing Different Prompting Strategies ===\n")
    
    episodes = create_test_episodes()
    strategies = {
        "enhanced": "enhanced",  # Few-shot examples
        "cot": "cot",           # Chain-of-thought
        "simple": "simple"      # Basic prompt
    }
    
    results = {}
    
    for strategy_name, template_type in strategies.items():
        print(f"Testing {strategy_name.upper()} prompting strategy...")
        
        try:
            # Initialize provider and agent
            provider = OllamaProvider(model="gemma3:12b-it-qat")
            agent = AndroidWorldAgent(provider, prompt_template=template_type)
            
            strategy_results = []
            
            for episode_data in episodes:
                episode = agent.load_episode(episode_data)
                result = agent.run_episode(episode)
                strategy_results.append(result)
                
                print(f"  {episode.task_name}: {result['step_accuracy']:.2%} accuracy")
            
            results[strategy_name] = strategy_results
            
        except Exception as e:
            print(f"  Error with {strategy_name}: {e}")
            results[strategy_name] = []
    
    return results

def test_self_reflection():
    """Test self-reflection capabilities."""
    print("\n=== Testing Self-Reflection ===\n")
    
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
        "task_name": "uninstall_slack_reflection",
        "params": {}
    }
    
    try:
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        agent = AndroidWorldAgent(provider, enable_reflection=True)
        
        episode = agent.load_episode(episode_data)
        result = agent.run_episode(episode)
        
        print(f"Episode completed with {result['step_accuracy']:.2%} accuracy")
        print(f"Generated {len(agent.reflection_history)} reflections")
        
        # Show sample reflections
        for i, reflection in enumerate(agent.reflection_history[:2]):
            print(f"\nReflection {i+1}:")
            print(f"  Step: {reflection['step_index']}")
            print(f"  Correct: {reflection['was_correct']}")
            print(f"  Reflection: {reflection['reflection'][:200]}...")
        
        return result
        
    except Exception as e:
        print(f"Error testing reflection: {e}")
        return None

def run_comprehensive_evaluation():
    """Run comprehensive evaluation with all features."""
    print("\n=== Comprehensive Evaluation ===\n")
    
    # Create results structure
    from datetime import datetime
    import os
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"results/run_{timestamp}"
    
    # Create results directories
    os.makedirs(f"{results_dir}/reports", exist_ok=True)
    os.makedirs(f"{results_dir}/data", exist_ok=True)
    os.makedirs(f"{results_dir}/visualizations", exist_ok=True)
    os.makedirs(f"{results_dir}/reflections", exist_ok=True)
    os.makedirs(f"{results_dir}/logs", exist_ok=True)
    
    print(f"📁 Results will be saved to: {results_dir}")
    
    # Initialize evaluation analyzer
    analyzer = EvaluationAnalyzer()
    
    # Test with enhanced prompting
    try:
        provider = OllamaProvider(model="gemma3:12b-it-qat")
        agent = AndroidWorldAgent(provider, prompt_template="enhanced", enable_reflection=True)
        
        episodes = create_test_episodes()
        
        for episode_data in episodes:
            print(f"Running episode: {episode_data['task_name']}")
            episode = agent.load_episode(episode_data)
            result = agent.run_episode(episode)
            analyzer.add_episode_result(result)
            
            print(f"  Accuracy: {result['step_accuracy']:.2%}")
            print(f"  Steps: {result['total_steps']}")
            print(f"  Correct: {result['correct_steps']}")
        
        # Generate comprehensive report
        print("\n=== Evaluation Report ===")
        report = analyzer.generate_report()
        print(report)
        
        # Save results to organized structure
        report_path = f"{results_dir}/reports/evaluation_report.md"
        analyzer.generate_report(report_path)
        print(f"📄 Report saved to: {report_path}")
        
        data_path = f"{results_dir}/data/metrics.json"
        analyzer.save_results(data_path)
        print(f"📊 Data saved to: {data_path}")
        
        # Save summary metrics
        summary_metrics = analyzer.calculate_metrics().__dict__
        summary_path = f"{results_dir}/data/summary_metrics.json"
        with open(summary_path, 'w') as f:
            import json
            json.dump(summary_metrics, f, indent=2)
        print(f"📈 Summary metrics saved to: {summary_path}")
        
        # Save reflections if available
        if hasattr(agent, 'reflection_history') and agent.reflection_history:
            reflection_path = f"{results_dir}/reflections/reflections.json"
            with open(reflection_path, 'w') as f:
                json.dump(agent.reflection_history, f, indent=2, default=str)
            print(f"🤔 Reflections saved to: {reflection_path}")
        
        # Create visualizations (if matplotlib is available)
        try:
            viz_dir = f"{results_dir}/visualizations"
            analyzer.create_visualizations(viz_dir)
            print(f"📈 Visualizations created in: {viz_dir}")
        except ImportError:
            print("Matplotlib not available - skipping visualizations")
        
        # Create summary log
        log_path = f"{results_dir}/logs/execution_log.txt"
        with open(log_path, 'w') as f:
            f.write(f"Android World Agent Evaluation Log\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Model: gemma3:12b-it-qat\n")
            f.write(f"Prompt Template: enhanced\n")
            f.write(f"Reflection Enabled: True\n")
            f.write(f"Total Episodes: {len(episodes)}\n")
            f.write(f"Report: {report_path}\n")
            f.write(f"Data: {data_path}\n")
        
        print(f"📝 Log saved to: {log_path}")
        
        return analyzer
        
    except Exception as e:
        print(f"Error in comprehensive evaluation: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run all tests."""
    print("🚀 Android World Agent - Phase 3 Evaluation")
    print("=" * 50)
    
    # Test different prompting strategies
    strategy_results = test_different_prompting_strategies()
    
    # Test self-reflection
    reflection_result = test_self_reflection()
    
    # Run comprehensive evaluation
    analyzer = run_comprehensive_evaluation()
    
    print("\n" + "=" * 50)
    print("✅ Phase 3 Evaluation Complete!")
    
    if analyzer:
        metrics = analyzer.calculate_metrics()
        print(f"\nFinal Summary:")
        print(f"  Total Episodes: {metrics.total_episodes}")
        print(f"  Overall Accuracy: {metrics.step_accuracy:.2%}")
        print(f"  Episode Success Rate: {metrics.episode_success_rate:.2%}")

if __name__ == "__main__":
    main() 