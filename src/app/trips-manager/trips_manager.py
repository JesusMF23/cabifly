import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
DRONES_API_URL = os.getenv('DRONES_API')

consumer = KafkaConsumer(
    'cabifly.trips',
    bootstrap_servers=f'{os.getenv("DOCKER_HOST_IP")}:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

client = MongoClient(MONGODB_URI)
db = client.cabifly

def get_nearest_drone(lat, lon, distance):
    response = requests.get(DRONES_API_URL, params={'lat': lat, 'lon': lon, 'distance': distance})
    if response.status_code == 200:
        drones = response.json()
        if drones:
            return drones[0]
    return None

while True:
    for message in consumer:
        print(f"Received message: {message.value}")
        trip = message.value
        if trip['status'] == 'waiting':
            lat = trip['location'][1]
            lon = trip['location'][0]
            distance = 1000

            nearest_drone = get_nearest_drone(lat, lon, distance)

            if nearest_drone:
                print(f"Drone allocated to trip. {nearest_drone}")
                trip['status'] = 'accepted'
                trip['drone_id'] = nearest_drone['drone_id']
                db.trips.update_one({'trip_id': trip['trip_id']}, {'$set': {'status': 'accepted', 'drone_id': nearest_drone['drone_id']}})
                print(f"Trip updated with assigned drone: {trip}")
            else:
                print(f"No available drones for trip: {trip['trip_id']}")
        else:
            print(f"Trip {trip['trip_id']} is not waiting.")
