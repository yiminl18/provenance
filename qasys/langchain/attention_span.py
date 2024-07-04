from model import model
import ast

def attention_span_llm_approach(Q, A, P, model_name = 'gpt35'):
    text = f"Q: {Q}\nA: {A}\nP: {P}"

    instruction = """You are an expert in identifying evidence. Given a question Q, its answer A, and a relevant text span P, your task is to find one or more Attention Text Span(s) that lead to the answer A. An Attention Text Span is a sub-span within P that directly contributes to answering Q and generating A. The returned Attention Text Span(s) should be as concise as possible and MUST BE RAW TEXT EXTRACTED FROM P.

    Now, I will provide you with Q, A, and P. 
    ###
    Return format requirements:
    - If you find one or more Attention Text Span(s) in P that lead to A, please return the Attention Text Span(s) as a list like ['Hi how are you', 'I am fine thank you']. 
    - If no Attention Text Span(s) can be found, please only return None.
    ###
    Now give me your List:
    """

    prompt = (instruction,text)
    response = model(model_name,prompt) # response is a string
    result = []
    None_list = ['None', 'none', 'NONE', 'None.']
    flag = False

    if response in None_list:
        return result, response, False
    
    try:
        response_list = ast.literal_eval(response)
    except:
        return result, response, False

    for r in response_list:
        if contains_text(clean_text(P), clean_text(r)):
            result.append(r)
            flag = True

    return result, response, flag

import re

def clean_text(text):
    """
    去除文本中的特殊字符，只保留字母和数字
    
    :param text: 输入文本 (str)
    :return: 处理后的文本 (str)
    """
    return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '', text).lower()

def contains_text(main_text, sub_text):
    """
    检查main_text中是否包含sub_text
    
    :param main_text: 主文字 (str)
    :param sub_text: 子文字 (str)
    :return: bool
    """
    return sub_text in main_text