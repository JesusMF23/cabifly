import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
consumer = KafkaConsumer(
    'cabifly.drones',
    bootstrap_servers=f'{os.getenv("DOCKER_HOST_IP")}:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

client = MongoClient(MONGODB_URI)
db = client.cabifly
collection = db.drones

while True:
    for message in consumer:
        print(f"Received message: {message.value}")

        if 'data' in message.value:
            drone_data = message.value['data']
            
            if 'location' in drone_data and 'coordinates' in drone_data['location']:
                drone_data['location'] = {
                    'type': 'Point',
                    'coordinates': drone_data['location']['coordinates']
                }
                
                collection.insert_one(drone_data)
                print(f"Drone data ingested: {drone_data}")
            else:
                print("Invalid drone data: 'location' or 'coordinates' missing")
        else:
            print("Invalid message: 'data' field missing")
