from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

# Track Ethereum address (sent from MetaMask)
@app.route('/track-address', methods=['POST'])
def track_address():
    data = request.json
    address = data.get('address')
    
    if not address:
        return jsonify({"error": "Address is required"}), 400
    
    # Save the address to MongoDB
    db.tracked_addresses.insert_one({"address": address})
    
    return jsonify({"message": f"Tracking started for address {address}"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=3000)


# Add this to your app.py
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

@app.route('/get-transactions', methods=['GET'])
def get_transactions():
    transactions = list(db.transactions.find())
    
    # Convert MongoDB ObjectId to string
    for tx in transactions:
        tx['_id'] = str(tx['_id'])
    
    return jsonify(transactions)

@app.route('/track-address', methods=['POST'])
def track_address():
    data = request.get_json()
    address = data.get('address')
    if address:
        db.tracked_addresses.update_one(
            {'address': address},
            {'$set': {'address': address}},
            upsert=True
        )
        return jsonify({'status': 'success', 'message': 'Address tracked'}), 200
    return jsonify({'status': 'error', 'message': 'Address not provided'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=3000)
