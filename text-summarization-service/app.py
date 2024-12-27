import time
import json
import uuid
from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError, NoBrokersAvailable
from threading import Thread
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC_REQUEST = 'summarization-requests'
KAFKA_TOPIC_RESPONSE = 'summarization-responses'

# Store summarization request status in memory
summarization_status = {}

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
                group_id="summarization-group",
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
            summary = response.get("summary")
            error = response.get("error")

            if request_id in summarization_status:
                if error:
                    summarization_status[request_id] = {"status": "Failed", "result": error}
                else:
                    summarization_status[request_id] = {"status": "Completed", "result": summary}
        except Exception as e:
            print(f"Error processing message: {str(e)}")

# Start Kafka consumer in a separate thread
thread = Thread(target=listen_to_kafka, daemon=True)
thread.start()

# Define request body model
class SummarizationRequest(BaseModel):
    text: str
    style: str  # Style is now a required field

@app.route("/summarize", methods=["POST"])
def summarize():
    # Generate a unique ID for the request
    request_id = str(uuid.uuid4())
    summarization_status[request_id] = {"status": "In Progress", "result": None}

    # Get input text and style from request
    try:
        # Validate the incoming JSON payload using Pydantic model
        data = request.json
        if not data:
            raise ValueError("Invalid JSON payload")

        summarization_request = SummarizationRequest(**data)
        text = summarization_request.text
        style = summarization_request.style
    except (ValidationError, ValueError) as e:
        summarization_status[request_id]["status"] = "Failed"
        return jsonify({"error": f"Invalid request data: {str(e)}"}), 400

    try:
        # Prepare message to be sent to Kafka for processing
        message = {
            "request_id": request_id,
            "text": text,
            "style": style  # Include the style in the Kafka message
        }

        producer.send(KAFKA_TOPIC_REQUEST, message)
        producer.flush()

        return jsonify({
            "task_id": request_id,
            "status": "Request sent to Kafka"
        }), 202

    except Exception as e:
        summarization_status[request_id]["status"] = "Failed"
        return jsonify({"error": str(e)}), 500

@app.route("/summarize/status/<task_id>", methods=["GET"])
def get_status(task_id):
    if task_id not in summarization_status:
        return jsonify({"error": "Task not found"}), 404

    status_data = summarization_status[task_id]
    return jsonify({
        "task_id": task_id,
        "status": status_data["status"],
        "result": status_data["result"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
