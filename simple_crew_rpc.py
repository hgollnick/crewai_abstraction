import os
import pika
import json
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

GROQ_LLM = ChatGroq(
            api_key="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",
            model="llama3-70b-8192"
        )

agent = Agent(
  role='Senior Researcher',
  goal='Uncover groundbreaking technologies in {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world."
  ),
  llm=GROQ_LLM,
  tools=[],
  allow_delegation=True,
)

task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[],
  agent=agent,
)

crew = Crew(
  agents=[agent],
  tasks=[task],
  process=Process.sequential,
  cache=True,
  max_rpm=100,
  share_crew=True
)

## RabbitMQ

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
        body=str(crew.kickoff(inputs=json.loads(body)))
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=rpc_queue, on_message_callback=on_request)

print("RPC Server Awaiting Requests...")
channel.start_consuming()
