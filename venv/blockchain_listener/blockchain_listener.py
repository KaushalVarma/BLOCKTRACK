# blockchain_listener.py
from web3 import Web3
from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

# Connect to an Ethereum node (Cloudflare free endpoint)
w3 = Web3(Web3.HTTPProvider('https://cloudflare-eth.com'))

def listen_for_transactions():
    print("Starting transaction listener...")

    # Keep track of the last processed block
    last_block = w3.eth.block_number

    while True:
        current_block = w3.eth.block_number
        if current_block > last_block:
            print(f"Processing block {current_block}")
            
            # Fetch block transactions
            block = w3.eth.get_block(current_block, full_transactions=True)

            # Get all tracked addresses from MongoDB
            tracked_addresses = db.tracked_addresses.find()

            for tx in block.transactions:
                # Debug: Print each transaction being processed
                print(f"Checking transaction {tx['hash'].hex()}")

                # Check if the transaction involves a tracked address
                for address_data in tracked_addresses:
                    address = address_data['address']
                    if tx['from'] == address or tx['to'] == address:
                        print(f"New transaction detected for {address}: {tx['hash'].hex()}")

                        # Store transaction details in MongoDB
                        db.transactions.insert_one({
                            'hash': tx['hash'].hex(),
                            'from': tx['from'],
                            'to': tx['to'],
                            'value': tx['value'],
                            'blockNumber': tx['blockNumber']
                        })

            # Update the last processed block
            last_block = current_block

        # Sleep for a while before checking again
        time.sleep(10)

if __name__ == "__main__":
    listen_for_transactions()
