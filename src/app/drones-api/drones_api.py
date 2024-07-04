from flask import Flask, request, jsonify
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
client = pymongo.MongoClient(MONGODB_URI)
db = client.cabifly

db.drones.create_index([("location", pymongo.GEOSPHERE)])

app = Flask(__name__)

@app.route("/drones", methods=["GET"])
def get_drones():
    try:
        lon = request.args.get('lon')
        lat = request.args.get('lat')
        distance = request.args.get('distance')

        if lon is None or lat is None or distance is None:
            return jsonify({"error": "Missing query parameters: lon, lat, and distance are required"}), 400

        lon = float(lon)
        lat = float(lat)
        distance = float(distance)
        
        items = db.drones.find({
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "$maxDistance": distance
                }
            }
        }, {"_id": 0})
        
        drones = []
        for item in items:
            drone = {
                'drone_id': item.get('drone_id'),
                'location': item.get('location')
            }
            drones.append(drone)
        
        return jsonify(drones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
