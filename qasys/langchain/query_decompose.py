import getpass
import os
import json
from model import model
from questions import civic_q, paper_q, notice_q

def json_flatten_2list(json_data):
    result = []
    for entity_key, entity in json_data.items():
        try:
            result.append(entity["entity_name"])
        except(KeyError):
            pass
        try:
            attributes = entity["attributes"]
        except(KeyError):
            continue
        for attribute_name, attribute_value in attributes.items():
            result.append(attribute_name)
            result.append(attribute_value)
    result= [x for x in result if x] # filter '' elements
    return result

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
    

# def query_extractor(question: str, model_name = 'gpt35') -> dict:
#     text = f"Q: {question}"
#     instruction = """Can you extract the entities, their attriubtes and attribute values from sentence Q?
#     Return the answer in JSON format as shown below:
#     {
#         "entity1": {
#             "entity_name": "entity1's name",
#             "attributes": {
#                 "attribute1's name": "attribute1's value",
#                 "attribute2's name": "attribute2's value"
#             }
#         },
#         "entity2": {
#             "entity_name": "entity2's name",
#             "attributes": {
#                 "attribute1's name": "attribute1's value",
#                 "attribute2's name": "attribute2's value"
#             }
#         }
#     }.
#     If there are no constraints on attributes, return an empty string for the attribute value. Do not decompose a date like 'May 23, 2023' into its components."""

#     prompt = (instruction,text)
#     response = model(model_name,prompt, json_mode=True)
#     return json.loads(response)


def query_extractor(question: str, model_name = 'gpt35') -> list:
    bad_words = ['Yes', 'No', 'yes', 'no', 'YES', 'NO', 'None', 'none', 'NONE', "I don't know.",]
    if question in bad_words:
        return []
    text = f"Q: {question}"

    instruction = """Your task is to decompose a sentence Q into its components. \
        If the sentence is a single entity, return the entity name. \
        If the sentence contains multiple entities, ectract these entities and use @ to separate them. \
        If the sentence is a predicate (or condition, e.g. date) , return the predicate as it is. \
        If the sentence contains multiple predicates, extract these predicates and use @ to separate them. \
        If the sentence is a mix of entities and predicates, extract all these entities and predicates and use @ to separate them.\
            """

    prompt = (instruction,text)
    response = model(model_name,prompt)
    return response.split('@')

def answer_extractor(question: str, model_name = 'gpt35') -> list:
    return query_extractor(question, model_name)

# question = 
# a = query_extractor("2017", 'gpt4o')
# print(a)
# print(json_flatten_2list(a))

# if __name__ == "__main__":
#     question_set = notice_q()
#     dataset_name = 'notice'
#     json_to_store = {}
#     model_names = ['gpt35', 'gpt4o', 'gpt4omini']
#     for model_name in model_names:
#         for i, question in enumerate(question_set):
#             extracted_dict = query_extractor(question, model_name=model_name)
#             json_to_store[f"question_{i}"] = {"question": question, "extracted": extracted_dict}

#         with open(f'test/output/provenance/questionset_{dataset_name}_{model_name}.json', 'w', encoding='utf-8') as f:
#             json.dump(json_to_store, f, ensure_ascii=False, indent=4)