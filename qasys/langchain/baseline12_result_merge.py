# 获取文件夹内所有JSON文件的路径
import os, glob, json
from nltk import word_tokenize
from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path
from label_file import append_to_json_file

baseline_names = ['baseline1_0.7', 'baseline2']
combined_baseline_name = 'baseline1_0.7_and_2'
baseline_indexes = [1, 2]
dataset_names = ['civic','paper','notice']
model_names = ['gpt4o']
question_set = [civic_q(), paper_q(), notice_q()] # same index as dataset_names
path_set = [civic_path(), paper_path(), notice_path()] # same index as dataset_names

def sort_set_by_list_order(original_list, my_set):
    # 按照原始列表中的顺序对集合中的元素排序
    sorted_list = [item for item in original_list if item in my_set]
    return sorted_list

def get_precision(prediction, ground_truth):
    # 计算精确度
    if len(prediction) == 0:
        return 0.0  # 防止分母为零
    precision = len(set(prediction).intersection(set(ground_truth))) / len(prediction)
    return precision

def get_recall(prediction, ground_truth):
    # 计算召回率
    if len(ground_truth) == 0:
        return 0.0  # 防止分母为零
    recall = len(set(prediction).intersection(set(ground_truth))) / len(ground_truth)
    return recall

def get_f1_score(precision, recall):
    # 计算 F1 分数
    if precision + recall == 0:
        return 0.0  # 防止分母为零
    f1_score = 2 * precision * recall / (precision + recall)
    return f1_score

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

def precision_loss(prediction:list[str], ground_truth: list[str]):
    """
    Compute the precision loss between two lists of strings.

    Parameters:
    list1 (list): The first list of strings
    list2 (list): The second list of strings

    Returns:
    float: The precision loss
    list: The sentences in prediction that are not in ground_truth, sentences that being wrongly predicted
    """

    precision = get_precision(prediction, ground_truth)

    # Convert the lists to sets
    set1 = set(prediction)
    set2 = set(ground_truth)
    
    # Compute the intersection of the two sets
    intersection = set1.intersection(set2)
    
    # Compute the precision loss ((set1-set1 intersect set2)/set1)
    
    precision_loss_sentences = set1 - intersection # a subset of set1, a set of prediction
    print()
    print(prediction)
    print(precision_loss_sentences)
    
    return precision, sort_set_by_list_order(prediction, precision_loss_sentences)

import numpy as np 


def get_embedding(text:str, model="text-embedding-3-small"):
    from openai import OpenAI
    client = OpenAI()
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def get_cosine_similarity(str1:str, str2:str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

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

if __name__ == "__main__":    
    for dataset_index, dataset_name in enumerate(dataset_names):
        for model_name in model_names:
            for question_index, question in enumerate(question_set[dataset_index]):
                for path_index, path in enumerate(path_set[dataset_index]):
                    baseline_name = baseline_names[0]
                    baseline_index = baseline_indexes[0]
                    with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/labeled_file/b{baseline_index}_{dataset_name}_{model_name}_q{question_index}_d{path_index}.json', 'r') as file0: # f is a list of dict element
                        content_list = json.load(file0)
                        for content_index, content0 in enumerate(content_list):
                            evidence_answer_0 = content0["evidence_answer"] # evidence_answer_0 is list of str, of baseline1_0.7
                            evidence_0 = content0["evidence"]
                            jaccard_similarity_0 = content0["jaccard_similarity"]
                            if jaccard_similarity_0 < 0.5:
                                baseline_name = baseline_names[1]
                                baseline_index = baseline_indexes[1]
                                with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/labeled_file/b{baseline_index}_{dataset_name}_{model_name}_q{question_index}_d{path_index}.json', 'r') as file1: # f is a list of dict element
                                    content_list = json.load(file1)
                                    content1 = content_list[content_index]
                                    evidence_answer_1 = content1["evidence_answer"] # evidence_answer_0 is list of str, of baseline2, ground_truth
                                    evidence_1 = content1["evidence"]
                                
                                precision, PL_sentences = precision_loss(evidence_0, evidence_1) # precision loss, P2里P1没有capture的句子
                                recall, RL_sentences = precision_loss(evidence_1, evidence_0) # recall loss, P1里P2没有capture的句子
                                print("score: ", jaccard_similarity_0)
                                print("PL: ", precision)
                                print("RL: ", recall)
                                print("PL_sentences: ", PL_sentences)
                                print("RL_sentences: ", RL_sentences)
                                f1_score = get_f1_score(precision, recall)
                                dict_to_save = {
                                    "question": question,
                                    "raw_answer": evidence_answer_1,
                                    "evidence_answer": evidence_answer_0,
                                    
                                    "jaccard_similarity": jaccard_similarity_0,
                                    "precision": precision,
                                    "recall": recall,
                                    "f1_score": f1_score,
                                    "precision_loss_sentences": PL_sentences,
                                    "recall_loss_sentences": RL_sentences,
                                    
                                    "predicted_evidence": content0["evidence"],
                                    "ground_truth_evidence": content1["evidence"],
                                    "index_to_delete": content1["index_to_delete"],

                                    "search_pool": content0["search_pool"],
                                    
                                    
                                    "provenance": content0["raw_provenance"],


                                    "model_name": model_name,
                                    "baseline_name_0": baseline_names[0],
                                    "baseline_name_1": baseline_names[1],
                                    "document_path": path,
                                    
                                }
                                append_to_json_file(f'test/output/provenance/{combined_baseline_name}/{dataset_name}/{model_name}/{dataset_name}_{model_name}_q{question_index}_d{path_index}.json', dict_to_save)


        # for question_index, question in enumerate(question_set[dataset_index]):
        #     result = {
        #         f'q_{question_index}': sum(question_score[question_index]) / len(question_score[question_index])
        #     }
        #     append_to_json_file(f'test/output/provenance/{baseline_name}/{dataset_name}/question_score.json', result)

        # for path_index, path in enumerate(path_set[dataset_index]):
        #     result = {
        #         f'd_{path_index}': sum(document_score[path_index]) / len(document_score[path_index])
        #     }
        #     append_to_json_file(f'test/output/provenance/{baseline_name}/{dataset_name}/document_score.json', result)
                # baselineresult={}
                # folder_paths = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/jaccard_union'
                # for folder_path in folder_paths:
                #     file_paths = glob.glob(os.path.join(folder_path, '*.json'))

                #     scores = []
                #     # # 依次读取每个JSON文件并解析为字典
                #     for file_path in file_paths:
                #         # 打开文件并读取内容
                #         with open(file_path, 'r', encoding='utf-8') as file:
                #             print(f"file_path: {file_path}")
                #             content = json.load(file)
                #             question = content["question"]
                #             baseline_type = content["baseline_type"]
                #             document_path = content["document_path"]
                #             raw_provenance = content["raw_provenance"]
                #             evidence = content["evidence"]
                #             raw_answer = content["raw_answer"]
                #             evidence_answer = content["evidence_answer"]
                #             search_pool = content["search_pool"]
                #             jaccard_similarity = jaccard_similarity_word_union(raw_answer, evidence_answer)
                #             jaccard_similarity_cleaned = jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer)
                #             cosine_similarity = get_cosine_similarity(raw_answer, evidence_answer)
                #             scores.append(cosine_similarity)

                #             # cosine_similarity = cosine_similarity(raw_answer, evdience_answer)

                #             result = {
                #                 "model_name": model_name,
                #                 "baseline_type": baseline_type,
                #                 "document_path": document_path,
                #                 "question": question,
                #                 "raw_provenance": raw_provenance,
                #                 "evidence": evidence,
                #                 "raw_answer": raw_answer,
                #                 "evidence_answer": evidence_answer,
                #                 "search_pool": search_pool,
                #                 "jaccard_similarity": jaccard_similarity,
                #                 "jaccard_similarity_cleaned": jaccard_similarity_cleaned,
                #                 "cosine_similarity": cosine_similarity
                #             }

                #             layer_to_insert = "scored/"
                #             after_segment = model_name + "/"

                #             result_path = insert_layer(file_path, layer_to_insert, after_segment)
                #             print(f"result_path: {result_path}")
                #             with open(result_path, 'w', encoding='utf-8') as f:
                #                 json.dump(result, f, ensure_ascii=False, indent=4)

                #     result = {
                #         "baseline_name": baseline_name,
                #         "model_name": model_name,
                #         "dataset_name": dataset_name,
                #         "average_jaccard_similarity": sum(scores) / len(scores)
                #     }

                #     with open(folder_path+"/average_result/average_cosine_similarity.json", 'w', encoding='utf-8') as f:
                #         json.dump(result, f, ensure_ascii=False, indent=4)

