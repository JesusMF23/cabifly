from flask import Flask, request, jsonify
from pymongo import MongoClient
from kafka import KafkaProducer
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import uuid

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
app = Flask(__name__)

client = MongoClient(MONGODB_URI)
db = client.cabifly
producer = KafkaProducer(
    bootstrap_servers=f'{os.getenv("DOCKER_HOST_IP")}:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)

@app.route('/users/<user_id>/trips', methods=['GET'])
def get_trips(user_id):
    trips = list(db.trips.find({'user_id': user_id}, {'_id': 0}))
    return jsonify(trips)

@app.route('/users/<user_id>/trips', methods=['POST'])
def create_trip(user_id):
    data = request.json
    trip = {
        'created_at': datetime.utcnow().isoformat(),
        'location': [data['lon'], data['lat']],
        'status': 'waiting',
        'trip_id': str(uuid.uuid4()),
        'user_id': user_id
    }
    db.trips.insert_one(trip)
    
    trip.pop('_id', None)
    print(f"sending message to kafka: {trip}")
    producer.send('cabifly.trips', key=trip['trip_id'].encode('utf-8'), value=trip)
    producer.flush()
    return jsonify({"status": "Trip created", "trip_id": trip['trip_id'], "trip": trip}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
