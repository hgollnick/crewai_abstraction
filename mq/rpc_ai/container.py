import os
import pika

rpc_queue='rpc_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT")),
            credentials=pika.PlainCredentials(username=os.getenv("RABBITMQ_USER"), password=os.getenv("RABBITMQ_PASSWORD"))
        ))

channel = connection.channel()
channel.queue_declare(queue=rpc_queue)

def on_request(ch, method, properties, body):
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=str("Hello, " + body.decode())
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=rpc_queue, on_message_callback=on_request)

print("RPC Server Awaiting Requests...")
channel.start_consuming()
