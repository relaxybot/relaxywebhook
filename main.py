#Importa Framework Flask
from flask import Flask, Response, Request
#Import interfaccia Python per MongoDB
from pymongo import MongoClient

#Assegniamo nome all'istanza dell'oggetto Flask
app = Flask(__name__)
app.run(debug=True)

#Indichiamo l'URI per l'accesso a MongoDB
client = MongoClient("mongodb+srv://relaxybot:tecnica54321@cluster0.sxu9qiv.mongodb.net/?retryWrites=true&w=majority")

#Eseguiamo un try catch, nel caso non dovessimo riuscirci a connettere a MongoDB
try:
    client = MongoClient("mongodb+srv://relaxybot:tecnica54321@cluster0.sxu9qiv.mongodb.net/?retryWrites=true&w=majority", connectTimeoutMS=30000, socketTimeoutMS=None)
    print("Connection successful")
except:
    print("Unsuccessful")

#Indichiamo a quale database connetterci specificando il nome
db = client.get_database('chatbot_to_db')

#Definiamo il link per il webhook e la relativa funzione
@app.route('/webhook', methods = ['POST','GET'])
def webhook():
    #Prendiamo in esame la richiesta in formato JSON
    req = Request.request.get_json(force = True)
    #Dal file JSON ci interessa il campo queryText di queryResult
    query = req['queryResult']['queryText']
    #E il campo fullfillmentText di queryResult
    result = req ['queryResult']['fulfillmentText']
    #Prendiamo i due campi e li mettiamo all'interno di data
    data = {"query": query,
            "result": result
    }
    print(query,result)
    #Scegliamo il record in cui inserire data
    records = db['messages']
    #Inseriamo data
    records.insert_one(data)
    print("data go inserted into db")

    #Diamo status 200, sarebbe OK in HTTP
    return Response(status=200)

#Run app
if __name__ == "__main__":
    app.run()
