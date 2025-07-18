
# Android World Agent Evaluation Report
Generated: 2025-07-17 22:25:37

## Summary Statistics
- **Total Episodes**: 27
- **Total Steps**: 85
- **Correct Steps**: 51
- **Step Accuracy**: 60.00%
- **Successful Episodes**: 7
- **Episode Success Rate**: 25.93%
- **Average Steps per Episode**: 3.1

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
- **change_wallpaper**: 16.67%
- **share_photo_email**: 20.00%
- **enable_dark_mode**: 50.00%
- **update_software**: 33.33%
- **connect_bluetooth_speaker**: 100.00%
- **block_spam_number**: 33.33%
- **turn_on_airplane_mode**: 50.00%
- **delete_all_alarms**: 0.00%
- **reply_email_bob**: 66.67%
- **change_language_spanish**: 100.00%
- **RecipeAddMultipleRecipesFromImage**: 100.00%
- **RecipeAddMultipleRecipesFromMarkor**: 100.00%
- **RecipeAddMultipleRecipesFromMarkor2**: 60.00%
- **RecipeAddSingleRecipe**: 50.00%
- **RecipeDeleteDuplicateRecipes**: 75.00%
- **RecipeDeleteDuplicateRecipes2**: 75.00%

## App-Specific Performance
- **Settings**: 45.45%
- **Apps**: 0.00%
- **App Info**: 100.00%
- **Home**: 83.33%
- **Camera**: 100.00%
- **Messages**: 100.00%
- **Chat**: 0.00%
- **Network & Internet**: 100.00%
- **Wi-Fi**: 0.00%
- **Clock**: 50.00%
- **Alarm**: 50.00%
- **Add Alarm**: 0.00%
- **Battery**: 0.00%
- **Bluetooth**: 50.00%
- **Chrome**: 100.00%
- **Contacts**: 100.00%
- **Add Contact**: 100.00%
- **Sound**: 100.00%
- **Maps**: 0.00%
- **Wallpaper**: 100.00%
- **Gallery**: 0.00%
- **Downloaded**: 0.00%
- **beach.jpg**: 0.00%
- **Vacation**: 0.00%
- **photo2.jpg**: 100.00%
- **Share**: 50.00%
- **Email**: 50.00%
- **Display**: 100.00%
- **System**: 0.00%
- **Software Update**: 100.00%
- **Pair New Device**: 100.00%
- **JBL Flip**: 100.00%
- **Phone**: 0.00%
- **Spam**: 0.00%
- **1234567890**: 100.00%
- **Bob**: 100.00%
- **Reply**: 0.00%
- **Languages & Input**: 100.00%
- **Languages**: 100.00%
- **Simple Gallery Pro**: 100.00%
- **recipes.jpg**: 100.00%
- **Broccoli**: 83.33%
- **Markor**: 100.00%
- **recipes.txt**: 100.00%
- **Filter**: 100.00%
- **Add Recipe**: 0.00%
- **Recipes**: 100.00%
- **Duplicate1**: 100.00%
- **Duplicate2**: 0.00%

## Error Analysis
**Most Common Error Patterns:**
- **Wrong Element Clicked**: 27 occurrences
- **Wrong Action Type (Click vs Type)**: 4 occurrences
- **Wrong Text Typed**: 2 occurrences
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
