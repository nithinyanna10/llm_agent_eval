
# Android World Agent Evaluation Report
Generated: 2025-07-17 21:00:15

## Summary Statistics
- **Total Episodes**: 3
- **Total Steps**: 8
- **Correct Steps**: 5
- **Step Accuracy**: 62.50%
- **Successful Episodes**: 1
- **Episode Success Rate**: 33.33%
- **Average Steps per Episode**: 2.7

## Task-Specific Performance
- **uninstall_slack**: 66.67%
- **take_photo**: 100.00%
- **send_message**: 33.33%

## App-Specific Performance
- **Settings**: 100.00%
- **Apps**: 0.00%
- **App Info**: 100.00%
- **Home**: 100.00%
- **Camera**: 100.00%
- **Messages**: 100.00%
- **Chat**: 0.00%

## Error Analysis
**Most Common Error Patterns:**
- **Wrong Element Clicked**: 1 occurrences
- **Wrong Text Typed**: 1 occurrences
- **Wrong Action Type (Type vs Click)**: 1 occurrences

## Sample Errors

**Error 1:**
- Episode: uninstall_slack
- Goal: Uninstall the Slack app
- App: Apps
- Predicted: CLICK("Unknown")
- Ground Truth: CLICK("Slack")

**Error 2:**
- Episode: send_message
- Goal: Send a message to John
- App: Chat
- Predicted: TYPE("Text Input", "Hello John")
- Ground Truth: TYPE("Text Input", "Hello John!")

**Error 3:**
- Episode: send_message
- Goal: Send a message to John
- App: Chat
- Predicted: TYPE("Text Input", "Hello John")
- Ground Truth: CLICK("Send")
