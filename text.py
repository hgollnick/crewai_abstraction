from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

GROQ_LLM = ChatGroq(
            api_key="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",
            model="llama3-70b-8192"
        )

researcher = Agent(
  role="Senior Researcher",
  goal="Uncover groundbreaking technologies in {topic}",
  verbose=True,
  memory=True,
  backstory="Driven by curiosity, you're at the forefront of"
    "innovation, eager to explore and share knowledge that could change"
    "the world.",
  llm=GROQ_LLM,
  tools=[],
  allow_delegation=True
)

identify_trends = Task(
  description="Identify the next big trend in {topic}. Focus on identifying pros and cons and the overall narrative. Your final report should clearly articulate the key points,its market opportunities, and potential risks.)",
  expected_output="A comprehensive 3 paragraphs long report on the latest AI trends.",
  tools=[],
  agent=researcher
)

crew = Crew(
  agents=[researcher],
  tasks=[identify_trends],
  process=Process.sequential,
  cache=True,
  max_rpm=100,
  share_crew=True
)

print(crew.kickoff(inputs={'topic':'AI'}))
