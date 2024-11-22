from langchain_groq import ChatGroq
from crewai import Crew, Process, Agent, Task

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Authenticate using LinkedIn credentials
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Agents are defined with attributes for backstory, cache, and verbose mode
researcher = Agent(
    role='Researcher',
    goal='Conduct in-depth analysis',
    backstory='Experienced data analyst with a knack for uncovering hidden trends.',
    cache=True,
    verbose=False,
    # tools=[]  # This can be optionally specified; defaults to an empty list
    use_system_prompt=True,  # Enable or disable system prompts for this agent
    max_rpm=30,  # Limit on the number of requests per minute
    max_iter=5  # Maximum number of iterations for a final answer
)
writer = Agent(
    role='Writer',
    goal='Create engaging content',
    backstory='Creative writer passionate about storytelling in technical domains.',
    cache=True,
    verbose=False,
    # tools=[]  # Optionally specify tools; defaults to an empty list
    use_system_prompt=True,  # Enable or disable system prompts for this agent
    max_rpm=30,  # Limit on the number of requests per minute
    max_iter=5  # Maximum number of iterations for a final answer
)

egtask = Task(
    description='Find and summarize the latest and most relevant news on AI',
    agent=writer,
    expected_output='A bullet list summary of the top 5 most important AI news',
)

# Establishing the crew with a hierarchical process and additional configurations
project_crew = Crew(
    tasks=[egtask],  # Tasks to be delegated and executed under the manager's supervision
    agents=[researcher, writer],
    manager_llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama3-groq-8b-8192-tool-use-preview"), # Mandatory if manager_agent is not set
    process=Process.hierarchical,  # Specifies the hierarchical management approach
    respect_context_window=True,  # Enable respect of the context window for tasks
    memory=True,  # Enable memory usage for enhanced task execution
    manager_agent=None,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    planning=True,  # Enable planning feature for pre-execution strategy
)
