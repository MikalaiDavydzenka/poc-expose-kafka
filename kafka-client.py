#!/usr/bin/env python3

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from kafka import KafkaProducer, KafkaConsumer
import json
import click
import logging
import time

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
# BOOTSTRAP_SERVERS="192.168.2.11:30094,192.168.2.11:30095"
BOOTSTRAP_SERVERS="192.168.2.242:9094"
CLIENT_ID="test"
GROUP_ID="test"
TOPIC_NAME="example_topic"

@click.group()
def cli():
    pass

@cli.command()
def create_topic():
    admin_client = KafkaAdminClient(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        client_id=CLIENT_ID,
    )

    topic_list = []
    topic_list.append(
        NewTopic(
            name=TOPIC_NAME,
            num_partitions=1,
            replication_factor=1,
        )
    )

    try:
        admin_client.create_topics(
            new_topics=topic_list,
            validate_only=False,
        )
    except TopicAlreadyExistsError as e:
        log.info(e.message)

def value_serializer(data):
    return json.dumps(data).encode("utf-8")

def value_deserializer(data):
    return json.loads(data.decode("utf-8"))

@cli.command()
def send_time():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=value_serializer,
    )
    producer.send(
        topic=TOPIC_NAME,
        value={
            "time" : time.asctime(),
        },
    )

@cli.command()
def read():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=value_deserializer,
    )

    for message in consumer:
        message = message.value
        log.info(f"{message}")

if __name__ == "__main__":
    logging.basicConfig(
        # level=logging.DEBUG,
    )
    cli()