import time
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError
from models.summarizer import Summarizer

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC_REQUEST = 'summarization-requests'
KAFKA_TOPIC_RESPONSE = 'summarization-responses'

# Initialize the summarizer
summarizer = Summarizer()

# Function to create and return Kafka consumer with retry
def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC_REQUEST,
                bootstrap_servers=KAFKA_BROKER,
                group_id="summarization-group",
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                value_deserializer=lambda m: json.loads(m.decode("utf-8"))
            )
            logger.info("Connected to Kafka consumer!")
            return consumer
        except (NoBrokersAvailable, KafkaError) as e:
            logger.error(f"Error connecting to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# Initialize Kafka consumer
consumer = create_kafka_consumer()

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Consumer loop to process summarization requests
for message in consumer:
    logger.info(f"Received message: {message.value}")
    if not message.value:
        logger.warning(f"Received empty message: {message}")
        continue

    request = message.value
    request_id = request.get("request_id")
    text = request.get("text")
    style = request.get("style")

    # Validate the message
    if not request_id or not text or not style:
        logger.warning(f"Invalid message: {request}")
        continue

    try:
        # Perform summarization
        summary = summarizer.summarize(text, style)

        # Send the summarization response
        response = {
            "request_id": request_id,
            "summary": summary,
            "status": "Completed"
        }
        producer.send(KAFKA_TOPIC_RESPONSE, response)
        producer.flush()
        logger.info(f"Sent summarization response for {request_id}")
    except Exception as e:
        # Handle errors
        error_response = {
            "request_id": request_id,
            "error": f"Summarization failed: {str(e)}",
            "status": "Failed"
        }
        producer.send(KAFKA_TOPIC_RESPONSE, error_response)
        producer.flush()
        logger.error(f"Error processing request {request_id}: {e}")

    # Manually commit the offset after processing the message
    consumer.commit()
