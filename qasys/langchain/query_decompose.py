import getpass
import os
import json

def read_questions(file_path):

    # Open the file and load the data
    with open(file_path, 'r') as file:
        data = json.load(file)
    q = []
    sql = []
    for item in data:
        q.append(item.get('question'))
        sql.append(item.get('SQL'))
    return q, sql

api_key = os.getenv('OPENAI_API_KEY')

# Optional, uncomment to trace runs with LangSmith. Sign up here: https://smith.langchain.com.
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()

import datetime
from typing import Literal, Optional, Tuple

from langchain_core.pydantic_v1 import BaseModel, Field


class SubQuery(BaseModel):
    """Search over a document collections of civic agenda projects."""

    sub_query: str = Field(
        ...,
        description="A very specific question against the projects.",
    )

from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def query_decomposition(question):
    '''
    Input: question, str
    Output: subquestions, list of class SubQuery
    '''
    system_prompt = """You are an expert at converting user questions into  sub-questions. \

    Perform query decomposition. Given a user question, break it down into distinct sub questions that \
    you need to answer in order to answer the original question.

    If there are acronyms or words you are not familiar with, do not try to rephrase them."""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    llm_with_tools = llm.bind_tools([SubQuery])
    parser = PydanticToolsParser(tools=[SubQuery])
    query_analyzer = prompt | llm_with_tools | parser

    # Print the prompt
    formatted_prompt = prompt.format(question=question)

    l = query_analyzer.invoke(
        {
            "question": question
        }
    )   
    # print(str(l))

    return l, formatted_prompt

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def sample_questions():
    q = []
    q.append('What is the number of disaster projects starting later than 2021?') # Civic
    q.append('What are the titles for papers whose topic is related to AI and publication year is later than 2018?') # Paper

    return q 

def civic_questions():
    q = []
    q.append('What is the number of disaster projects starting later than 2021?') # Civic
    # q.append('There exists at least two projects that are related to disaster and have a start date later than 2021. Please give me the name of these two projects') # Civic
    # q.append("What are the names of projects that are related to disaster and have a start date later than 2021? Only list the names of these projects") # Civic
    # q.append("What is the name of the project in design that has the earliest construction start date?")
    # q.append("How many project under construction are being discussed in the document?")
    # q.append("What is the number of vehicle related projects?")


    return q

def paper_questions():
    q = []
    # q.append('What are the titles for papers whose topic is related to AI and publication year is later than 2018?') # Paper
    # q.append('What statistical methods are used when processing data from user studies?')
    # q.append('How many statistical methods are used when processing data from user studies?')
    # q.append('How many user studies are taken in the paper?')
    # q.append("What is the publication year of this paper?")
    # q.append("How many authors are there in this paper?")
    # q.append("What are the emails of the authors that are not Gmail and end with 'edu'?")
    q.append('How many authors are there for this paper?')

    return q

if __name__ == "__main__":

    #q, sql = read_questions('/Users/yiminglin/Documents/Codebase/provenance/data/questions/q_text_sql.json')
    q = sample_questions()
    output = []
    for i in range(len(q)):
        result = {}
        question = q[i]
        #SQL = sql[i]
        print(i)
        #print(question)
        subq = query_decomposition(question)
        result['question'] = question
        result['subquestions'] = subq
        output.append(result)
        #print(SQL)
        if(i>=5):
            break
    
    write_json(output, 'data/questions/sample_output.json')
    