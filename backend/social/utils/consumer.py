from confluent_kafka import Consumer, KafkaError

import json

from utils.process_msg import process_msg

# Kafka broker properties
bootstrap_servers = 'kafka:9092'

# Topic to consume messages from
topic = 'eventstream'

# Kafka Consumer configuration
conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'social-group',
    'auto.offset.reset': 'earliest'
}

def start_consumer():
    # Create Kafka Consumer instance
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe([topic])

    try:
        while True:
            # Poll for messages
            message = consumer.poll(1.0)

            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition
                    continue
                else:
                    # Error
                    print(f'Error: {message.error()}', flush=True)
                    break

            decoded_msg = json.loads(message.value().decode("utf-8"))

            # Process the message
            print(f'Received message: {decoded_msg}', flush=True)

            process_msg(decoded_msg)

    except KeyboardInterrupt:
        pass

    finally:
        # Clean up resources
        consumer.close()