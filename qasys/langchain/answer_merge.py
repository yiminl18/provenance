import os, sys
# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取父级的父级文件夹路径
parent_parent_dir = os.path.abspath(os.path.join(current_dir, "../../"))
# 将父级的父级文件夹添加到 PYTHONPATH
sys.path.append(parent_parent_dir)
# 现在可以导入 model 模块
from model import model

def merge_answers(question, sub_query_list, sub_answer):
    '''
    Input: question, str
           sub_query_list, list of str
           sub_answer, list of str
    Output: final_answer, str
    '''
    model_name = 'gpt35'
    system = """You are an expert at merging sub-answers into a final answer. \
                Perform query merging, given a initial question,\
                a list of its sub-querys and sub-answers, merge them into a final answer. \
                These sub-answers are generated correspondingly from the sub-questions that\
                have been well decomposed. \
                Hence you need to find an intersection between the sub-answers to generate the final answer\
                for the initial question. \
                If there are acronyms or words you are not familiar with, do not try to rephrase them."""
    
    prompt = (system, str({'question': question, 'sub_query_list': str(sub_query_list), 'sub_answer': sub_answer}))
    response = model(model_name,prompt)
    return response