from kafka import KafkaConsumer

KAFKA_BROKER = "localhost:9092"
TOPIC = "my-realtime-topic"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='test-consumer-group',
    value_deserializer=lambda x: x.decode('utf-8', errors='replace')
)

print("Consuming messages from Kafka...")
for message in consumer:
    print(f"Offset: {message.offset}, Value: {message.value}")
