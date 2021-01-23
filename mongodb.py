import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://jason:<password>@docbot.ualur.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
