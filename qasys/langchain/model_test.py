
import time 
import sys 
import os

from model import model 


def read_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

Q = "What is the issue date of the notice?"

text = f"Q: {Q}"

instruction = """Can you extract the entities, their attributes and attribute values from sentence Q?
Return the answer in JSON format as shown below:
{
    "entity1": {
        "entity_name": "entity1's name",
        "attributes": {
            "attribute1": "value1",
            "attribute2": "value2"
        }
    },
    "entity2": {
        "entity_name": "entity2's name",
        "attributes": {
            "attribute1": "value1",
            "attribute2": "value2"
        }
    }
}.
If there are no constraints on attributes, return an empty string for the attribute value."""

model_name = 'gpt4o'


prompt = (instruction,text)
response = model(model_name,prompt, json_mode=True)
print(response)