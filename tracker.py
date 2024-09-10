import requests
import json
import logging
from logger import setup_logger
from notifications import send_telegram_alert

# Initialize logger
setup_logger()

# Replace with your Alchemy API URL
alchemy_api_url = 'https://eth-mainnet.g.alchemy.com/v2/KcnHJtjN3ExcNbHihVE23599zO8sPTRG'

# Beacon Deposit Contract address
deposit_contract_address = '0x00000000219ab540356cBB839Cbe05303d7705Fa'

# Function to fetch block timestamp with error handling
def fetch_block_timestamp(block_number):
    try:
        block_number_hex = hex(block_number)
        alchemy_url = f"{alchemy_api_url}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBlockByNumber",
            "params": [block_number_hex, True]
        }
        response = requests.post(alchemy_url, headers=headers, json=data)
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and data['result']:
                return int(data['result']['timestamp'], 16)
        else:
            logging.error(f"Failed to fetch block timestamp for block {block_number}: {response.text}")
            send_telegram_alert(f"Error fetching block timestamp for block {block_number}")
            return None
    except Exception as e:
        logging.error(f"Exception in fetch_block_timestamp for block {block_number}: {str(e)}")
        send_telegram_alert(f"Exception in fetching block timestamp: {str(e)}")
        return None

# Function to monitor the deposit contract with error handling
def fetch_contract_deposits(block_number):
    try:
        alchemy_url = f"{alchemy_api_url}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), True]
        }
        response = requests.post(alchemy_url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            block_data = data['result']
            transactions = block_data['transactions']

            found_deposit = False
            for tx in transactions:
                if tx['to'] and tx['to'].lower() == deposit_contract_address.lower():
                    logging.info(f"Transaction to Beacon Contract found: {tx['hash']}")
                    process_deposit_transaction(tx)
                    found_deposit = True

            if not found_deposit:
                logging.info(f"No transaction to contract found in block {block_number}")
        else:
            logging.error(f"Failed to fetch transactions for block {block_number}: {response.text}")
            send_telegram_alert(f"Error fetching transactions for block {block_number}: {response.status_code}")
    except Exception as e:
        logging.error(f"Exception in fetch_contract_deposits for block {block_number}: {str(e)}")
        send_telegram_alert(f"Exception in fetching transactions for block {block_number}: {str(e)}")

# Function to process the deposit transaction
def process_deposit_transaction(transaction):
    try:
        blockNumber = int(transaction['blockNumber'], 16)
        gasUsed = int(transaction['gas'], 16)
        gasPrice = int(transaction['gasPrice'], 16)
        blockTimestamp = fetch_block_timestamp(blockNumber)
        
        if blockTimestamp is None:
            logging.error(f"Failed to retrieve block timestamp for block {blockNumber}")
            return

        deposit_info = {
            "blockNumber": blockNumber,
            "blockTimestamp": blockTimestamp,
            "fee": gasUsed * gasPrice,
            "hash": transaction['hash'],
            "pubkey": transaction['from'],
            "amount": int(transaction['value'], 16) / (10 ** 18)  # Convert from Wei to ETH
        }

        logging.info(f"Deposit Info: {deposit_info}")
        save_deposit(deposit_info)
        send_telegram_alert(f"New deposit: {deposit_info}")
    except Exception as e:
        logging.error(f"Exception in process_deposit_transaction for tx {transaction['hash']}: {str(e)}")
        send_telegram_alert(f"Error processing deposit: {str(e)}")

# Save deposit details to JSON with error handling
def save_deposit(deposit_info):
    try:
        with open('deposits.json', 'r') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(deposit_info)

    try:
        with open('deposits.json', 'w') as file:
            json.dump(existing_data, file, indent=4)
        logging.info(f"Successfully saved deposit: {deposit_info['hash']}")
    except Exception as e:
        logging.error(f"Failed to save deposit data: {str(e)}")
        send_telegram_alert(f"Error saving deposit data: {str(e)}")

if __name__ == "__main__":
    # Example block number to monitor
    latest_block = 20261857  # Replace with the latest block to monitor
    fetch_contract_deposits(latest_block)
