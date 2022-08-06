from time import time
from flask import Flask, Response, Request
from pymongo import MongoClient
from bson.objectid import ObjectId
from schema.covidData_schema import covidData_serializer, covidDatas_serializer
import json
import schedule
import time
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

conn = MongoClient("mongodb+srv://admin:iW70CzDypD5z8Kr5@api.uq5l2w9.mongodb.net/Covid_Data?retryWrites=true&w=majority")
db = conn['Covid_Data']
collection_name = db["Cases"]

@app.route("/", methods=["GET"])
def home():
    return "Welcome"

@app.route("/health", methods=["GET"])
def getHealth():
    return "Application started successfully"

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

url = "https://covid-19-statistics.p.rapidapi.com/reports"
headers = {
    "X-RapidAPI-Key": "ceba13ce3fmsh54baf7333381a96p1e82f6jsnb4f6c7e0220f",
    "X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com"
}

# provinces = ["California","New York","Texas","Florida","Illinois"]
# yesterday = datetime.now() - timedelta(1)
# currentDate = str(datetime.strftime(yesterday, '%Y-%m-%d'))

# def data_load():
#     for x in provinces:
#         print(x)
#         querystring = {"region_province":x,"iso":"USA","region_name":"US","date":currentDate}
#         r = requests.request("GET", url, headers=headers, params=querystring)
#         if r.status_code == 200:
#             data = r.json()
#             collection_name.insert_one(data)

# schedule.every().day.at("01:40").do(data_load)

while 1:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    app.run(debug=True)