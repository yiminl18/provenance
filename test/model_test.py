
import time 
import sys 
import os

# Get the directory of the current file
current_file_directory = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_directory = os.path.dirname(current_file_directory)
sys.path.append(parent_directory)
from model import model 


def read_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

text = """Capital Improvement Projects (Design)
Marie Canyon Green Streets
(cid:190) Updates:
(cid:131) A hydrology report was prepared and will be used to size the pre-
manufactured biofilters. City staff is reviewing multiple biofilter
manufacturers for filters that will work in the proposed project area. It is
anticipated to have a final design by March 2022. The project will be
advertised for construction bids shortly after this date.
"""
instruction = 'Is Marie Canyon Green Streets project a Capital Improvement Project? Return yes or no. ' 
model_name = 'gpt35'


prompt = (instruction,text)
response = model(model_name,prompt)
print(response)