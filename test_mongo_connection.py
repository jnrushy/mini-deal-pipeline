from pymongo import MongoClient
import os
from dotenv import load_dotenv

def test_mongo_connection():
    try:
        load_dotenv()
        client = MongoClient(os.getenv('MONGO_URI'))
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        print("✅ Successfully connected to MongoDB!")
        
        # Test creating and accessing our database
        db = client[os.getenv('MONGO_DB')]
        collection = db['test_collection']
        
        # Insert a test document
        test_doc = {"test": "connection"}
        collection.insert_one(test_doc)
        print("✅ Successfully inserted test document!")
        
        # Clean up
        collection.delete_one(test_doc)
        print("✅ Cleaned up test document!")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure MongoDB is installed and running")
        print("2. Check if the MongoDB service is running: brew services list | grep mongodb")
        print("3. Verify your .env file has the correct MONGO_URI")
        print("4. Try connecting to MongoDB Compass with the same URI")

if __name__ == "__main__":
    test_mongo_connection() 