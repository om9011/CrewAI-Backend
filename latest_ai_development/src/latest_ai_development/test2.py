import os
import re
from datetime import datetime

import pandas as pd
import requests
from crewai import Agent, Crew, Process, Task
from crewai_tools import tool
from langchain.agents import load_tools
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


def format_response(response: str) -> str:
    entries = re.split(r"(?<=]), (?=\[)", response)
    return [entry.strip("[]") for entry in entries]


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

human_tools = load_tools(["human"])


@tool("search tool")
def cryptocurrency_news_tool(ticker_symbol: str) -> str:
    """Get news for a given cryptocurrency ticker symbol"""
    return """
    {
        "title": "Bitcoin (BTC) Price Today",
        "description": "The current price of Bitcoin (BTC) along with market cap, trading volume, and other metrics.",
        "url": "https://example.com/bitcoin-price-today"
    },
    {
        "title": "What is Bitcoin (BTC)?",
        "description": "A detailed guide on Bitcoin, its blockchain technology, and why it is the leading cryptocurrency.",
        "url": "https://example.com/what-is-bitcoin"
    },
    {
        "title": "Bitcoin News and Updates",
        "description": "Stay updated with the latest news, updates, and developments related to Bitcoin (BTC).",
        "url": "https://example.com/bitcoin-news"
    }
]"""


llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

system = "You are experienced Machine Learning & AI Engineer."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | llm
response = chain.invoke({"text": "How to increase inference speed for a 7B LLM?"})

customer_communicator = Agent(
    role="Senior cryptocurrency customer communicator",
    goal="Find which cryptocurrency the customer is interested in",
    backstory="""You're highly experienced in communicating about cryptocurrencies
    and blockchain technology with customers and their research needs""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
    tools=human_tools,
)

news_analyst = Agent(
    role="Cryptocurrency News Analyst",
    goal="""Get news for a given cryptocurrency. Write 1 paragraph analysis of
    the market and make prediction - up, down or neutral.""",
    backstory="""You're an expert analyst of trends based on cryptocurrency news.
    You have a complete understanding of macroeconomic factors, but you specialize
    into analyzing news.
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
    tools=[cryptocurrency_news_tool],
)

price_analyst = Agent(
    role="Cryptocurrency Price Analyst",
    goal="""Get historical prices for a given cryptocurrency. Write 1 paragraph analysis of
    the market and make prediction - up, down or neutral.""",
    backstory="""You're an expert analyst of trends based on cryptocurrency
    historical prices. You have a complete understanding of macroeconomic factors,
    but you specialize into technical analys based on historical prices.
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
)

writer = Agent(
    role="Cryptocurrency Report Writer",
    goal="""Write 1 paragraph report of the cryptocurrency market.""",
    backstory="""
    You're widely accepted as the best cryptocurrency analyst that
    understands the market and have tracked every asset for more than 10 years. Your trends
    analysis are always extremely accurate.

    You're also master level analyst in the traditional markets and have deep understanding
    of human psychology. You understand macro factors and combine those multiple
    theories - e.g. cycle theory. You're able to hold multiple opininons when analysing anything.

    You understand news and historical prices, but you look at those with a
    healthy dose of skepticism. You also consider the source of news articles.

    Your most well developed talent is providing clear and concise summarization
    that explains very complex market topics in simple to understand terms.

    Some of your writing techniques include:

    - Creating a bullet list (executive summary) of the most importannt points
    - Distill complex analyses to their most important parts

    You writing transforms even dry and most technical texts into
    a pleasant and interesting read.""",
    llm=llm,
    verbose=True,
    max_iter=5,
    memory=True,
    allow_delegation=False,
)

get_cryptocurrency = Task(
    description=f"Ask which cryptocurrency the customer is interested in.",
    expected_output="""Cryptocurrency symbol that the human wants you to research e.g. BTC.""",
    agent=customer_communicator,
)

get_news_analysis = Task(
    description=f"""
    Use the search tool to get news for the cryptocurrency

    The current date is {datetime.now()}.

    Compose the results into a helpful report""",
    expected_output="""Create 1 paragraph report for the cryptocurrency,
    along with a prediction for the future trend
    """,
    agent=news_analyst,
    context=[get_cryptocurrency],
)

get_price_analysis = Task(
    description=f"""
    Use the price tool to get historical prices

    The current date is {datetime.now()}.

    Compose the results into a helpful report""",
    expected_output="""Create 1 paragraph summary for the cryptocurrency,
    along with a prediction for the future trend
    """,
    agent=price_analyst,
    context=[get_cryptocurrency],
)

write_report = Task(
    description=f"""Use the reports from the news analyst and the price analyst to
    create a report that summarizes the cryptocurrency""",
    expected_output="""1 paragraph report that summarizes the market and
    predicts the future prices (trend) for the cryptocurrency""",
    agent=writer,
    context=[get_news_analysis, get_price_analysis],
)

crew = Crew(
    agents=[customer_communicator, price_analyst, news_analyst, writer],
    tasks=[get_cryptocurrency, get_news_analysis, get_price_analysis, write_report],
    verbose=2,
    process=Process.sequential,
    full_output=True,
    share_crew=False,
    manager_llm=llm,
    max_iter=15,
)

results = crew.kickoff()