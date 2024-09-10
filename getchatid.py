import requests

# Replace with your Telegram bot token
telegram_bot_token = '7226518298:AAEk2jphfg9xPoSx21PWdmlblqnTmbrBul4'

def get_updates(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)  # Print the raw response
        if data['result']:
            for update in data['result']:
                chat_id = update['message']['chat']['id']
                print(f"Chat ID: {chat_id}")
        else:
            print("No updates found. Double-check if you've sent a message to the bot.")
    else:
        print(f"Failed to get updates: {response.status_code} - {response.text}")

get_updates(telegram_bot_token)
