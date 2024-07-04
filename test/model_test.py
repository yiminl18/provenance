
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

Q = "Starting date of disaster projects after 2021"
A = "The disaster project \"Broad Beach Road Water Quality Infrastructure Repairs\" is scheduled to begin construction in Spring 2022. The disaster project \"Latigo Canyon Road Roadway/Retaining Wall Improvements\" is currently in the design phase, with no specific start date mentioned. The project \"Marie Canyon Green Streets\" is anticipated to have a final design by March 2022 and will be advertised for construction bids shortly after that date.",



P = """Management Plan. This project is scheduled to be accepted by the Council \r\nat the January 24, 2022 meeting.\r\nDisaster Projects (Design)\r\nBroad Beach Road Water Quality Infrastructure Repairs (CalJPIA Project)\r\n¾ Updates:\r\n The project consultant prepared the specifications for the project. Staff \r\nis finalizing the bid documents.\r\n¾ Project Schedule:\r\n Complete Design: February 2022\r\n Begin Construction: Spring 2022\r\nLatigo Canyon Road Roadway/Retaining Wall Improvements (FEMA Project)\r\n¾ Updates:\r\n Staff is finalizing the design of this project."""

text = f"Q: {Q}\nA: {A}\nP: {P}"

instruction = """You are an expert in identifying evidence. Given a question Q, its answer A, and a relevant text span P, your task is to find one or more Core Evidence Segments that lead to the answer A. A Core Evidence Segment is a sub-span within P that directly contributes to answering Q and generating A. The returned Core Evidence Segment(s) should be as concise as possible and MUST BE RAW TEXT EXTRACTED FROM P. If no Core Evidence Segment can be found, please only return None.

Now, I will provide you with Q, A, and P. Please identify and return the Core Evidence Segments as a list like ['Hi how are you', 'I am fine thank you']."""

model_name = 'gpt4o'


prompt = (instruction,text)
response = model(model_name,prompt)
print(response)