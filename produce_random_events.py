import json
import time
import random
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError, NoBrokersAvailable, NodeNotReadyError

KAFKA_BROKER = "kafka:29092"
TOPIC = "my-realtime-topic"

# Retry logic for Kafka admin connection
def ensure_topic():
    for attempt in range(10):
        try:
            admin = KafkaAdminClient(bootstrap_servers=KAFKA_BROKER)
            topic = NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)
            try:
                admin.create_topics([topic])
                print(f"✅ Created topic '{TOPIC}'")
            except TopicAlreadyExistsError:
                print(f"ℹ️ Topic '{TOPIC}' already exists")
            finally:
                admin.close()
            return
        except (NoBrokersAvailable, NodeNotReadyError) as e:
            print(f"Kafka broker not ready ({type(e).__name__}), retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Kafka broker not available after multiple retries")

def random_event():
    return {
        "userId": str(random.randint(1, 1000)),
        "latencyMs": int(random.uniform(0, 100)),
        "eventTime": str(int(time.time() * 1000))
    }

def main():
    ensure_topic()
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print(f"🚀 Publishing events to '{TOPIC}' every second...")
    while True:
        event = random_event()
        future = producer.send(TOPIC, value=event)
        try:
            record_metadata = future.get(timeout=10)
            print(f"Sent: {event} (partition={record_metadata.partition}, offset={record_metadata.offset})")
            producer.flush()
        except Exception as e:
            print(f"❌ Failed to send event: {e}")
        time.sleep(1)

if __name__ == "__main__":
    main()
