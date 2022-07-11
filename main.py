from urllib import response
from flask import Flask, Response, request
import pymongo
import json

with open('config.json') as file:
    params = json.load(file)['params']

app = Flask(__name__)

client = pymongo.MongoClient(params['client_url'])
db = client[params['db']]

@app.route('/webhook', methods = ['POST','GET'])
def webhook():
    req = request.get_json(force = True)
    query = req['queryResult']['queryText']
    result = req ['queryResult']['fulfillmentText']
    data = {"query": query,
            "result": result
    }

    col = db['chat_data']
    col.insert_one(data)
    print("data go inserted into db")

    return Response(status=200)

if __name__ == "__main__":
    app.run()