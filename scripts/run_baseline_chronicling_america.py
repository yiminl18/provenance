from pipeline.baseline.llm_query import LLMQuery
import datasets.get_questions as gq
from pathlib import Path
import os

with open(Path.home() / "api_keys" / "openai2.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read()
f.close()

baseline = LLMQuery('gpt-4o-mini')

test_question = gq.process_dataset("chroniclingamerica", "dev")

Q = test_question[0]['question']
A = test_question[0]['answer']


P = test_question[0]['context']


result = baseline.run(Q, A, P)
print(result)
print(baseline.llm_performance_history)
print(baseline.get_total_time())

