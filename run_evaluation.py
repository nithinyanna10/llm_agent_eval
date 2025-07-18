#!/usr/bin/env python3
"""
Main script to run Android World agent evaluation with organized results.
"""

import os
import sys
from datetime import datetime

def main():
    """Run the complete evaluation pipeline."""
    
    print("🚀 Android World Agent - Complete Evaluation Pipeline")
    print("=" * 60)
    
    # Step 1: Create results structure
    print("\n📁 Step 1: Creating results structure...")
    try:
        from create_results_structure import create_results_structure
        create_results_structure()
        print("✅ Results structure created successfully!")
    except Exception as e:
        print(f"❌ Error creating results structure: {e}")
        return
    
    # Step 2: Run debug tests first
    print("\n🔍 Step 2: Running debug tests...")
    try:
        from debug_accuracy import test_single_prediction, test_agent_step, test_episode
        test_single_prediction()
        test_agent_step()
        test_episode()
        print("✅ Debug tests completed!")
    except Exception as e:
        print(f"❌ Error in debug tests: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 3: Run comprehensive evaluation
    print("\n📊 Step 3: Running comprehensive evaluation...")
    try:
        from test_enhanced_agent import run_comprehensive_evaluation
        analyzer = run_comprehensive_evaluation()
        
        if analyzer:
            metrics = analyzer.calculate_metrics()
            print(f"\n🎯 Final Results:")
            print(f"  Total Episodes: {metrics.total_episodes}")
            print(f"  Overall Accuracy: {metrics.step_accuracy:.2%}")
            print(f"  Episode Success Rate: {metrics.episode_success_rate:.2%}")
            print(f"  Average Steps per Episode: {metrics.average_steps_per_episode:.1f}")
            
            # Show top error patterns
            if metrics.error_patterns:
                print(f"\n🔍 Top Error Patterns:")
                for pattern, count in sorted(metrics.error_patterns.items(), 
                                           key=lambda x: x[1], reverse=True)[:3]:
                    print(f"  {pattern}: {count} occurrences")
        
        print("✅ Comprehensive evaluation completed!")
        
    except Exception as e:
        print(f"❌ Error in comprehensive evaluation: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 4: Show results summary
    print("\n📋 Step 4: Results Summary")
    print("=" * 40)
    
    # Find the latest results directory
    results_base = "results"
    if os.path.exists(results_base):
        run_dirs = [d for d in os.listdir(results_base) if d.startswith("run_")]
        if run_dirs:
            latest_run = sorted(run_dirs)[-1]
            latest_path = os.path.join(results_base, latest_run)
            
            print(f"📁 Latest Results: {latest_path}")
            
            # List generated files
            for subdir in ["reports", "data", "visualizations", "reflections", "logs"]:
                subdir_path = os.path.join(latest_path, subdir)
                if os.path.exists(subdir_path):
                    files = os.listdir(subdir_path)
                    if files:
                        print(f"  📂 {subdir}/: {len(files)} files")
                        for file in files[:3]:  # Show first 3 files
                            print(f"    - {file}")
                        if len(files) > 3:
                            print(f"    ... and {len(files) - 3} more")
    
    print("\n" + "=" * 60)
    print("🎉 Evaluation pipeline completed!")
    print("\n📚 Next Steps:")
    print("  1. Check the generated reports in results/run_*/reports/")
    print("  2. Review visualizations in results/run_*/visualizations/")
    print("  3. Analyze error patterns in the evaluation report")
    print("  4. Run debug_accuracy.py for detailed debugging if needed")

if __name__ == "__main__":
    main() 