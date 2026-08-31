import os

from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC_ORDERS = os.getenv("KAFKA_TOPIC_ORDERS", "orders")
KAFKA_TOPIC_CLICKSTREAM = os.getenv("KAFKA_TOPIC_CLICKSTREAM", "clickstream")
