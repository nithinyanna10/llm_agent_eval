
# Android World Agent Evaluation Report
Generated: 2025-07-17 20:52:28

## Summary Statistics
- **Total Episodes**: 3
- **Total Steps**: 8
- **Correct Steps**: 0
- **Step Accuracy**: 0.00%
- **Successful Episodes**: 0
- **Episode Success Rate**: 0.00%
- **Average Steps per Episode**: 2.7

## Task-Specific Performance
- **uninstall_slack**: 0.00%
- **take_photo**: 0.00%
- **send_message**: 0.00%

## App-Specific Performance
- **Settings**: 0.00%
- **Apps**: 0.00%
- **App Info**: 0.00%
- **Home**: 0.00%
- **Camera**: 0.00%
- **Messages**: 0.00%
- **Chat**: 0.00%

## Error Analysis
**Most Common Error Patterns:**
- **Wrong Action Type (Type vs Click)**: 7 occurrences
- **Wrong Text Typed**: 1 occurrences

## Sample Errors

**Error 1:**
- Episode: uninstall_slack
- Goal: Uninstall the Slack app
- App: Settings
- Predicted: TYPE("search_box", "enhanced")
- Ground Truth: CLICK("Apps")

**Error 2:**
- Episode: uninstall_slack
- Goal: Uninstall the Slack app
- App: Apps
- Predicted: TYPE("search_box", "enhanced")
- Ground Truth: CLICK("Slack")

**Error 3:**
- Episode: uninstall_slack
- Goal: Uninstall the Slack app
- App: App Info
- Predicted: TYPE("search_box", "enhanced")
- Ground Truth: CLICK("Uninstall")
