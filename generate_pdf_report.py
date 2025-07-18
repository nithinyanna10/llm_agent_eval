#!/usr/bin/env python3
"""
Generate a styled PDF report from the latest evaluation results, including metrics, tables, and embedded visualizations.
"""

import os
import glob
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.units import inch
from PIL import Image as PILImage
from reportlab.lib.enums import TA_CENTER
from dataclasses import asdict

def find_latest_results_dir():
    base = "results"
    if not os.path.exists(base):
        raise FileNotFoundError("No results directory found.")
    run_dirs = [d for d in os.listdir(base) if d.startswith("run_")]
    if not run_dirs:
        raise FileNotFoundError("No run_* directories found in results.")
    latest = sorted(run_dirs)[-1]
    return os.path.join(base, latest)

def get_next_test_number(c_reports_dir):
    os.makedirs(c_reports_dir, exist_ok=True)
    pdfs = glob.glob(os.path.join(c_reports_dir, "evaluation_test_*.pdf"))
    nums = [int(os.path.basename(f).split("_")[-1].split(".")[0]) for f in pdfs if f.split("_")[-1].split(".")[0].isdigit()]
    return max(nums, default=0) + 1

def add_plain_summary(story, metrics, styles):
    summary_lines = [
        f"Total Episodes: {metrics.get('total_episodes', 0)}",
        f"Total Steps: {metrics.get('total_steps', 0)}",
        f"Correct Steps: {metrics.get('correct_steps', 0)}",
        f"Step Accuracy: {metrics.get('step_accuracy', 0):.2%}",
        f"Successful Episodes: {metrics.get('successful_episodes', 0)}",
        f"Episode Success Rate: {metrics.get('episode_success_rate', 0):.2%}",
        f"Average Steps/Episode: {metrics.get('average_steps_per_episode', 0):.2f}"
    ]
    for line in summary_lines:
        story.append(Paragraph(line, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

def add_visualizations(story, viz_dir, styles):
    import os
    from reportlab.platypus import Image
    from reportlab.lib.units import inch
    if not os.path.exists(viz_dir):
        return
    images = [f for f in os.listdir(viz_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        return
    story.append(Paragraph("Visualizations:", styles['Heading2']))
    for img_file in images:
        img_path = os.path.join(viz_dir, img_file)
        story.append(Image(img_path, width=5.5*inch, height=3.5*inch))
        story.append(Spacer(1, 0.2*inch))

def add_plain_episode_details(story, results_path, styles):
    import json
    from reportlab.platypus import Table, TableStyle, KeepTogether
    from reportlab.lib import colors
    with open(results_path) as f:
        episodes = json.load(f)
    if not isinstance(episodes, list):
        episodes = [episodes]
    for ep in episodes:
        # Build the episode log as a list of Paragraphs
        ep_story = []
        ep_story.append(Paragraph(f"<b>Episode:</b> {ep.get('episode_id', '')}", styles['Normal']))
        ep_story.append(Paragraph(f"<b>Goal:</b> {ep.get('goal', '')}", styles['Normal']))
        correct = 0
        total = len(ep.get('steps', []))
        for i, step in enumerate(ep.get('steps', [])):
            import json as _json
            if isinstance(step, str):
                import re
                obs_match = re.search(r"observation=(\{.*?\})", step)
                pred_match = re.search(r"predicted_action='(.*?)'", step)
                gt_match = re.search(r"ground_truth_action='(.*?)'", step)
                corr_match = re.search(r"is_correct=(True|False)", step)
                obs = _json.loads(obs_match.group(1).replace("'", '"')) if obs_match else {}
                pred = pred_match.group(1) if pred_match else ''
                gt = gt_match.group(1) if gt_match else ''
                is_corr = corr_match.group(1) == 'True' if corr_match else False
            else:
                obs = step.get('observation', {})
                pred = step.get('predicted_action', '')
                gt = step.get('ground_truth_action', '')
                is_corr = step.get('is_correct', False)
            if is_corr:
                correct += 1
            ep_story.append(Paragraph(f"  Step {i+1}: App={obs.get('app', '')}, UI={obs.get('ui_elements', [])}", styles['Normal']))
            ep_story.append(Paragraph(f"    Predicted: {pred}", styles['Normal']))
            ep_story.append(Paragraph(f"    Ground Truth: {gt}", styles['Normal']))
            ep_story.append(Paragraph(f"    Correct: {is_corr}", styles['Normal']))
        incorrect = total - correct
        acc = correct / total if total else 0.0
        ep_story.append(Paragraph(f"Summary: Total Steps: {total}, Correct: {correct}, Incorrect: {incorrect}, Accuracy: {acc:.2%}", styles['Normal']))
        # Wrap the episode log in a bordered Table for visual separation
        table = Table([[ep_story]], colWidths=[6.8*inch])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(Spacer(1, 0.2*inch))
        story.append(KeepTogether(table))
        story.append(Spacer(1, 0.2*inch))

def main():
    # Find latest results
    results_dir = find_latest_results_dir()
    report_path = os.path.join(results_dir, "reports", "evaluation_report.md")
    summary_path = os.path.join(results_dir, "data", "summary_metrics.json")
    metrics_path = os.path.join(results_dir, "data", "metrics.json")
    c_reports_dir = "c_reports"
    test_num = get_next_test_number(c_reports_dir)
    pdf_path = os.path.join(c_reports_dir, f"evaluation_test_{test_num:02d}.pdf")

    # Load summary metrics (fallback to metrics.json if summary_metrics.json doesn't exist)
    import json
    if os.path.exists(summary_path):
        with open(summary_path) as f:
            metrics = json.load(f)
    else:
        with open(metrics_path) as f:
            metrics_list = json.load(f)
            metrics = metrics_list[0] if isinstance(metrics_list, list) and metrics_list else {}
    # Load report text
    with open(report_path) as f:
        report_md = f.read()

    # PDF setup
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(f"Android World Agent Evaluation Report", styles['Title']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Plain summary
    add_plain_summary(story, metrics, styles)

    # Visualizations
    viz_dir = os.path.join(results_dir, "visualizations")
    add_visualizations(story, viz_dir, styles)

    # Per-episode details (plain, boxed)
    add_plain_episode_details(story, metrics_path, styles)

    # Add full markdown report as appendix
    story.append(PageBreak())
    story.append(Paragraph("Full Markdown Report", styles['Heading2']))
    for line in report_md.splitlines():
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))

    # Build PDF
    doc.build(story)
    print(f"✅ PDF report generated: {pdf_path}")

if __name__ == "__main__":
    main() 