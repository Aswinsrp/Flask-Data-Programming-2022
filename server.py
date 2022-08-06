from flask import Flask, Response, Request
from pymongo import MongoClient
from bson.objectid import ObjectId
from schema.covidData_schema import covidData_serializer, covidDatas_serializer
import json

app = Flask(__name__)

conn = MongoClient("mongodb+srv://admin:iW70CzDypD5z8Kr5@api.uq5l2w9.mongodb.net/Covid_Data?retryWrites=true&w=majority")
db = conn['Covid_Data']
collection_name = db["Cases"]

@app.route("/", methods=["GET"])
def home():
    return "x"

@app.route("/health", methods=["GET"])
def getHealth():
    return "Application running"

@app.route("/getCovidData",methods=["GET"])
def getCovidData():
    try:
        data = covidDatas_serializer(db.Cases.find())
        return Response(
            response= json.dumps(data),status=500,mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"msg":"Failed to retrive Data"}),status=500,mimetype="application/json"
        )

if __name__ == "__main__":
    app.run(debug=True)