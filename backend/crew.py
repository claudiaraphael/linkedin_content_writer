import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

#### Tools
search_tool = SerperDevTool()
analysis_tool = SerperDevTool()



#### Agents
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
    role="Data Rationalizer",
    goal ="Your role is to understand the analysis of the Data Analyst and explain the rational decisions behind it's analysis' results.",
    backstory="Expert Mathmatician and Statistician, with a deep understanding of data analysis and interpretation. You have a nack for explaining complex mathmatical processes in a way that any CEO can understand, without omissing any relevant inforamtion for data justification.",
    tools=['analysis_tool'],
    memory=True,
    verbose=True,
    allow_delegation=True, # para delegar o racional e a analise pro writer
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

#### Tasks

research_task = Task(
    description=(
        "Research the latest developments and insights about {topic}. Summarize 3–5 main points."
    ),
    expected_output="A structured summary of 3-5 main points about {topic}.",
    agent=researcher,
    tools=[search_tool],
    background_info=[
        "Search the web for the latest news about {topic} from the last 30 days.",
        "Search specifically for news from the last 2 weeks first for the first 3 bullet points of the 5 you will write",
        "stick to your task of researching the latest news about {topic}, and summarize eah piece of news you find into 5 bullet points",
        "The last 2 bulletpoints should be reserved for major news in the last 30 days, such as information relating to significant news about FAANG, Openai and the Chinese, Deepseek. We are seeking news like new products, new features, new models, new metrics, new technology, microchip production, datacenters."     
     ],
    context=[background_info]
)

analysis_task = Task(
    description=(
        "Analyse the data provided by the AI Research Specialist and provide insights."
        ),
    agent=analyst,
    tools=[analysis_tool],
    context=[research_task],

)

rationale_task = Task(
    description=("Understand the analysis of the Data Analyst and explain the rational decisions behind it's analysis' results."),
    agent=Rationalist,
    tools=[analysis_tool],
    context=[analysis_task],
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
