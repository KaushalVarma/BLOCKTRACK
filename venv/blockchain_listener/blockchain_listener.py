from web3 import Web3
from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

# Index the address field to make lookups faster
db.tracked_addresses.create_index('address', unique=True)

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

            # Debugging: Check if transactions exist in the block
            if not block.transactions:
                print(f"No transactions found in block {current_block}")
            else:
                print(f"Found {len(block.transactions)} transactions in block {current_block}")
            
            # Fetch block transactions
            block = w3.eth.get_block(current_block, full_transactions=True)

            # Get all tracked addresses from MongoDB in a set for fast lookup
            tracked_addresses = set([doc['address'].lower() for doc in db.tracked_addresses.find()])

            # Iterate over all transactions in the block
            for tx in block.transactions:  # 'tx' is defined here
                tx_from = tx['from'].lower() if tx['from'] else None
                tx_to = tx['to'].lower() if tx['to'] else None

                # Check if the transaction involves a tracked address
                if (tx_from and tx_from in tracked_addresses) or (tx_to and tx_to in tracked_addresses):
                    print(f"New transaction detected for {tx_from} or {tx_to}: {tx['hash'].hex()}")
                    
                    # Insert transaction into MongoDB
                    db.transactions.insert_one({
                        'hash': tx['hash'].hex(),
                        'from': tx['from'],
                        'to': tx['to'],
                        'value': tx['value'],
                        'blockNumber': tx['blockNumber']
                    })
                    print("Transaction successfully inserted into MongoDB")

            # Update the last processed block
            last_block = current_block

        # Sleep for a while before checking again
        time.sleep(10)

if __name__ == "__main__":
    listen_for_transactions()
