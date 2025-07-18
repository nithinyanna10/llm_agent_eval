#!/usr/bin/env python3
"""
Create the results folder structure for organizing evaluation outputs.
"""

import os
from datetime import datetime

def create_results_structure():
    """Create the results folder structure."""
    
    # Base results directory
    base_dir = "results"
    
    # Create main directories
    directories = [
        "reports",           # Markdown and text reports
        "visualizations",    # Charts and plots
        "data",             # JSON data files
        "reflections",      # Self-reflection outputs
        "logs",             # Execution logs
        "comparisons"       # Agent comparison results
    ]
    
    # Create directories
    for dir_name in directories:
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    
    # Create timestamped subdirectories for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_dir, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    
    # Create subdirectories in the run directory
    for dir_name in directories:
        dir_path = os.path.join(run_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    
    # Create a README for the results structure
    readme_content = f"""# Evaluation Results

This directory contains evaluation results from Android World agent testing.

## Directory Structure

- `reports/` - Markdown and text reports
- `visualizations/` - Charts and plots
- `data/` - JSON data files
- `reflections/` - Self-reflection outputs
- `logs/` - Execution logs
- `comparisons/` - Agent comparison results

## Current Run

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Run ID: {timestamp}

## Files

- `evaluation_report.md` - Main evaluation report
- `metrics.json` - Detailed metrics data
- `visualizations/` - Performance charts
- `reflections.json` - Self-reflection data
"""
    
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created: {readme_path}")
    print(f"\n🎯 Results structure ready! Use run_{timestamp} for current evaluation.")

if __name__ == "__main__":
    create_results_structure() 