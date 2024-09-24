from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from flask_cors import CORS  # Import the CORS module
from bson import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

# Route to track an Ethereum address (sent from MetaMask)
@app.route('/track-address', methods=['POST'])
def track_address():
    data = request.json
    address = data.get('address')

    if not address:
        return jsonify({"error": "Address is required"}), 400

    # Upsert the address in MongoDB (insert if not exists, update otherwise)
    db.tracked_addresses.update_one(
        {'address': address},
        {'$set': {'address': address}},
        upsert=True
    )

    return jsonify({"message": f"Tracking started for address {address}"}), 201

# Route to fetch all tracked transactions
@app.route('/get-transactions', methods=['GET'])
def get_transactions():
    # Fetch transactions from the MongoDB collection
    transactions = list(db.transactions.find())

    # Convert MongoDB ObjectId to string for JSON serialization
    for tx in transactions:
        tx['_id'] = str(tx['_id'])

    return jsonify(transactions), 200

# Route to fetch tracked addresses (optional, for debugging/tracking purposes)
@app.route('/get-tracked-addresses', methods=['GET'])
def get_tracked_addresses():
    addresses = list(db.tracked_addresses.find())

    # Convert MongoDB ObjectId to string
    for address in addresses:
        address['_id'] = str(address['_id'])

    return jsonify(addresses), 200

# Route to fetch the latest transactions (supports polling)
@app.route('/get-latest-transactions', methods=['GET'])
def get_latest_transactions():
    transactions = list(db.transactions.find())
    
    # Convert MongoDB ObjectId to string
    for tx in transactions:
        tx['_id'] = str(tx['_id'])
    
    return jsonify(transactions)

# Route to render the dashboard HTML
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
