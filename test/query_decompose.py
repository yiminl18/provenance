import getpass
import os

path = '/Users/yiminglin/Documents/Codebase/config/openai/config.txt'

def read_key(path):
    with open(path, 'r') as file:
    # Iterate over each line in the file
        content = file.read()
        lines = content.split('\n')
    return lines[0]

api_key = read_key(path)
os.environ["OPENAI_API_KEY"] = api_key

# Optional, uncomment to trace runs with LangSmith. Sign up here: https://smith.langchain.com.
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()

import datetime
from typing import Literal, Optional, Tuple

from langchain_core.pydantic_v1 import BaseModel, Field


class SubQuery(BaseModel):
    """Search over a database of tutorial videos about a software library."""

    sub_query: str = Field(
        ...,
        description="A very specific query against the database.",
    )

from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

system = """You are an expert at converting user questions into database queries. \
You have access to a database of tutorial videos about a software library for building LLM-powered applications. \

Perform query decomposition. Given a user question, break it down into distinct sub questions that \
you need to answer in order to answer the original question.

If there are acronyms or words you are not familiar with, do not try to rephrase them."""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
llm_with_tools = llm.bind_tools([SubQuery])
parser = PydanticToolsParser(tools=[SubQuery])
query_analyzer = prompt | llm_with_tools | parser

l = query_analyzer.invoke(
    {
        "question": "what are the top-3 movies whose actor is john and released after 2020"
    }
)

print(l)