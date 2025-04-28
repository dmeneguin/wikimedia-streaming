import json
from requests_sse import EventSource
from validation import validate_data
from kafka import KafkaProducer

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
# Configuration
KAFKA_BROKER = 'kafka:29092'  # Adjust if needed
TOPIC_NAME = 'delta-stream'

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON
)

with EventSource(url) as stream:
    for event in stream:
        if event.type == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                # discard canary events
                if change['meta']['domain'] == 'canary':
                    continue            

                validation = validate_data(change)

                # Example JSON data to send
                data = {'payload': change, 'valid': validation['result']}
                # Send JSON message
                future = producer.send(TOPIC_NAME, value=data)
                result = future.get(timeout=10)  # Block until a single message is sent (or timeout)
                print(f"Message sent! Metadata: {result}")
                producer.flush()
producer.close()