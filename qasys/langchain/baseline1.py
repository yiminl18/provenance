from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path
from query_decompose import query_exractor
import json, os, glob
from indexing import split_docs, store_splits
from langchain.docstore.document import Document
from retrieve_and_generation import generate_from_evidence
from setup_logging import setup_logging, close_logging
from txt2pdf_path import pdf2pdf_path
import logging

dataset_name = 'notice'
model_name = 'gpt4o'

def get_extracted_question(question, file_path):
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
folder_path = f'test/output/provenance/baseline0/{dataset_name}/{model_name}'
extracted_question_path = f'test/output/provenance/questionset_{dataset_name}_{model_name}.json'


# 获取文件夹内所有JSON文件的路径
file_paths = glob.glob(os.path.join(folder_path, '*.json'))

# 依次读取每个JSON文件并解析为字典
for file_path in file_paths:
    # 打开文件并读取内容
    with open(file_path, 'r', encoding='utf-8') as file:
        node_info = {}
        logger, file_handler, console_handler, timestamp = setup_logging()

        logging.info(f"folder_path: {folder_path}")
        logging.info(f"extracted_question_path: {extracted_question_path}")
        logging.info(f"file_path: {file_path}")

        content = json.load(file)  # 将JSON内容解析为字典
        question = content["question"]
        answer = content["raw answer"]
        document_path = content["document path"]
        raw_provenance = content["raw provenance"]
        logging.info(f"question: {question}")
        logging.info(f"answer: {answer}")
        logging.info(f"document_path: {document_path}")
        logging.info(f"raw_provenance: {raw_provenance}")

        extracted_question_list = get_extracted_question(question, extracted_question_path)
        logging.info(f"extracted_question_list: {extracted_question_list}")
        extracted_answer_json = query_exractor(answer, model_name=model_name) # model should be the same as 'extracted_question_path'
        logging.info(f"extracted_answer_list: {extracted_answer_json}")
        extracted_answer_list = json_flatten_2list(extracted_answer_json)
        logging.info(f"extracted_answer_json: {extracted_answer_list}")

        extracted_search_list = extracted_question_list + extracted_answer_list
        logging.info(f"extracted_search_list: {extracted_search_list}")

        docs =  [Document(page_content=rp, metadata={"source": "local"}) for rp in raw_provenance[0]]
# 3. split raw_provenence sentence by sentence, "\n\n" or "\n" or ". ", to be determined
        all_splits = split_docs(docs = docs, chunk_size=1)
        
# 4. embedding list in 2 and all sentences in 3, get the most similar sentence for each key, value pair. We can set a threshold for the similarity score, return those above the threshold. Get evidence
        vector_store = store_splits(all_splits)
        evidence = []
        for extracted_search in extracted_search_list:
            searched_docs = vector_store.similarity_search_with_score(extracted_search, k=20) # using large k to return all chunks' score, then we can filter by threshold
            
            for doc in searched_docs:
                if doc[1] < 0.3:
                    evidence.append(doc[0].page_content)
            evidence = list(set(evidence))

            logging.info(f"evidence_len: {len(evidence)}")
        vector_store.delete_collection()
        evidence = list(set(evidence))
        logging.info(f"evidence: {evidence}")



# 5. generate answer from evidence
        evidence_answer = generate_from_evidence(question, evidence)
        logging.info(f"evidence_answer: {evidence_answer}")
        provenance_dict = {
            "model name": model_name,
            "baseline type": 1,
            "document path": document_path,
            "question": question,
            "raw provenance": raw_provenance,
            "evidence": evidence,
            "raw answer": answer,
            "evidence answer": evidence_answer,
            "extracted elements": extracted_search_list
        }

        logging.info(f"all_splits: {all_splits}")
        
        # output_filename = convert_baseline(os.path.basename(file_path))
        with open(f'test/output/provenance/baseline1/{dataset_name}/{model_name}/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(provenance_dict, f, ensure_ascii=False, indent=4)

# 6. store the results in a json file, same format as baseline 0
"""
{
    "model name": "gpt35",
    "baseline type": 1,
    "document path": "",
    "question": "",
    "raw provenance": [
        ["",
         ]
    ],
    "evidence": ["",
    ],
    "raw answer": ""
    "evidence answer": ""
    "extracted elements": ["",]
}
"""


