import pika
import json
import logging
import time

# RabbitMQ configuration
RABBITMQ_HOST = 'rabbitmq'
ANOMALY_QUEUE = 'anomaly_queue'
UPDATE_QUEUE = 'update_queue'
AGGREGATION_INTERVAL = 30  # seconds

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_connection_with_retry(retries=10, delay=5):
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            logging.info("Connected to RabbitMQ")
            return connection
        except Exception as e:
            logging.error(f"Attempt {i+1}/{retries} failed to connect to RabbitMQ: {e}")
            time.sleep(delay)
    raise Exception("Could not connect to RabbitMQ after several retries.")

def aggregate_anomalies():
    connection = create_connection_with_retry()
    channel = connection.channel()
    channel.queue_declare(queue=ANOMALY_QUEUE, durable=True)
    channel.queue_declare(queue=UPDATE_QUEUE, durable=True)

    anomalies = []
    start_time = time.time()

    def callback(ch, method, properties, body):
        nonlocal anomalies
        try:
            anomaly = json.loads(body)
            anomalies.append(anomaly)
            logging.info(f"Received anomaly: {anomaly}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_qos(prefetch_count=10)
    channel.basic_consume(queue=ANOMALY_QUEUE, on_message_callback=callback)
    
    logging.info("Federated Learning Server started, waiting for anomaly messages...")
    
    while True:
        connection.process_data_events(time_limit=AGGREGATION_INTERVAL)
        elapsed = time.time() - start_time

        if anomalies:
            total_time = sum(item['processing_time'] for item in anomalies)
            avg_time = total_time / len(anomalies)
            new_threshold = avg_time
            update_message = {
                "new_threshold": new_threshold,
                "anomaly_count": len(anomalies),
                "aggregation_period": elapsed
            }
            channel.basic_publish(
                exchange='',
                routing_key=UPDATE_QUEUE,
                body=json.dumps(update_message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent message
                )
            )
            logging.info(f"Aggregated {len(anomalies)} anomalies over {elapsed:.2f}s. New threshold: {new_threshold:.3f}")
            anomalies = []
            start_time = time.time()
        else:
            logging.info("No anomalies received during this aggregation period.")

if __name__ == "__main__":
    try:
        aggregate_anomalies()
    except KeyboardInterrupt:
        logging.info("Federated Learning Server stopped.")
