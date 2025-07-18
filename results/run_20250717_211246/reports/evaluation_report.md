
# Android World Agent Evaluation Report
Generated: 2025-07-17 21:14:55

## Summary Statistics
- **Total Episodes**: 11
- **Total Steps**: 29
- **Correct Steps**: 18
- **Step Accuracy**: 62.07%
- **Successful Episodes**: 3
- **Episode Success Rate**: 27.27%
- **Average Steps per Episode**: 2.6

## Task-Specific Performance
- **uninstall_slack**: 66.67%
- **take_photo**: 100.00%
- **send_message**: 33.33%
- **search_wifi**: 66.67%
- **set_alarm**: 75.00%
- **check_battery**: 0.00%
- **turn_on_bluetooth**: 50.00%
- **search_weather_chrome**: 100.00%
- **add_contact_alice**: 100.00%
- **mute_phone**: 50.00%
- **directions_airport**: 33.33%

## App-Specific Performance
- **Settings**: 60.00%
- **Apps**: 0.00%
- **App Info**: 100.00%
- **Home**: 100.00%
- **Camera**: 100.00%
- **Messages**: 100.00%
- **Chat**: 0.00%
- **Network & Internet**: 100.00%
- **Wi-Fi**: 0.00%
- **Clock**: 100.00%
- **Alarm**: 100.00%
- **Add Alarm**: 0.00%
- **Battery**: 0.00%
- **Bluetooth**: 0.00%
- **Chrome**: 100.00%
- **Contacts**: 100.00%
- **Add Contact**: 100.00%
- **Sound**: 100.00%
- **Maps**: 0.00%

## Error Analysis
**Most Common Error Patterns:**
- **Wrong Element Clicked**: 7 occurrences
- **Wrong Action Type (Click vs Type)**: 2 occurrences
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
