from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

from langchain.tools.retriever import create_retriever_tool

import text_splitter, vector_database, document_loader
from dotenv import load_dotenv

GROQ_LLM = ChatGroq(
            api_key="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",
            model="llama3-70b-8192"
        )

load_dotenv("azure.env")
documents = document_loader.load_docs()
splited_docs = text_splitter.split_docs(documents)
vectordb = vector_database.create_vector_database(splited_docs)


def create_verctor_db_tool(retriever):
    return create_retriever_tool(
        retriever,
        "Vector DB Retriever",
        "Vector database retriever to get information about Complience",
    )

agent = Agent(
  role='Complience Officer',
  goal='Answer questions about complience and risk management.',
  verbose=True,
  memory=True,
  backstory=(
    "You're an officer conducting investigations, implementing compliance programs,"
    " and mitigating risk to ensure organizational integrity."
  ),
  llm=GROQ_LLM,
  tools=[create_verctor_db_tool(vectordb.as_retriever())],
  allow_delegation=True,
)

writer = Agent(
    role='Email Writer Agent',
    goal="""If there is any complience misconduct, write an email explaining what should be done to improve misconduct,
    otherwise, write an email explaining that there is no misconduct.""",
    backstory="""You are a master at synthesizing a variety of information and writing a helpful email \
    that will address the customer's issues and provide them with helpful information""",
    llm=GROQ_LLM,
    verbose=True,
    allow_delegation=False,
    max_iter=5,
    memory=True,
    # step_callback=lambda x: print_agent_output(x,"Email Writer Agent"),
)


task = Task(
  description=(
    "Identify if \"{topic}\", goes by complience."
  ),
  expected_output='A one paragraph comprehensive report answering if there is any complience misconduct.',
  tools=[create_verctor_db_tool(vectordb.as_retriever())],
  agent=agent, 
)

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[agent, writer],
  tasks=[task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  # memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'Can I use companies property for personal use?'})
print(result)