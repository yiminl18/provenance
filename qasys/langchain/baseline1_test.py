from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path
from query_decompose import query_extractor
import json, os, glob
from indexing import split_docs, store_splits
from langchain.docstore.document import Document
from retrieve_and_generation import generate_from_evidence
from setup_logging import setup_logging, close_logging
from txt2pdf_path import pdf2pdf_path
import logging
from textblob import TextBlob
from itertools import groupby
from pretrain_sentence_splitter import nltk_sent_tokenize_for_list, nltk_sent_tokenize


dataset_name = 'paper'
model_name = 'gpt35'
question_set = paper_q()



def get_extracted_question(question, file_path):
    '''
    Get pre-computed extracted entities given a question
    '''
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = json.load(file)  # 将JSON内容解析为字典
        for question_key, content in contents.items():
            if content[f"question"] == question:
                entities = content["extracted"]
                for entity_key, entity in entities.items():
                    result.append(entity["entity_name"])
                    attributes = entity["attributes"]
                    for attribute_name, attribute_value in attributes.items():
                        result.append(attribute_name)
                        result.append(attribute_value)
    return result

def json_flatten_2list(json_data):
    result = []
    for entity_key, entity in json_data.items():
        try:
            result.append(entity["entity_name"])
        except(KeyError):
            pass
        try:
            attributes = entity["attributes"]
        except(KeyError):
            continue
        for attribute_name, attribute_value in attributes.items():
            result.append(attribute_name)
            result.append(attribute_value)
    result= [x for x in result if x] # filter '' elements
    return result

def convert_baseline(string):
    """
    字符串中的'baseline0'和'baseline1'相互转换

    参数:
    string (str): 原始字符串

    返回:
    str: 修改后的字符串
    """
    if 'baseline0' in string:
        return string.replace('baseline0', 'baseline1')
    elif 'baseline1' in string:
        return string.replace('baseline1', 'baseline0')

def get_token_num(text:str):
    import re
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def get_token_num_for_list(text_list: list):
    token_num = 0
    for text in text_list:
        token_num += get_token_num(text)
    return token_num


# 1. extract each question
# json_to_store = {}
# model_names = ['gpt35', 'gpt4o']
# for model_name in model_names:
#     for i, question in enumerate(civic_q()):
#         extracted_dict = query_exractor(question, model_name=model_name)
#         json_to_store[f"question_{i}"] = {"question": question, "extracted": extracted_dict}

#     with open(f'test/output/provenance/questionset_civic_{model_name}.json', 'w', encoding='utf-8') as f:
#         json.dump(json_to_store, f, ensure_ascii=False, indent=4)
    
# 2. extract each answer, from results of baseline 0
# extract raw_answer in baseline 0, append every key, value pair to a list
# 指定文件夹路径
folder_path = f'test/output/provenance/baseline1/{dataset_name}/{model_name}/labeled_file'
extracted_question_path = f'test/output/provenance/questionset_{dataset_name}_{model_name}.json'


# 获取文件夹内所有JSON文件的路径
file_paths = glob.glob(os.path.join(folder_path, '*.json'))

# logger, file_handler, console_handler, timestamp = setup_logging()
# logging.info(f"run baseline1.py for {dataset_name} with {model_name}")
# logging.info(f"folder_path: {folder_path}")
# logging.info(f"extracted_question_path: {extracted_question_path}")
# logging.info(f"file number: {len(file_paths)}")
# close_logging(logger, [file_handler, console_handler])

# run_info = {
#     "dataset_name": dataset_name,
#     "model_name": model_name,
#     "file_number": len(file_paths),
#     "extracted_question_path": extracted_question_path,
#     "folder_path": folder_path
# }
# with open(f'test/output/logging/experiment/run_info_{timestamp}.json', 'w', encoding='utf-8') as f:
#     json.dump(run_info, f, ensure_ascii=False, indent=4)

# 依次读取每个JSON文件并解析为字典
for file_path in file_paths:
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        node_info = {}
        logger, file_handler, console_handler, timestamp = setup_logging()

        logging.info(f"folder_path: {folder_path}")
        logging.info(f"extracted_question_path: {extracted_question_path}")
        logging.info(f"file_path: {file_path}")

        content_list = json.load(file)  # 将JSON内容解析为字典
        question = content_list[0]["question"]
        document_path = content_list[0]["document_path"]

        for content in content_list:
            extracted_search_list = content["search_pool"]

            answer = content["raw_answer"]
        
        raw_provenance = content["raw_provenance"] # provenance is a list of str
        logging.info(f"question: {question}")
        logging.info(f"answer: {answer}")
        logging.info(f"document_path: {document_path}")
        logging.info(f"raw_provenance: {raw_provenance}")
        logging.info(f"raw_provenance_len: {len(raw_provenance)}")

        logging.info(f"extracted_question_list: {extracted_question_list}")


        logging.info(f"extracted_search_list: {extracted_search_list}")



        # # 3. split raw_provenence sentence by sentence, "\n\n" or "\n" or ". ", to be determined

        # docs =  [Document(page_content=rp, metadata={"source": "local"}) for rp in raw_provenance]
        # all_splits = split_docs(docs = docs, chunk_size=1, separators=["\n\n"])
        # logging.info(f"all_splits: {all_splits}")
        # logging.info(f"all_splits_len: {len(all_splits)}")
        # logging.info(f"all_splits_text: {[split.page_content for split in all_splits]}")

        # sentences = []
        # for split in all_splits:
        #     sentences += sent_tokenize(split.page_content) # input: str, output: list of str

        sentences = []
        # for rp in raw_provenance:
        #     sentences += TextBlob(rp).sentences # sentences is a list of str
        sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)
        
        total_token_num = get_token_num_for_list(sentences)
        all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
        logging.info(f"sentences: {sentences}")
        logging.info(f"sentences_len: {len(sentences)}")
        logging.info(f"all_splits: {all_splits}")
        logging.info(f"all_splits_len: {len(all_splits)}")
        
# 4. embedding list in 2 and all sentences in 3, get the most similar sentence for each key, value pair. We can set a threshold for the similarity score, return those above the threshold. Get evidence
        vector_store = store_splits(all_splits)
        evidence = []
        searched_docs = []
        for extracted_search in extracted_search_list:
            searched_docs+=vector_store.similarity_search_with_score(extracted_search, k=30) # using large k to return all chunks' score, then we can filter by threshold. # return is a list of tuple, (Document, score) 
            logging.info(f"searched_docs: {searched_docs}")
            # logging.info(f"searched_docs: {searched_docs}")   
        
            # for doc in searched_docs:
            #     if doc[1] < 0.3: # doc is a tuple, (Document, score)
            #         evidence.append(doc[0].page_content)
            # evidence = list(set(evidence))

            # logging.info(f"evidence_len: {len(evidence)}")
        vector_store.delete_collection()
        logging.info(f"searched_docs: {searched_docs}")
        # 首先根据data进行排序，以便使用groupby
        sorted_tuples = sorted(searched_docs, key=lambda x: x[0].page_content)
        # 使用groupby对相同的data进行分组，并取每组中score最高的tuple
        unique_tuples = [max(group, key=lambda x: x[1]) for key, group in groupby(sorted_tuples, key=lambda x: x[0])]

        # 按照score从高到低排序
        ranked_tuples = sorted(unique_tuples, key=lambda x: x[1], reverse=True)

        # 从ranked_tuples中提取evidence
        for doc in ranked_tuples:
            if get_token_num_for_list(evidence) < total_token_num * 0.2:
                evidence.append(doc[0].page_content) # evidence is a list of str
                    
        logging.info(f"evidence: {evidence}")
        logging.info(f"evidence_token_num: {get_token_num_for_list(evidence)}")
        logging.info(f"total_token_num: {total_token_num}")



# 5. generate answer from evidence
        evaluation_instruction = ""
        question_index= question_set.index(question)
        if dataset_name == 'paper':
            if question_index == 0 or question_index == 1:
                evaluation_instruction = " Return only a number."
            elif question_index == 3:
                evaluation_instruction = " Return only one word representing the venue."
            elif question_index == 4:
                evaluation_instruction = " Return yes or no."

        if dataset_name == 'notice':
            if question_index == 0:
                evaluation_instruction = " Return only one date."
            if question_index == 2 or question_index == 3 or question_index == 4:
                evaluation_instruction = " Return only one company name."

        evidence_answer = generate_from_evidence(question+evaluation_instruction, evidence)
        logging.info(f"prompt_instruction: {question+evaluation_instruction}")
        logging.info(f"evidence_answer: {evidence_answer}")
        provenance_dict = {
            "model_name": model_name,
            "baseline_type": 1,
            "document_path": document_path,
            "question": question,
            "raw_provenance": raw_provenance,
            "evidence": evidence,
            "raw_answer": answer,
            "evidence_answer": evidence_answer,
            "search_pool": extracted_search_list
        }

        logging.info(f"all_splits: {all_splits}")
        
        # output_filename = convert_baseline(os.path.basename(file_path))
        with open(f'test/output/provenance/baseline1/{dataset_name}/{model_name}/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
        close_logging(logger, [file_handler, console_handler])

# 6. store the results in a json file, same format as baseline 0



