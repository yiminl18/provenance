from pipeline.baseline.llm_query import LLMQuery
import datasets.get_questions as gq

from pathlib import Path
import os

with open(Path.home() / "api_keys" / "openai2.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read()
f.close()

baseline = LLMQuery('gpt-4o-mini')

test_question = gq.process_dataset('naturalquestions', 'dev')


Q = test_question[0]['question']

# can be yes, no, or none
YN = test_question[0]['yes_no_answer']

# can be a list or empty (there is no short answer, it's a yes/no question, or the long_answer to the question is not in the document text)
A = test_question[0]['answer']['short_answers'][0]

# can be a list or empty
P = test_question[0]['answer']['long_answers'][0]


result = baseline.run(Q, A, P)
print(result)
print(baseline.llm_performance_history)
print(baseline.get_total_time())

