# blockchain_listener/ethereum.py
from web3 import Web3
from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

# Connect to Ethereum node (Cloudflare or other provider)
w3 = Web3(Web3.HTTPProvider('https://cloudflare-eth.com'))

def listen_for_transactions():
    print("Starting transaction listener...")
    
    # Get the tracked addresses from MongoDB
    tracked_addresses = db.tracked_addresses.find()
    
    # Dictionary to store filters for each address
    filters = {}
    
    for address in tracked_addresses:
        address_str = address['address']
        # Set up a filter to listen for new transactions involving the address
        tx_filter = w3.eth.filter({'fromBlock': 'latest', 'address': address_str})
        filters[address_str] = tx_filter

    while True:
        for address, tx_filter in filters.items():
            try:
                new_entries = tx_filter.get_new_entries()
                for tx in new_entries:
                    # Process and store transaction details in MongoDB
                    db.transactions.insert_one(tx)
                    print(f"Transaction detected for {address}: {tx}")
            except Exception as e:
                print(f"Error while fetching transactions: {e}")
        
        time.sleep(10)  # Sleep for 10 seconds before checking for new transactions

if __name__ == "__main__":
    listen_for_transactions()
