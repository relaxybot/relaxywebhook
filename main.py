from flask import Flask, Response, request
from pymongo import MongoClient

app = Flask(__name__)
app.run()

client = MongoClient("mongodb+srv://relaxybot:tecnica54321@cluster0.sxu9qiv.mongodb.net/?retryWrites=true&w=majority")

try:
    client = MongoClient(uri, connectTimeoutMS=30000, socketTimeoutMS=None)
    print("Connection successful")
except:
    print("Unsuccessful")
    
db = client.get_database('chatbot_to_db')

@app.route('/webhook', methods = ['POST','GET'])
def webhook():
    req = request.get_json(force = True)
    query = req['queryResult']['queryText']
    result = req ['queryResult']['fulfillmentText']
    data = {"query": query,
            "result": result
    }

    records = db['messages']
    records.insert_one(data)
    print("data go inserted into db")

    return Response(status=200)

if __name__ == "__main__":
    app.run()
