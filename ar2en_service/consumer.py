import time
import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError
from transformers import pipeline

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

KAFKA_BROKER = 'kafka:9092'
KAFKA_TOPIC_REQUEST = 'translation-requests-ar2en'
KAFKA_TOPIC_RESPONSE = 'translation-responses-ar2en'

# Initialize the Hugging Face translation pipeline for Arabic to English
translator = pipeline("translation_ar_to_en", model="Helsinki-NLP/opus-mt-ar-en")

# Function to create and return Kafka consumer with retry
def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC_REQUEST,
                bootstrap_servers=KAFKA_BROKER,
                group_id="translation-group-ar2en",
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

# Consumer loop to process translation requests
for message in consumer:
    logger.info(f"Received message: {message.value}")
    if not message.value:
        logger.warning(f"Received empty message: {message}")
        continue

    request = message.value
    request_id = request.get("request_id")
    text = request.get("text")

    if not request_id or not text:
        logger.warning(f"Invalid message received: {request}")
        continue

    try:
        # Perform translation
        result = translator(text)
        translated_text = result[0]["translation_text"]
        
        # Send the translation response
        response = {
            "request_id": request_id,
            "translated_text": translated_text,
            "status": "Completed"
        }
        for _ in range(3):
            try:
                producer.send(KAFKA_TOPIC_RESPONSE, response)
                producer.flush()
                logger.info(f"Sent translation response for {request_id}")
                break
            except KafkaError as e:
                logger.error(f"Failed to send message to Kafka: {e}")
                time.sleep(1)
        
        consumer.commit()
    except Exception as e:
        error_response = {
            "request_id": request_id,
            "error": f"Translation failed: {str(e)}",
            "status": "Failed"
        }
        for _ in range(3):
            try:
                producer.send(KAFKA_TOPIC_RESPONSE, error_response)
                producer.flush()
                logger.info(f"Sent error response for {request_id}")
                break
            except KafkaError as e:
                logger.error(f"Failed to send error message to Kafka: {e}")
                time.sleep(1)
        
        consumer.commit()
