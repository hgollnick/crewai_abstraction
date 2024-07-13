from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI


GROQ_LLM = ChatGroq(
            api_key="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",
            model="llama3-70b-8192"
        )

# GROQ_LLM = AzureChatOpenAI(
#     azure_endpoint="https://dt-openai-lab-001.openai.azure.com",
#     api_key="7c54b5fb598945cabaa58a637455aeb2",
#     azure_deployment="gpt-35-turbo",
#     api_version="2023-03-15-preview"
# )

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

# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[agent],
  tasks=[task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  # memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

# Starting the task execution process with enhanced feedback
result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)