import json
import dspy
import openai
import os
import sys
import time

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取父级的父级文件夹路径
parent_parent_dir = os.path.abspath(os.path.join(current_dir, "../../"))
# 将父级的父级文件夹添加到 PYTHONPATH
sys.path.append(parent_parent_dir)
# 现在可以导入 model 模块
from model import model
start_time = time.time()

api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

# model_name = "gpt-3.5-turbo" # this is the name for dspy
model_name = "gpt35" # our model's name rule


# Set up OpenAI API client
openai_model = dspy.OpenAI(model=model_name, api_key=openai.api_key)
dspy.settings.configure(lm=openai_model)

# 读取 JSON 文件
with open('data/dev.json', 'r') as file:
    questions = json.load(file)

questions = questions[:200]

# CoT method
classify = dspy.ChainOfThought('question -> answer', n=1)

# 结果列表
results = []

# Iterate through questions and get rationale and answer
for q in questions:
    question_id = q['question_id']
    question_text = q['question']

    # dspy part, please comment out this part if you want to run our model, because although it won't be stored in the results, it will still be run
    # response = classify(question=question_text)
    # result = {
    #     "question_id": question_id,
    #     "question": question_text,
    #     "rationale": response.completions.rationale,
    #     "answer": response.completions.answer
    # }
    # end dspy part

    # our model part
    instruction = 'Please decompose this question to a chain of questions.' 

    prompt = (question_text,instruction)
    response = model(model_name,prompt)
    result = {
        "question_id": question_id,
        "question": question_text,
        "rationale": response
    }
    # end our model part
    
    results.append(result)

# 将结果保存为 JSON 文件
with open('test/output/ourmodel_decompose_gpt35.json', 'w') as file:
    json.dump(results, file, indent=4)

print("Results have been saved to results.json")

# run time calculationz
total_time = time.time() - start_time
print(f"Total execution time: {total_time:.2f} seconds")
