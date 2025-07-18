"""
Evaluation metrics and analysis for Android World agent performance.
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter

@dataclass
class EvaluationMetrics:
    """Comprehensive evaluation metrics for agent performance."""
    # Basic metrics
    total_episodes: int
    total_steps: int
    correct_steps: int
    step_accuracy: float
    
    # Episode-level metrics
    successful_episodes: int
    episode_success_rate: float
    average_steps_per_episode: float
    
    # Task-specific metrics
    task_accuracy: Dict[str, float]  # accuracy per task type
    app_accuracy: Dict[str, float]   # accuracy per app
    
    # Error analysis
    common_errors: List[Dict[str, Any]]
    error_patterns: Dict[str, int]
    
    # Timing metrics (if available)
    average_response_time: Optional[float] = None
    total_evaluation_time: Optional[float] = None
    
    # Self-reflection metrics
    reflection_quality_score: Optional[float] = None
    learning_improvement: Optional[float] = None

class EvaluationAnalyzer:
    """Analyzes agent performance and generates comprehensive reports."""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.error_analysis: Dict[str, Any] = {}
        
    def add_episode_result(self, episode_result: Dict[str, Any]):
        """Add a single episode result for analysis."""
        self.results.append(episode_result)
    
    def add_batch_results(self, results: List[Dict[str, Any]]):
        """Add multiple episode results for analysis."""
        self.results.extend(results)
    
    def calculate_metrics(self) -> EvaluationMetrics:
        """Calculate comprehensive evaluation metrics."""
        if not self.results:
            return EvaluationMetrics(
                total_episodes=0, total_steps=0, correct_steps=0, step_accuracy=0.0,
                successful_episodes=0, episode_success_rate=0.0, average_steps_per_episode=0.0,
                task_accuracy={}, app_accuracy={}, common_errors=[], error_patterns={}
            )
        
        # Basic metrics
        total_episodes = len(self.results)
        total_steps = sum(r['total_steps'] for r in self.results)
        correct_steps = sum(r['correct_steps'] for r in self.results)
        step_accuracy = correct_steps / total_steps if total_steps > 0 else 0.0
        
        # Episode-level metrics
        successful_episodes = sum(1 for r in self.results if r['step_accuracy'] == 1.0)
        episode_success_rate = successful_episodes / total_episodes if total_episodes > 0 else 0.0
        average_steps_per_episode = total_steps / total_episodes if total_episodes > 0 else 0.0
        
        # Task-specific metrics
        task_accuracy = self._calculate_task_accuracy()
        app_accuracy = self._calculate_app_accuracy()
        
        # Error analysis
        common_errors, error_patterns = self._analyze_errors()
        
        return EvaluationMetrics(
            total_episodes=total_episodes,
            total_steps=total_steps,
            correct_steps=correct_steps,
            step_accuracy=step_accuracy,
            successful_episodes=successful_episodes,
            episode_success_rate=episode_success_rate,
            average_steps_per_episode=average_steps_per_episode,
            task_accuracy=task_accuracy,
            app_accuracy=app_accuracy,
            common_errors=common_errors,
            error_patterns=error_patterns
        )
    
    def _calculate_task_accuracy(self) -> Dict[str, float]:
        """Calculate accuracy per task type."""
        task_results = defaultdict(list)
        
        for result in self.results:
            task_name = result.get('episode_id', 'unknown')
            task_results[task_name].append(result['step_accuracy'])
        
        return {task: sum(accuracies) / len(accuracies) 
                for task, accuracies in task_results.items()}
    
    def _calculate_app_accuracy(self) -> Dict[str, float]:
        """Calculate accuracy per app."""
        app_results = defaultdict(list)
        
        for result in self.results:
            for step in result.get('steps', []):
                # Handle both dict and AgentStep objects
                if hasattr(step, 'observation'):
                    # AgentStep object
                    app = step.observation.get('app', 'Unknown')
                    app_results[app].append(1 if step.is_correct else 0)
                else:
                    # Dictionary
                    app = step['observation'].get('app', 'Unknown')
                    app_results[app].append(1 if step['is_correct'] else 0)
        
        return {app: sum(accuracies) / len(accuracies) if accuracies else 0.0
                for app, accuracies in app_results.items()}
    
    def _analyze_errors(self) -> tuple[List[Dict[str, Any]], Dict[str, int]]:
        """Analyze common errors and patterns."""
        errors = []
        error_patterns = Counter()
        
        for result in self.results:
            for step in result.get('steps', []):
                # Handle both dict and AgentStep objects
                if hasattr(step, 'is_correct'):
                    # AgentStep object
                    if not step.is_correct:
                        error = {
                            'episode_id': result.get('episode_id', 'unknown'),
                            'goal': result.get('goal', ''),
                            'observation': step.observation,
                            'predicted': step.predicted_action,
                            'ground_truth': step.ground_truth_action,
                            'app': step.observation.get('app', 'Unknown')
                        }
                        errors.append(error)
                        
                        # Analyze error patterns
                        pattern = self._classify_error_pattern(step)
                        error_patterns[pattern] += 1
                else:
                    # Dictionary
                    if not step['is_correct']:
                        error = {
                            'episode_id': result.get('episode_id', 'unknown'),
                            'goal': result.get('goal', ''),
                            'observation': step['observation'],
                            'predicted': step['predicted_action'],
                            'ground_truth': step['ground_truth_action'],
                            'app': step['observation'].get('app', 'Unknown')
                        }
                        errors.append(error)
                        
                        # Analyze error patterns
                        pattern = self._classify_error_pattern(step)
                        error_patterns[pattern] += 1
        
        return errors, dict(error_patterns)
    
    def _classify_error_pattern(self, step: Dict[str, Any]) -> str:
        """Classify the type of error made."""
        # Handle both dict and AgentStep objects
        if hasattr(step, 'predicted_action'):
            # AgentStep object
            predicted = step.predicted_action.lower()
            ground_truth = step.ground_truth_action.lower()
        else:
            # Dictionary
            predicted = step['predicted_action'].lower()
            ground_truth = step['ground_truth_action'].lower()
        
        if 'click' in predicted and 'click' in ground_truth:
            return "Wrong Element Clicked"
        elif 'type' in predicted and 'type' in ground_truth:
            return "Wrong Text Typed"
        elif 'click' in predicted and 'type' in ground_truth:
            return "Wrong Action Type (Click vs Type)"
        elif 'type' in predicted and 'click' in ground_truth:
            return "Wrong Action Type (Type vs Click)"
        else:
            return "Format Error"
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate a comprehensive evaluation report."""
        metrics = self.calculate_metrics()
        
        report = f"""
# Android World Agent Evaluation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics
- **Total Episodes**: {metrics.total_episodes}
- **Total Steps**: {metrics.total_steps}
- **Correct Steps**: {metrics.correct_steps}
- **Step Accuracy**: {metrics.step_accuracy:.2%}
- **Successful Episodes**: {metrics.successful_episodes}
- **Episode Success Rate**: {metrics.episode_success_rate:.2%}
- **Average Steps per Episode**: {metrics.average_steps_per_episode:.1f}

## Task-Specific Performance
"""
        
        for task, accuracy in metrics.task_accuracy.items():
            report += f"- **{task}**: {accuracy:.2%}\n"
        
        report += f"""
## App-Specific Performance
"""
        
        for app, accuracy in metrics.app_accuracy.items():
            report += f"- **{app}**: {accuracy:.2%}\n"
        
        report += f"""
## Error Analysis
**Most Common Error Patterns:**
"""
        
        for pattern, count in sorted(metrics.error_patterns.items(), 
                                   key=lambda x: x[1], reverse=True)[:5]:
            report += f"- **{pattern}**: {count} occurrences\n"
        
        if metrics.common_errors:
            report += f"""
## Sample Errors
"""
            for i, error in enumerate(metrics.common_errors[:3]):
                report += f"""
**Error {i+1}:**
- Episode: {error['episode_id']}
- Goal: {error['goal']}
- App: {error['app']}
- Predicted: {error['predicted']}
- Ground Truth: {error['ground_truth']}
"""
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report
    
    def save_results(self, output_path: str):
        """Save detailed results to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
    
    def create_visualizations(self, output_dir: str = "evaluation_plots"):
        """Create visualization plots for the evaluation results."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        metrics = self.calculate_metrics()
        
        # Create accuracy comparison plot
        plt.figure(figsize=(12, 8))
        
        # Task accuracy
        plt.subplot(2, 2, 1)
        tasks = list(metrics.task_accuracy.keys())
        accuracies = list(metrics.task_accuracy.values())
        plt.bar(tasks, accuracies)
        plt.title('Task-Specific Accuracy')
        plt.ylabel('Accuracy')
        plt.xticks(rotation=45)
        
        # App accuracy
        plt.subplot(2, 2, 2)
        apps = list(metrics.app_accuracy.keys())
        app_accuracies = list(metrics.app_accuracy.values())
        plt.bar(apps, app_accuracies)
        plt.title('App-Specific Accuracy')
        plt.ylabel('Accuracy')
        plt.xticks(rotation=45)
        
        # Error patterns
        plt.subplot(2, 2, 3)
        patterns = list(metrics.error_patterns.keys())
        counts = list(metrics.error_patterns.values())
        plt.pie(counts, labels=patterns, autopct='%1.1f%%')
        plt.title('Error Pattern Distribution')
        
        # Overall metrics
        plt.subplot(2, 2, 4)
        overall_metrics = ['Step Accuracy', 'Episode Success Rate']
        overall_values = [metrics.step_accuracy, metrics.episode_success_rate]
        plt.bar(overall_metrics, overall_values)
        plt.title('Overall Performance')
        plt.ylabel('Rate')
        plt.ylim(0, 1)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/evaluation_summary.png", dpi=300, bbox_inches='tight')
        plt.close()

def compare_agents(agent_results: Dict[str, List[Dict[str, Any]]]) -> pd.DataFrame:
    """Compare performance across different agents or configurations."""
    comparison_data = []
    
    for agent_name, results in agent_results.items():
        analyzer = EvaluationAnalyzer()
        analyzer.add_batch_results(results)
        metrics = analyzer.calculate_metrics()
        
        comparison_data.append({
            'Agent': agent_name,
            'Step Accuracy': metrics.step_accuracy,
            'Episode Success Rate': metrics.episode_success_rate,
            'Total Episodes': metrics.total_episodes,
            'Average Steps per Episode': metrics.average_steps_per_episode
        })
    
    return pd.DataFrame(comparison_data) 