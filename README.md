# Pinot + Kafka + Superset Demo

This project demonstrates a local setup of Apache Pinot, Kafka, Zookeeper, a Python Kafka producer, and Apache Superset using Docker Compose. It includes scripts for uploading Pinot schemas/configs and producing/consuming Kafka events.

---

## Prerequisites
- Docker & Docker Compose
- Python 3.12 (for running scripts locally, optional)

---

## Quick Start

### 1. Start All Services
```sh
docker compose up -d
```
This will launch Zookeeper, Kafka, Pinot (controller, broker, server, minion), a Python producer, and Superset.

### 2. Upload Pinot Schema & Table Config
```sh
docker compose exec -it producer python upload_pinot_schema.py
```
This uploads the schema and table config to the Pinot controller.

### 3. Produce Events to Kafka
- The `producer` service will automatically start and produce random events to Kafka topic `my-realtime-topic`.
- To run the producer manually:
  ```sh
  docker compose run --rm producer python produce_random_events.py
  ```

### 4. Consume Events from Kafka (for debugging)
- From your Mac:
  ```sh
  python consume_kafka_events.py
  ```
- Or from inside the Kafka container:
  ```sh
  docker compose exec kafka kafka-console-consumer --bootstrap-server kafka:29092 --topic my-realtime-topic --from-beginning
  ```

### 5. Access Pinot UI
- [http://localhost:9000](http://localhost:9000)

### 6. Access Superset UI
- [http://localhost:8088](http://localhost:8088)
- Default admin: `admin` / `admin`

---

## Caveats & Tips

- **Kafka Broker Address:**
  - From containers, use `kafka:29092`.
  - From your Mac, use `localhost:9092`.
- **Kafka Data Reset:**
  - To completely reset Kafka/Zookeeper (delete all topics/messages):
    ```sh
    docker compose down
    docker volume prune  # WARNING: removes all unused Docker volumes
    # Or manually delete any data directories if you use bind mounts
    ```
- **Schema Matching:**
  - The producer must send events matching the Pinot schema exactly:
    ```json
    {
      "userId": "string",
      "latencyMs": int,
      "eventTime": "string (milliseconds since epoch)"
    }
    ```
- **No Data in Pinot?**
  - Check that the producer is using the correct broker address.
  - Check that the schema and table config are uploaded.
  - Check Pinot UI for ingestion errors.
  - Use the Python consumer or Kafka console consumer to verify messages are in Kafka.
- **Topic Offsets Increase, But No Messages?**
  - Make sure you are consuming from the correct broker and topic.
  - Try using a new consumer group or `auto_offset_reset='earliest'`.

---

## File Overview
- `compose.yaml` — Docker Compose setup for all services
- `produce_random_events.py` — Python script to produce random events to Kafka
- `consume_kafka_events.py` — Python script to consume and print Kafka events
- `upload_pinot_schema.py` — Script to upload Pinot schema and table config
- `schemas/` — Pinot schema and table config JSON files
- `requirements.txt` — Python dependencies for producer/consumer scripts
- `Dockerfile.superset` — Custom Dockerfile for Superset with Pinot connector

---

## Troubleshooting
- If you change the schema or table config, re-upload them and restart Pinot services.
- If you want to reset all data, stop all containers and prune Docker volumes.
- If you see connection errors, check that all services are running and healthy with `docker compose ps`.

---

## License
MIT
