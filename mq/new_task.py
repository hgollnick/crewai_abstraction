import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World"
channel.basic_publish(exchange='', routing_key='hello', body=message, properties=pika.BasicProperties(delivery_mode = pika.DeliveryMode.Persistent))
print(" [x] Sent {message}")
connection.close()