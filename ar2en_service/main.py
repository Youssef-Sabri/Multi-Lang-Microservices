import time
import json
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable
from threading import Thread

app = FastAPI()

KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC_REQUEST = 'translation-requests-ar2en'
KAFKA_TOPIC_RESPONSE = 'translation-responses-ar2en'

# Store translation request status in memory
translation_status = {}

# Function to create and return Kafka producer with retry
def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            # Test producer connection
            producer.send(KAFKA_TOPIC_REQUEST, value={"test": "test"})
            producer.flush()
            print("Connected to Kafka!")
            return producer
        except (NoBrokersAvailable, KafkaError) as e:
            print(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Initialize Kafka producer
producer = create_kafka_producer()

# Function to create and return Kafka consumer with retry
def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC_RESPONSE,
                bootstrap_servers=KAFKA_BROKER,
                group_id="translation-group-ar2en",
                value_deserializer=lambda m: json.loads(m.decode("utf-8"))
            )
            print("Connected to Kafka consumer!")
            return consumer
        except (NoBrokersAvailable, KafkaError) as e:
            print(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Initialize Kafka consumer
consumer = create_kafka_consumer()

# Background task to listen to Kafka consumer
def listen_to_kafka():
    for message in consumer:
        try:
            response = message.value
            if not response:
                print(f"Empty message received: {message}")
                continue  # Skip empty messages

            request_id = response.get("request_id")
            translated_text = response.get("translated_text")
            error = response.get("error")

            if request_id in translation_status:
                if error:
                    translation_status[request_id] = {"status": "Failed", "result": error}
                else:
                    translation_status[request_id] = {"status": "Completed", "result": translated_text}
        except Exception as e:
            print(f"Error processing message: {str(e)}")

# Start Kafka consumer in a separate thread
thread = Thread(target=listen_to_kafka, daemon=True)
thread.start()

# Define request body model
class TranslationRequest(BaseModel):
    text: str

# POST endpoint for translating text
@app.post("/translate/ar2en")
def translate(request: TranslationRequest):
    request_id = str(uuid.uuid4())
    translation_status[request_id] = {"status": "In Progress", "result": None}

    message = {
        "request_id": request_id,
        "text": request.text
    }

    try:
        producer.send(KAFKA_TOPIC_REQUEST, message)
        producer.flush()
        return {"id": request_id, "status": "Request sent to Kafka"}
    except Exception as e:
        translation_status[request_id] = {"status": "Failed", "result": None}
        raise HTTPException(status_code=500, detail=f"Error sending to Kafka: {str(e)}")

# GET endpoint for checking translation status
@app.get("/translate/ar2en/status/{id}")
def get_status(id: str):
    if id not in translation_status:
        raise HTTPException(status_code=404, detail="Translation request not found")
    
    status_data = translation_status[id]
    
    return {
        "id": id,
        "status": status_data["status"],
        "result": status_data["result"]
    }
