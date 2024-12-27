import time
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError
from transformers import pipeline

# Set up logging configuration
logging.basicConfig(level=logging.INFO)  # Change to DEBUG for more verbosity
logger = logging.getLogger(__name__)

KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC_REQUEST = 'translation-requests-en2ar'
KAFKA_TOPIC_RESPONSE = 'translation-responses-en2ar'

# Initialize the Hugging Face translation pipeline
translator = pipeline("translation_en_to_ar", model="Helsinki-NLP/opus-mt-en-ar")

# Function to create and return Kafka consumer with retry
def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC_REQUEST,
                bootstrap_servers=KAFKA_BROKER,
                group_id="translation-group",  # Ensure unique group ID
                auto_offset_reset="earliest",  # Start reading from the earliest offset
                enable_auto_commit=False,  # Disable auto commit
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

# Consumer loop to process translation requests
for message in consumer:
    logger.info(f"Received message: {message.value}")  # Log the received message
    if not message.value:
        logger.warning(f"Received empty message: {message}")
        continue  # Skip empty messages

    request = message.value
    request_id = request.get("request_id")
    text = request.get("text")

    if not request_id or not text:
        logger.warning(f"Invalid message received: {request}")
        continue  # Skip invalid messages

    try:
        # Perform translation
        result = translator(text)
        translated_text = result[0]["translation_text"]
        
        # Send the translation response
        response = {
            "request_id": request_id,
            "translated_text": translated_text,
            "status": "Completed"  # Status indicating translation success
        }
        for _ in range(3):  # Retry 3 times
            try:
                producer.send(KAFKA_TOPIC_RESPONSE, response)
                producer.flush()
                logger.info(f"Sent translation response for {request_id}")
                break
            except KafkaError as e:
                logger.error(f"Failed to send message to Kafka: {e}")
                time.sleep(1)  # Wait before retrying
        
        # Manually commit the offset after processing the message
        consumer.commit()
    except Exception as e:
        # Send error message in case of failure
        error_response = {
            "request_id": request_id,
            "error": f"Translation failed: {str(e)}",
            "status": "Failed"  # Status indicating failure
        }
        for _ in range(3):  # Retry 3 times
            try:
                producer.send(KAFKA_TOPIC_RESPONSE, error_response)
                producer.flush()
                logger.info(f"Sent error response for {request_id}")
                break
            except KafkaError as e:
                logger.error(f"Failed to send error message to Kafka: {e}")
                time.sleep(1)  # Wait before retrying
        
        # Manually commit the offset after processing the message
        consumer.commit()
