from datetime import datetime

import json
from random import randint

from fastapi import status

from faker import Faker

from app.init_producer import KAFKA_PRODUCER

def generate_event(topic, name, _data):
    """
    The function takes in a kafka event object produces the event
    and returns the appropriate status code.

    :params name: (str) event name
    :params _data: (Pydantic.Model or dict) data from event stream

    :return: (int) status code
    """

    _status = status.HTTP_200_OK

    kafka_event = {
        "time_stamp": datetime.utcnow().timestamp(),
        "event": name,
    }

    kafka_event["properties"] = _data.dict() if not isinstance(_data, dict) else _data

    # print("Kafka Event Produced --> ", kafka_event, flush=True)

    KAFKA_PRODUCER.produce(
        topic=topic,
        value=json.dumps(kafka_event),
        key=None,
    )
    return _status

def generate_random_events():
    try:
        fake = Faker()
    
        for _ in range(10):
            generate_event("eventstream", "tenant_created", {
                "id": randint(100000, 999999),
                "name": fake.company(),
                "address": fake.street_address(),
                "city": fake.city(),
                "country": fake.country(),
                "zip_code": fake.postcode(),
                "phone": fake.phone_number(),
                "web_url": fake.domain_name()
            })
    except Exception as e:
        print(e)