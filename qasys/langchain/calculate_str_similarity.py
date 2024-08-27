# 获取文件夹内所有JSON文件的路径
import os, glob, json
from nltk import word_tokenize
from questions import paper_q, civic_q, notice_q



def insert_layer(input_str, layer_to_insert, after_segment):
    # 找到需要插入的位置
    index = input_str.find(after_segment) + len(after_segment)
    
    # 插入新的层级
    new_str = input_str[:index] + layer_to_insert + input_str[index:]
    
    return new_str

def clean_string(input_string):
    # 使用 isalnum() 方法只保留字母和阿拉伯数字
    cleaned_string = ''.join(char for char in input_string if char.isalnum())
    return cleaned_string

import numpy as np 


def get_embedding(text:str, model="text-embedding-3-small"):
    from openai import OpenAI
    client = OpenAI()
    return np.array(client.embeddings.create(input = [text], model=model).data[0].embedding)

def normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def centralize(vector: np.ndarray, mean_vector: np.ndarray) -> np.ndarray:
    return vector - mean_vector

def get_cosine_similarity(str1:str, str2:str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def get_cosine_distance(str1:str, str2:str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return 1 - dot_product / (norm_vec1 * norm_vec2)

def get_l2_distance(str1: str, str2: str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    distance = np.linalg.norm(vec1 - vec2) ** 2
    return distance

def get_inner_product_similarity(str1: str, str2: str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    inner_product = np.dot(vec1, vec2)
    return inner_product


# def jaccard_similarity_char_union(str1, str2):
#     # 将字符串转换为小写并只保留字母和数字
#     str1 = ''.join(filter(str.isalnum, str1.lower()))
#     str2 = ''.join(filter(str.isalnum, str2.lower()))
    
#     # 将字符串转换为字符集合
#     set1 = set(str1)
#     set2 = set(str2)
    
#     # 计算交集和并集
#     intersection = set1.intersection(set2)
#     union = set1.union(set2)
    
#     # 计算 Jaccard 相似度
#     if len(union) == 0:
#         return 0.0  # 防止分母为零
#     jaccard_sim = len(intersection) / len(union)
    
#     return jaccard_sim

def jaccard_similarity_word_union(str1: str, str2:str):
    """
    Compute the Jaccard similarity between two strings by counting the number of common words.

    Parameters:
    str1 (str): The first string
    str2 (str): The second string

    Returns:
    float: The Jaccard similarity
    """
    # Split the strings into words
    words1 = set(word_tokenize(str1.lower()))
    words2 = set(word_tokenize(str2.lower()))
    # print(words1)
    # print(words2)
    
    # Compute the intersection and union of the two sets
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    # Compute the Jaccard similarity
    if len(union) == 0:
        return 0.0  # Prevent division by zero
    jaccard_sim = len(intersection) / len(union)
    return jaccard_sim

def jaccard_similarity_word_union_cleaned(str1: str, str2:str):
    """
    Compute the Jaccard similarity between two strings by counting the number of common words.

    Parameters:
    str1 (str): The first string
    str2 (str): The second string

    Returns:
    float: The Jaccard similarity
    """
    # Split the strings into words
    words1_list = word_tokenize(str1.lower())
    words2_list = word_tokenize(str2.lower())
    words1_list = [clean_string(w) for w in words1_list]
    words2_list = [clean_string(w) for w in words2_list]
    words1 = set(words1_list)
    words2 = set(words2_list)

    # print(words1)
    # print(words2)
    
    # Compute the intersection and union of the two sets
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    # Compute the Jaccard similarity
    if len(union) == 0:
        return 0.0  # Prevent division by zero
    jaccard_sim = len(intersection) / len(union)
    return jaccard_sim

def calculate_str_similarity(baseline_name:str, dataset_name:str, model_name:str, question_set:list[str]):


    folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

    file_paths = glob.glob(os.path.join(folder_path, '*.json'))

    # scores = [[] for _ in range(len(question_set))]
    scores = []
    # # 依次读取每个JSON文件并解析为字典
    for file_path in file_paths:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"file_path: {file_path}")
            content = json.load(file)
            question = content["question"]
            question_index= question_set.index(question)
            baseline_type = content["baseline_type"]
            document_path = content["document_path"]
            raw_provenance = content["raw_provenance"]
            evidence = content["evidence"]
            raw_answer = content["raw_answer"]
            evidence_answer = content["evidence_answer"]
            search_pool = content["search_pool"]
            jaccard_similarity = jaccard_similarity_word_union(raw_answer, evidence_answer)
            jaccard_similarity_cleaned = jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer)
            cosine_similarity = get_cosine_similarity(raw_answer, evidence_answer)
            # scores[question_index].append(jaccard_similarity_cleaned)
            scores.append(jaccard_similarity_cleaned)

            # cosine_similarity = cosine_similarity(raw_answer, evdience_answer)

            result = {
                "model_name": model_name,
                "baseline_type": baseline_type,
                "document_path": document_path,
                "question": question,
                "raw_provenance": raw_provenance,
                "evidence": evidence,
                "raw_answer": raw_answer,
                "evidence_answer": evidence_answer,
                "search_pool": search_pool,
                "jaccard_similarity": jaccard_similarity,
                "jaccard_similarity_cleaned": jaccard_similarity_cleaned,
                "cosine_similarity": cosine_similarity
            }

            layer_to_insert = "jaccard_union/"
            after_segment = model_name + "/"

            result_path = insert_layer(file_path, layer_to_insert, after_segment)
            print(f"result_path: {result_path}")
            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     baseline_names = ['baseline0', 'baseline1']
#     dataset_names = ['civic', 'paper', 'notice']
#     model_names = ['gpt35', 'gpt4o', 'gpt4omini']
#     question_sets = [civic_q(), paper_q(), notice_q()]
#     for dataset_name, question_set in zip(dataset_names, question_sets):
#         for baseline_name in baseline_names:
#             for model_name in model_names:
#                 calculate_str_similarity(baseline_name, dataset_name, model_name, question_set)
#                 print(f"baseline_name: {baseline_name}, dataset_name: {dataset_name}, model_name: {model_name}")
#     for dataset_name in dataset_names:
#         for baseline_name in baseline_names:
#             for model_name in model_names:
#                 get_average_result(baseline_name, dataset_name, model_name)
    



#     # for question_index, score_for_question in enumerate(scores):
#     #     result = {
#     #         "baseline_name": baseline_name,
#     #         "model_name": model_name,
#     #         "dataset_name": dataset_name,
#     #         "question_index" : question_index,
#     #         "question": question_set[question_index],
#     #         "average_jaccard_similarity": sum(score_for_question) / len(score_for_question)
#     #     }

#     #     with open(folder_path+f"/average_result/average_jaccard_similarity_q{question_index}.json", 'w', encoding='utf-8') as f:
#     #         json.dump(result, f, ensure_ascii=False, indent=4)

#     result = {
#         "baseline_name": baseline_name,
#         "model_name": model_name,
#         "dataset_name": dataset_name,
#         "question_index" : question_index,
#         "question": question_set[question_index],
#         "average_jaccard_similarity": sum(scores) / len(scores)
#     }

#     with open(folder_path+f"/average_result/average_jaccard_similarity.json", 'w', encoding='utf-8') as f:
#         json.dump(result, f, ensure_ascii=False, indent=4)

    # result = {
    #     "baseline_name": baseline_name,
    #     "model_name": model_name,
    #     "dataset_name": dataset_name,
    #     "question_index" : question_index,
    #     "average_jaccard_similarity": sum(scores) / len(scores)
    # }

    # with open(folder_path+"/average_result/average_cosine_similarity.json", 'w', encoding='utf-8') as f:
    #     json.dump(result, f, ensure_ascii=False, indent=4)

# test
# a = "Consolvo, S., McDonald, D.W., Toscos, T., et al."
# b = "Consolvo S."
# print(jaccard_similarity_word_union(a,b))
# a = "Under 49 U.S.C. § 60122 and 49 CFR § 190.223, you are subject to a civil penalty not to exceed \n$257,664 per violation per day the violation persists, up to a maximum of $2,576,627 for a related \nseries of violations.  For violation occurring on or after March 21, 2022 and before January 6, \n2023, the maximum penalty may not exceed $239,142 per violation per day the violation persists, \nup to a maximum of $2,391,412 for a related series of violations.  For violation occurring on or \nafter May 3, 2021 and before March 21, 2022, the maximum penalty may not exceed $225,134 \nper violation per day the violation persists, up to a maximum of $2,251,334 for a related series of \nviolations.  For  violation  occurring  on  or  after  January  11,  2021  and  before  May  3,  2021,  the \nmaximum penalty may not exceed $222,504 per violation per day the violation persists, up to a \nmaximum of $2,225,034 for a related series of violations"
# b = list(set(word_tokenize(a)))
# c = [word for word in b]
# print(c)




# text1 = "May 24"
# text2 = "This will take place on May 23, 2022. At this time, the event will be held in the main hall. All students are required to attend."
# text3 = "Alice is a student. She may attend the event on July 23, 2022. The event will be held in the main hall. Bob may also attend the event."



# similarity = get_cosine_similarity(text1, text2)
# print(f"cosine_similarity btw. text1 and text2: {similarity}")
# similarity = get_cosine_similarity(text1, text3)
# print(f"cosine_similarity btw. text1 and text3: {similarity}")

# text1 = "I am a student"
# text2 = "student I am a"
# print(jaccard_similarity_word_union(text1, text2))
# print(jaccard_similarity_word_union_cleaned(text1, text2))

