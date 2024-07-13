from langchain.agents import Tool, AgentType, initialize_agent
from langchain_openai import AzureChatOpenAI

AZURE = AzureChatOpenAI(
    azure_endpoint="https://dt-openai-lab-001.openai.azure.com",
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

agent = initialize_agent([comments_api], AZURE, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True)

agent.invoke({"input": "Get me the comment with ID 1"})