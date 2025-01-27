from pipeline.baseline.bfs import BFS
import datasets.get_questions as gq

from pathlib import Path
import os

with open(Path.home() / "api_keys" / "openai2.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read()
f.close()


baseline = BFS('gpt-4o-mini', 0.4)

test_question = gq.process_dataset("hotpot", "fullwiki")


Q = test_question[0]['question']
A = test_question[0]['answer']


P = [elem[0] + ': ' + '\n'.join(elem[1]) for elem in test_question[0]['context']]

P = '\n'.join(P)

P
result = baseline.run(Q, A, P)
print(result)
print(baseline.run_performance_history)

