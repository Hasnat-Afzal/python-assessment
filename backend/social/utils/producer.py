from random import randint
import json

from confluent_kafka import Producer

from faker import Faker

# Kafka broker properties
bootstrap_servers = 'kafka:9092'

# Topic to produce messages to
topic = 'eventstream'

# Callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Kafka Producer configuration
conf = {
    'bootstrap.servers': bootstrap_servers
}

# Create Kafka Producer instance
producer = Producer(conf)

def generate_messages():
    # Produce some messages
    
    fake = Faker()
    
    try:
        for i in range(10):
            message = json.dumps({
                "tenant_id": randint(100000, 999999),
                "tenant_name": fake.company(),
                "address": fake.street_address(),
                "city": fake.city(),
                "country": fake.country(),
                "zip_code": fake.postcode(),
                "phone": fake.phone_number(),
                "web_url": fake.domain_name()
            })
            producer.produce(topic, message.encode('utf-8'), callback=delivery_report)

        # Wait up to 1 second for events. Callbacks will be invoked during
        # this method call if the message is successfully delivered or fails
        # delivery.
        producer.poll(1)

        # Wait until all messages have been delivered
        producer.flush()

    except KeyboardInterrupt:
        # Clean up on Ctrl+C
        producer.flush()

    # finally:
    #     # Clean up resources
    #     producer.close()