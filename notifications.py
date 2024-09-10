import requests

# Replace with your Telegram bot token and chat ID
telegram_bot_token = '7226518298:AAEk2jphfg9xPoSx21PWdmlblqnTmbrBul4'
chat_id = '1442553983'

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send alert: {response.text}")
