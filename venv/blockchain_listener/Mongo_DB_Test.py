from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.blocktrack_db

# Insert a test document
result = db.test.insert_one({"message": "MongoDB is connected!"})
print(f"Test document inserted with ID: {result.inserted_id}")

