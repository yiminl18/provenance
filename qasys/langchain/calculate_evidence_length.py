# 获取文件夹内所有JSON文件的路径
import os, glob, json
from nltk import word_tokenize
from pretrain_sentence_splitter import get_token_num_for_list, get_token_num

# baseline_name = 'baseline2_sequential'
dataset_names = ['civic', 'paper', 'notice',]
model_names = ['gpt4o', 'gpt35', 'gpt4omini']

def insert_layer(input_str, layer_to_insert, after_segment):
    # 找到需要插入的位置
    index = input_str.find(after_segment) + len(after_segment)
    
    # 插入新的层级
    new_str = input_str[:index] + layer_to_insert + input_str[index:]
    
    return new_str



# print(f"baseline_name: {baseline_name}, total file number: {len(length_of_provenance)}")

def calculate_evidence_length(baseline_name = 'baseline0', dataset_names = ['civic','paper','notice'], model_names = ['gpt4o', 'gpt35', 'gpt4omini']):
    length_of_provenance = []
    length_of_provenance_sentence = []
    length_of_evidence = []
    length_of_evidence_sentence = []
    length_of_raw_answer = []
    length_of_evidence_answer = []
    ration_of_evidence_to_provenance = []
    length_of_raw_sentences = []
    for model_name in model_names:
        for dataset_name in dataset_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
            file_paths = glob.glob(os.path.join(folder_path, '*.json'))
            
            # # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    # print(f"file_path: {file_path}")
                    content = json.load(file)
                    question = content["question"]
                    baseline_type = content["baseline_type"]
                    document_path = content["document_path"]
                    raw_provenance = content["raw_provenance"]
                    evidence = content["evidence"]
                    raw_answer = content["raw_answer"]
                    evidence_answer = content["evidence_answer"]
                    # search_pool = content["search_pool"]
                    # raw_sentences = content["sentences"] # a list of str
                    jaccard_similarity = content["jaccard_similarity"]
                    # if jaccard_similarity <= 0.99:
                    #     continue

                    # cosine_similarity = cosine_similarity(raw_answer, evdience_answer)
                    for rp in raw_provenance:
                        length_of_provenance_sentence.append(get_token_num(rp))
                        # print(length_of_provenance[-1])
                    length_of_provenance.append(get_token_num_for_list(raw_provenance))
                    for e in evidence: # evidence is a list of sentences, sentence is str
                        length_of_evidence_sentence.append(get_token_num(e))
                    # for re in raw_sentences:
                    #     length_of_raw_sentences.append(get_token_num(re))
                    length_of_raw_answer.append(get_token_num(raw_answer))
                    if get_token_num(raw_answer) == 2048:
                        print(f"{file}")
                    length_of_evidence_answer.append(get_token_num(evidence_answer))
                    # print(length_of_provenance[-1])
                    length_of_evidence.append(get_token_num_for_list(evidence))
                    # print(length_of_evidence[-1])
    print("")
    print(f"baseline_name: {baseline_name}")
    print(f"average length_of_provenance: {sum(length_of_provenance)/len(length_of_provenance)}")
    print(f"average length_of_evidence: {sum(length_of_evidence)/len(length_of_evidence)}")
    print(f"average ration_of_evidence_to_provenance: {sum(length_of_evidence) / sum(length_of_provenance)}")
    print(f"average number of evidence sentence: {len(length_of_evidence_sentence)/len(length_of_evidence)}") # len(length_of_evidence) is the number of files
    print(f"average number of raw sentence: {len(length_of_raw_sentences)/len(length_of_evidence)}")
    print(f"average length_of_provenance_chunk: {sum(length_of_provenance_sentence)/len(length_of_provenance_sentence)}")
    print(f"min length_of_provenance_chunk: {min(length_of_provenance_sentence)}")
    print(f"max length_of_provenance_chunk: {max(length_of_provenance_sentence)}")
    print(f"average length_of_evidence_sentence: {sum(length_of_evidence_sentence)/len(length_of_evidence_sentence)}")
    print(f"min length_of_evidence_sentence: {min(length_of_evidence_sentence)}")
    print(f"max length_of_evidence_sentence: {max(length_of_evidence_sentence)}")
    print(f"average length_of_raw_answer: {sum(length_of_raw_answer)/len(length_of_raw_answer)}")
    print(f"max length_of_raw_answer: {max(length_of_raw_answer)}")
    print(f"min length_of_raw_answer: {min(length_of_raw_answer)}")
    print(f"average length_of_evidence_answer: {sum(length_of_evidence_answer)/len(length_of_evidence_answer)}")
    print(f"max length_of_evidence_answer: {max(length_of_evidence_answer)}")
    print(f"min length_of_evidence_answer: {min(length_of_evidence_answer)}")

def compare_difference(baseline_name1, baseline_name2, dataset_names = ['civic','paper','notice'], model_names = ['gpt4o', 'gpt35', 'gpt4omini']):

    for model_name in model_names:
        for dataset_name in dataset_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
            file_paths = glob.glob(os.path.join(folder_path, '*.json'))
            
            # # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    # print(f"file_path: {file_path}")
                    content = json.load(file)
                    question = content["question"]
                    baseline_type = content["baseline_type"]
                    document_path = content["document_path"]
                    raw_provenance = content["raw_provenance"]
                    evidence = content["evidence"]
                    raw_answer = content["raw_answer"]
                    evidence_answer = content["evidence_answer"]
                    # search_pool = content["search_pool"]
                    # raw_sentences = content["sentences"] # a list of str
                    jaccard_similarity = content["jaccard_similarity"]
                    # if jaccard_similarity <= 0.99:
                    #     continue

                    # cosine_similarity = cosine_similarity(raw_answer, evdience_answer)
                    for rp in raw_provenance:
                        length_of_provenance_sentence.append(get_token_num(rp))
                        # print(length_of_provenance[-1])
                    length_of_provenance.append(get_token_num_for_list(raw_provenance))
                    for e in evidence: # evidence is a list of sentences, sentence is str
                        length_of_evidence_sentence.append(get_token_num(e))
                    # for re in raw_sentences:
                    #     length_of_raw_sentences.append(get_token_num(re))
                    length_of_raw_answer.append(get_token_num(raw_answer))
                    if get_token_num(raw_answer) == 2048:
                        print(f"{file}")
                    length_of_evidence_answer.append(get_token_num(evidence_answer))
                    # print(length_of_provenance[-1])
                    length_of_evidence.append(get_token_num_for_list(evidence))
                    # print(length_of_evidence[-1])
    print("")
    print(f"baseline_name: {baseline_name}")
    print(f"average length_of_provenance: {sum(length_of_provenance)/len(length_of_provenance)}")
    print(f"average length_of_evidence: {sum(length_of_evidence)/len(length_of_evidence)}")
    print(f"average ration_of_evidence_to_provenance: {sum(length_of_evidence) / sum(length_of_provenance)}")
    print(f"average number of evidence sentence: {len(length_of_evidence_sentence)/len(length_of_evidence)}") # len(length_of_evidence) is the number of files
    print(f"average number of raw sentence: {len(length_of_raw_sentences)/len(length_of_evidence)}")
    print(f"average length_of_provenance_chunk: {sum(length_of_provenance_sentence)/len(length_of_provenance_sentence)}")
    print(f"min length_of_provenance_chunk: {min(length_of_provenance_sentence)}")
    print(f"max length_of_provenance_chunk: {max(length_of_provenance_sentence)}")
    print(f"average length_of_evidence_sentence: {sum(length_of_evidence_sentence)/len(length_of_evidence_sentence)}")
    print(f"min length_of_evidence_sentence: {min(length_of_evidence_sentence)}")
    print(f"max length_of_evidence_sentence: {max(length_of_evidence_sentence)}")
    print(f"average length_of_raw_answer: {sum(length_of_raw_answer)/len(length_of_raw_answer)}")
    print(f"max length_of_raw_answer: {max(length_of_raw_answer)}")
    print(f"min length_of_raw_answer: {min(length_of_raw_answer)}")
    print(f"average length_of_evidence_answer: {sum(length_of_evidence_answer)/len(length_of_evidence_answer)}")
    print(f"max length_of_evidence_answer: {max(length_of_evidence_answer)}")
    print(f"min length_of_evidence_answer: {min(length_of_evidence_answer)}")

baseline_names = ['baseline0', 'baseline1_0.4', 'baseline1_0.5', 'baseline1_0.6', 'baseline1_0.7', 'baseline1_0.8', 'baseline2']
for baseline_name in baseline_names:
    calculate_evidence_length(baseline_name=baseline_name, dataset_names=dataset_names, model_names=model_names)
