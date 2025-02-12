import pika
import json
import logging

# RabbitMQ connection parameters (using container name 'rabbitmq')
RABBITMQ_HOST = 'rabbitmq'
ANOMALY_QUEUE = 'anomaly_queue'
CANDIDATE_QUEUE = 'candidate_test_queue'

def publish_anomaly(anomaly_data: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=ANOMALY_QUEUE, durable=True)

        message = json.dumps(anomaly_data)
        channel.basic_publish(
            exchange='',
            routing_key=ANOMALY_QUEUE,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        logging.info(f"Published anomaly to queue: {message}")
        connection.close()
    except Exception as e:
        logging.error(f"Error publishing anomaly: {e}")

def publish_candidate_test(candidate_data: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=CANDIDATE_QUEUE, durable=True)

        message = json.dumps(candidate_data)
        channel.basic_publish(
            exchange='',
            routing_key=CANDIDATE_QUEUE,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # persistent message
            )
        )
        logging.info(f"Published candidate test to queue: {message}")
        connection.close()
    except Exception as e:
        logging.error(f"Error publishing candidate test: {e}")
