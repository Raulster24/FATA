import threading
import pika
import json
import time
import logging

# RabbitMQ configuration for updates
RABBITMQ_HOST = 'rabbitmq'
UPDATE_QUEUE = 'update_queue'

# Global variable to hold the current threshold
current_threshold = 0.3

def update_threshold(new_value):
    global current_threshold
    current_threshold = new_value
    logging.info(f"Updated global threshold: {current_threshold}")

def start_update_consumer():
    def run():
        retries = 10
        connection = None
        while retries:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
                logging.info("Update Consumer connected to RabbitMQ")
                break
            except Exception as e:
                logging.error(f"Update Consumer failed to connect (attempt {11 - retries}/10): {e}")
                time.sleep(5)
                retries -= 1
        if connection is None:
            logging.error("Update Consumer could not connect to RabbitMQ after multiple attempts.")
            return

        channel = connection.channel()
        channel.queue_declare(queue=UPDATE_QUEUE, durable=True)

        def callback(ch, method, properties, body):
            try:
                data = json.loads(body)
                new_threshold = data.get("new_threshold")
                if new_threshold is not None:
                    update_threshold(new_threshold)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logging.error(f"Error processing update message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=UPDATE_QUEUE, on_message_callback=callback)
        logging.info("Started update consumer thread, waiting for updates...")
        channel.start_consuming()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
