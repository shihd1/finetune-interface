from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
uri = "mongodb+srv://testuser:testuser@cluster0.fnhj60p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# database = client["celanese"]
# collection = database["Project 0"]
# result = collection.insert_one({ "<field name>" : "<value>" })
# print(result.acknowledged)