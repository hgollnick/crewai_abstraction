import pika
import json

from crewai import Agent, Task, Crew, Process
from langchain.agents import Tool
from langchain_openai import AzureChatOpenAI

AZURE = AzureChatOpenAI(
    azure_endpoint="https://dt-openai-lab-001.openai.azure.com/",
    api_key="7c54b5fb598945cabaa58a637455aeb2",
    azure_deployment="gpt-35-turbo",
    api_version="2023-03-15-preview"
)

def comments_func(__query__):
    import requests

    try:
        response = requests.get("https://jsonplaceholder.typicode.com/comments/1")
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching comments: {e}"

comments_api = Tool(
  name="comments_api",
  func=comments_func,
  description="Use this tool to retrieve 'comments' from 'jsonplaceholder.typicode.com'"
)

researcher = Agent(
  role="Senior Researcher",
  goal="Uncover groundbreaking technologies in {topic}",
  verbose=True,
  memory=True,
  backstory="Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world.",
  llm=AZURE,
  tools=[comments_api],
  allow_delegation=True,
)

identify_trends = Task(
  description="Identify the next big trend in {topic}. Focus on identifying pros and cons and the"
    "overall narrative. Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks.)",
  expected_output="A comprehensive 3 paragraphs long report on the latest AI trends.",
  tools=[comments_api],
  agent=researcher,
)

crew = Crew(
  agents=[researcher],
  tasks=[identify_trends],
  process=Process.sequential,
  cache=True,
  max_rpm=100,
  share_crew=True
)

## RabbitMQ
rpc_queue='rpc_queue'

connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="localhost",
            port=int(5672),
            credentials=pika.PlainCredentials(username="guest", password="guest")
        ))

channel = connection.channel()
channel.queue_declare(queue=rpc_queue)

def on_request(ch, method, properties, body):
    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=str(
crew.kickoff(inputs=json.loads(body))
)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=rpc_queue, on_message_callback=on_request)

print("RPC Server Awaiting Requests...")
channel.start_consuming()
