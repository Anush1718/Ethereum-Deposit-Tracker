# ETH Deposit Tracker
A Python-based Ethereum deposit tracking tool with alerting via Telegram and error handling. 

## Description
This ETH Deposit Tracker monitors transactions made to the Beacon Deposit Contract (`0x00000000219ab540356cBB839Cbe05303d7705Fa`) and logs details such as block number, timestamp, sender address (public key), transaction fee, and value. The tracker also sends notifications via Telegram and logs errors. The code is built using Python and the Alchemy API for blockchain interaction.

## Features
- Monitors the Beacon Deposit Contract for new deposits
- Logs transaction details including block number, timestamp, fee, and sender address
- Sends real-time alerts to Telegram when a new deposit is detected
- Comprehensive logging for errors and significant events
- Modular design with separate files for logger, Telegram integration, and deposit tracking

## Install Dependencies
python -m venv venv
source venv/bin/activate   # For Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

## Configure Environment Variables
ALCHEMY_API_URL='https://eth-mainnet.g.alchemy.com/v2/KcnHJtjN3ExcNbHihVE23599zO8sPTRG'
TELEGRAM_BOT_TOKEN='7226518298:AAEk2jphfg9xPoSx21PWdmlblqnTmbrBul4'
TELEGRAM_CHAT_ID='1442553983'



####  **File Structure**
Outline the structure of your project:

```markdown
## Project File Structure

plaintext
eth-deposit-tracker/
├── src/
│   ├── tracker.py          # Main logic for deposit tracking
│   ├── logger.py           # Logger setup
│   ├── getchatid.py        # Retrieves Telegram chat ID
│   ├── notifications.py    # Sends Telegram alerts
├── deposits.json           # Stored deposit data
├── .env                    # Environment variables (not in Git)
├── README.md               # Documentation
├── requirements.txt        # Python dependencies


  **Code Overview**
Explain each file's purpose in the project:

markdown
## Code Overview

- **tracker.py**: The main script responsible for fetching Ethereum transactions, processing deposit data, and triggering Telegram notifications.
- **logger.py**: Initializes the logger to track significant events and errors.
- **getchatid.py**: A helper script to get the chat ID of the Telegram bot for message notifications.
- **notifications.py**: Contains logic to send alerts to the Telegram chat when a new deposit is detected.

## Schema of Deposit Data
The deposit information is saved in `deposits.json` in the following format:

```json
{
  "blockNumber": 1234567,
  "blockTimestamp": 1618317040,
  "fee": 0.0021,
  "hash": "0x123abc...",
  "pubkey": "0x987xyz...",
  "amount": 32.0
}

## Logging and Error Handling
Explain the logging and error-handling mechanisms:
markdown
## Logging and Error Handling
The application uses Python’s `logging` module for error handling and logging significant events. All logs are stored in a log file for future reference.

- **Error Handling**: Ensures that any issues with API requests or invalid responses are logged.
- **Logging**: Logs important events like successful deposits and errors that occur during deposit tracking.


## Alerts and Notifications
This project integrates with Telegram to send real-time alerts when a new deposit is detected. The `notifications.py` file handles the communication with Telegram using the bot's API.
