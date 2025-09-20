import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# Tools
search_tool = SerperDevTool()

# Agents
researcher = Agent(
    role="AI Research Specialist",
    goal="Discover the latest AI trends about {topic}",
    backstory="Expert researcher uncovering AI developments for professionals.",
    tools=[search_tool],
    memory=True,
    verbose=True,
)

analyst = Agent(
    role="Data Analyst",
    goal ="Analyse data found and provide insights",
    backstory="Expert Data Analyst, knows all required metrics to measure AI performance and language",
    tools=['analysis_tool'],
    memory=True,
    verbose=True,
    allow_delegation=True, # para delegar a analise pro racional
)

Rationalist = Agent(

)

writer = Agent(
    role="LinkedIn AI Content Writer",
    goal="Write engaging LinkedIn-style articles about {topic}",
    backstory="Professional writer who makes AI trends insightful and approachable.",
    tools=[],
    memory=True,
    verbose=True,
    allow_delegation=False,
)

# Tasks
research_task = Task(
    description=(
        "Research the latest developments and insights about {topic}. Summarize 3–5 main points."
    ),
    expected_output="A structured summary of 3-5 main points about {topic}.",
    agent=researcher,
    tools=[search_tool],
)

write_task = Task(
    description=(
        "Write a professional LinkedIn article about {topic}, using the research provided. "
        "Tone: professional but approachable. End with a question for engagement."
    ),
    expected_output="A LinkedIn-style article of 3–5 short paragraphs.",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
)

def run_article_generation(topic: str):
    result = crew.kickoff(inputs={"topic": topic})
    return result
