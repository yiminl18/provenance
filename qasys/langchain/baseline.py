from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path, get_evaluation_instruction
from query_decompose import query_extractor, json_flatten_2list, answer_extractor
import json, os, glob
from indexing import split_docs, store_splits
from langchain.docstore.document import Document
from setup_logging import setup_logging, close_logging
from txt2pdf_path import pdf2pdf_path
import logging
from textblob import TextBlob
from itertools import groupby
from pretrain_sentence_splitter import nltk_sent_tokenize_for_list, nltk_sent_tokenize
from sequential_util import sort_substrings
from indexing import load_local_txt, load_local_pdf, load_local_pdf_as_one_page, split_docs, store_splits, path_extracted2raw, path_raw2extracted
from retrieve_and_generation import retrieve_and_generation, generate_from_evidence
from evidence_finder import find_evidence
from calculate_str_similarity import jaccard_similarity_word_union_cleaned
import random
from models.gpt_4o import gpt_4o
from models.gpt_35 import gpt_35
from models.gpt_4o_mini import gpt_4o_mini
from models.gpt_4_turbo import gpt_4_turbo
from label_file import append_to_json_file

def convert_set_to_intervals(input_set):
    if not input_set:
        return []
    
    sorted_list = sorted(input_set)
    intervals = []
    start = sorted_list[0]
    end = sorted_list[0]
    
    for i in range(1, len(sorted_list)):
        if sorted_list[i] == end + 1:
            end = sorted_list[i]
        else:
            intervals.append([start, end])
            start = sorted_list[i]
            end = sorted_list[i]
    
    intervals.append([start, end])
    return intervals

def convert_intervals_to_set(intervals: list[list[int]]):
    result_set = set()
    
    for interval in intervals:
        start, end = interval
        result_set.update(range(start, end + 1))
    
    return result_set

def try_interval(sentences: list[str], interval: list[int], intervals_to_be_removed: list[list[int]], question: str, evaluation_instruction: str, raw_answer: str, model_name: str):
    intervals_to_be_removed = intervals_to_be_removed.copy()
    intervals_to_be_removed.append(interval)
    temp_intervals_to_be_removed = intervals_to_be_removed
    temp_sentences = remove_elements_by_intervals(sentences, temp_intervals_to_be_removed)
    llm_call = generate_from_evidence(question+evaluation_instruction, temp_sentences, model_name)
    jaccard_similarity = jaccard_similarity_word_union_cleaned(raw_answer, llm_call["content"])
    threshold = 0.99
    influence = True if jaccard_similarity < threshold else False
    return {
        "influence": influence, # boolean
        "evidence": temp_sentences, # list[str]
        "evidence_answer": llm_call["content"], # str
        "jaccard_similarity": jaccard_similarity,
        "cost": llm_call["cost"],
    }

def interval_all_len_1(interval_list: list[list[int]]):
    for interval in interval_list:
        if interval[0] == interval[1]:
            continue;
        else:
            return False
    return True

def partition_intervals(intervals: list[list[int]]):
    result = []
    
    for interval in intervals:
        start, end = interval
        if start < end:
            mid = (start + end) // 2
            result.append([start, mid])
            result.append([mid + 1, end])
        else:
            result.append(interval)
    
    return result

def convert_set_to_intervals_without_merging(result_set, original_intervals):
    if not result_set:
        return []
    
    intervals = []
    for original_interval in original_intervals:
        start, end = original_interval
        current_interval = []
        for i in range(start, end + 1):
            if i in result_set:
                current_interval.append(i)
            else:
                if current_interval:
                    intervals.append([current_interval[0], current_interval[-1]])
                    current_interval = []
        if current_interval:
            intervals.append([current_interval[0], current_interval[-1]])
    
    return intervals

def remove_intervals(full_intervals: list[list[int]], remove_intervals: list[list[int]]):
    full_set = convert_intervals_to_set(full_intervals)
    remove_set = convert_intervals_to_set(remove_intervals)
    result_set = full_set - remove_set
    result_intervals = convert_set_to_intervals_without_merging(result_set, full_intervals)
    return result_intervals

def remove_elements_by_intervals(sentences: list[str], remove_intervals: list[list[int]]):
    remove_set = convert_intervals_to_set(remove_intervals)
    remove_indexes = list(remove_set)
    return remove_elements_by_indexes(sentences, remove_indexes)

def binary_search_sentences(sentences: list[str], question:str, evaluation_instruction:str, raw_answer:str, model_name: str):
    iterate_list = [[0, len(sentences)-1]]
    updated_iterate_list = iterate_list
    intervals_to_be_removed = []
    cost_list = []
    final_try_result = {}
    while True:
        print("-"*10)
        temp_intervals_to_be_removed = []
        for interval in updated_iterate_list:
            print("testing interval: ", interval)
            try_result = try_interval(sentences, interval, intervals_to_be_removed, question, evaluation_instruction, raw_answer, model_name)
            cost_list.append(try_result["cost"])
            if not try_result["influence"]: # no influence, remove it
                final_try_result = try_result
                intervals_to_be_removed.append(interval)
                temp_intervals_to_be_removed.append(interval)
                print("no influence, intervals_to_be_removed: ", intervals_to_be_removed)
            else:
                print("have influence")
                continue
        # if each interval of iterate_list is of len(1), return
        iterate_set = convert_intervals_to_set(iterate_list)
        intervals_to_be_removed_set = convert_intervals_to_set(intervals_to_be_removed)
        if interval_all_len_1(updated_iterate_list) or iterate_set == intervals_to_be_removed_set:
            print("binary ends, intervals_to_be_removed: ", intervals_to_be_removed)
            if not intervals_to_be_removed: # no deletion
                final_try_result = {
                    "influence": True, # boolean
                    "evidence": sentences, # list[str]
                    "evidence_answer": raw_answer, # str
                    "jaccard_similarity": 1,
                    "cost": 0,
                }
            return final_try_result, cost_list, intervals_to_be_removed
        # else partition iterate_list and continue
        else:
            updated_iterate_list = remove_intervals(updated_iterate_list, temp_intervals_to_be_removed)
            print("after this run's test, after removal: ", updated_iterate_list)
            logging.info("after this run's test, after removal: ", updated_iterate_list)
            updated_iterate_list = partition_intervals(updated_iterate_list)
            print("after partition: ", updated_iterate_list)
            logging.info("after partition: ", updated_iterate_list)

def greedy_search_sentences(sentences: list[str], question:str, evaluation_instruction:str, raw_answer:str, model_name: str, threshold=0.99):
    index_to_delete = []
    evidence_answer = ""
    jaccard_similarity = 0
    cost_list = []
    
    for i in range(len(sentences)):
        temp_index_to_delete = index_to_delete.copy()
        temp_index_to_delete.append(i)
        temp_sentence = remove_elements_by_indexes(sentences, temp_index_to_delete)
        
        llm_call = generate_from_evidence(question+evaluation_instruction, temp_sentence, model_name)
        temp_evidence_answer = llm_call["content"]
        cost_list.append(llm_call["cost"])
        
        temp_jaccard_similarity = jaccard_similarity_word_union_cleaned(raw_answer, temp_evidence_answer)
        
        if temp_jaccard_similarity > threshold: # no influence on the result
            index_to_delete = temp_index_to_delete
            evidence_answer = temp_evidence_answer
            jaccard_similarity = temp_jaccard_similarity
    
    if not evidence_answer: # every sentence has influence, no deletion
        evidence_answer = raw_answer
        jaccard_similarity = 1
    
    evidence = remove_elements_by_indexes(sentences, index_to_delete)
    
    return {
        "evidence": evidence,
        "evidence_answer": evidence_answer,
        "jaccard_similarity": jaccard_similarity,
    }, cost_list, index_to_delete

def reverse_search_sentences_with_early_stop(sentences: list[str], question:str, evaluation_instruction:str, raw_answer:str, model_name: str, threshold=0.99):
    # get the index list by relevance
    all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
    vector_store = store_splits(all_splits)
    ranked_documents = vector_store.similarity_search(question, k=99999)
    vector_store.delete_collection()
    ranked_sentences = [doc.page_content for doc in ranked_documents] # is from most relevanct to least relevant
    # get the index of ranked_sentences in sentences
    relevance_index = [] # is from most relevanct to least relevant
    for sen in ranked_sentences:
        relevance_index.append(sentences.index(sen))
    reverse_index = relevance_index[::-1]

    # try to remove each sentence from least relevant to most relevant
    index_to_delete = []
    evidence_answer = ""
    jaccard_similarity = 0
    cost_list = []
    continuous_deletion = 0
    for i in reverse_index:
        continuous_deletion += 1
        temp_index_to_delete = index_to_delete.copy()
        temp_index_to_delete.append(i)
        temp_sentence = remove_elements_by_indexes(sentences, temp_index_to_delete)
        
        llm_call = generate_from_evidence(question+evaluation_instruction, temp_sentence, model_name)
        temp_evidence_answer = llm_call["content"]
        cost_list.append(llm_call["cost"])
        
        temp_jaccard_similarity = jaccard_similarity_word_union_cleaned(raw_answer, temp_evidence_answer)
        
        if temp_jaccard_similarity > threshold: # no influence on the result
            index_to_delete = temp_index_to_delete
            evidence_answer = temp_evidence_answer
            jaccard_similarity = temp_jaccard_similarity
            continuous_deletion = 0
        
        # early stop
        if continuous_deletion > 5:
            break

    if not evidence_answer:
        evidence_answer = raw_answer
        jaccard_similarity = 1

    evidence = remove_elements_by_indexes(sentences, index_to_delete)
    
    return {
        "evidence": evidence,
        "evidence_answer": evidence_answer,
        "jaccard_similarity": jaccard_similarity,
    }, cost_list, index_to_delete
    


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

def remove_elements_by_indexes(input_list:list, input_index:list):
    my_list = input_list.copy()
    indexes_to_remove = input_index.copy()
    if indexes_to_remove == []:
        return my_list
    # 将索引列表排序并反转
    indexes_to_remove.sort(reverse=True)
    
    # 删除相应索引位置的元素
    for index in indexes_to_remove:
        del my_list[index]
    
    return my_list

def rag_dataset_generation(dataset_name: str, question_set:list[str], document_set:list[str], model_name='gpt4turbo'):
    gpt_4o.call_count = 0
    gpt_35.call_count = 0
    gpt_4o_mini.call_count = 0
    gpt_4_turbo.call_count = 0
    cost_list = []
    for document_index, document_path in enumerate(document_set):
        # step0: load sample question and folder path
        docs = load_local_txt(path_raw2extracted(document_path))

        # step1: indexing
        all_splits = split_docs(docs, chunk_size=1000, chunk_overlap=0, add_start_index=True)
        vectorstore = store_splits(all_splits, "rag")
        # each document have one vector store for retrieval
        

        for question_index, question in enumerate(question_set):
            logger, file_handler, console_handler, timestamp = setup_logging()
            logging.info(f"question: {question}")

            evaluation_instruction = get_evaluation_instruction(question, question_set, dataset_name)
            logging.info(f"evaluation_instruction: {evaluation_instruction}")

            llm_call, sub_retrieved_docs, chunk_index, rag_prompt = retrieve_and_generation(question, vectorstore, 5, evaluation_instruction, model_name)
            raw_answer = llm_call["content"]
            cost_list.append(llm_call["cost"])
            logging.info(f"rag_prompt: {rag_prompt}")

            provenance = ([doc.page_content for doc in sub_retrieved_docs]) # retrieved_docs is a list of list of strings

            logging.info(f"Using following chunks:") # print each sub-answer
            logging.info(f"chunk_index: {chunk_index}")
            k = 0 # print top k retrieved docs
            for doc in sub_retrieved_docs:
                    k += 1
                    logging.info(f"top{k}\n retrieved_docs:\n {doc.metadata}\n {doc.page_content}\n {'-'*10}") # print each retrieved doc

            dataset_dict = {
                "model_name": "gpt4turbo",
                "document_path": document_path,
                "question": question,
                "evaluation_instruction": evaluation_instruction,
                "provenance": provenance,
                "raw_answer": raw_answer,
                "question_id": question_index,
                "document_id": document_index,
                "dataset": dataset_name,
                "logging_file": f"test/output/logging/logging_{timestamp}.log"
                }
            with open(f'test/output/rag_dataset/{dataset_name}/{dataset_name}_{model_name}_q{question_index}_d{document_index}.json', 'w', encoding='utf-8') as f:
                json.dump(dataset_dict, f, ensure_ascii=False, indent=4)

            close_logging(logger, [file_handler, console_handler])
        vectorstore.delete_collection()
    cost_dict = {
        "baseline_name": "rag_dataset_generation",
        "dataset_name": dataset_name,
        "model_names": "gpt4turbo",
        "cost": sum(cost_list),
        "run_time": len(cost_list),
        "average_cost": sum(cost_list)/len(cost_list),
        "gpt35_call_count": gpt_35.call_count,
        "gpt4o_call_count": gpt_4o.call_count,
        "gpt4o_mini_call_count": gpt_4o_mini.call_count,
        "gpt4_turbo_call_count": gpt_4_turbo.call_count,
    }
    append_to_json_file(f'test/output/rag_dataset/cost_count.json', cost_dict)
            


def baseline0(dataset_name:str, model_names:list[str], baseline_name: str):

    node_info = {}

    for model_name in model_names:
        gpt_4o.call_count = 0
        gpt_35.call_count = 0
        gpt_4o_mini.call_count = 0
        gpt_4_turbo.call_count = 0
        cost_list = []

        folder_path = f'test/output/rag_dataset/{dataset_name}'

        # 获取文件夹内所有JSON文件的路径
        file_paths = glob.glob(os.path.join(folder_path, '*.json'))

        logger, file_handler, console_handler, timestamp = setup_logging()
        logging.info(f"run baseline2.py for {dataset_name} with {model_name}")
        logging.info(f"folder_path: {folder_path}")
        logging.info(f"file number: {len(file_paths)}")
        close_logging(logger, [file_handler, console_handler])

        # 依次读取每个JSON文件并解析为字典
        for file_index, file_path in enumerate(file_paths):
            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                question = content["question"]
                provenance = content["provenance"] # list[str]
                raw_answer = content["raw_answer"]
                question_index = content["question_id"]
                document_path = content["document_path"]
                document_index = content["document_id"]
                evaluation_instruction = content["evaluation_instruction"]

                print(f"file_index: {file_index}")
                print(f"q{question_index}_d{document_index}")

                provenance_text = " ".join(provenance)
                evidence, unfiltered_evidence, find_evidence_response = find_evidence(question + evaluation_instruction, raw_answer, provenance_text, model_name = model_name) # w/o filter, first two returned ele are the same
                cost_list.append(find_evidence_response["cost"])

                llm_call = generate_from_evidence(question+evaluation_instruction, evidence)
                evidence_answer = llm_call["content"]
                cost_list.append(llm_call["cost"])

                provenance_dict = {
                    "dataset": dataset_name,
                    "model_name": model_name,
                    "baseline_name": baseline_name,
                    "question": question,
                    "provenance": provenance,
                    "evidence": evidence,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "jaccard_similarity": jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer),
                    "document_path": document_path,
                    "evaluation_instruction": evaluation_instruction,
                    "question_id": question_index,
                    "document_id": document_index,
                    "unfiltered_evidence": unfiltered_evidence,
                    "logging_file": f"test/output/logging/logging_{timestamp}.log"
                }

            close_logging(logger, [file_handler, console_handler])

            # with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', 'w', encoding='utf-8') as f:
            #     json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
            append_to_json_file(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', provenance_dict)
        
        cost_dict = {
            "baseline_name": baseline_name,
            "dataset_name": dataset_name,
            "model_name": model_name,
            "cost": sum(cost_list),
            "run_time": len(cost_list),
            "average_cost": sum(cost_list)/len(cost_list),
            "gpt35_call_count": gpt_35.call_count,
            "gpt4o_call_count": gpt_4o.call_count,
            "gpt4o_mini_call_count": gpt_4o_mini.call_count,
            "gpt4_turbo_call_count": gpt_4_turbo.call_count,
        }
        append_to_json_file(f'test/output/provenance/{baseline_name}/cost_count.json', cost_dict)
    

def baseline1(dataset_name:str, model_names:list[str], threshold = 0.5, baseline_name="baseline1"):


    for model_name in model_names:
        gpt_4o.call_count = 0
        gpt_35.call_count = 0
        gpt_4o_mini.call_count = 0
        gpt_4_turbo.call_count = 0
        cost_list = []
        # baseline1 uses generated data from baseline0
        # 2. extract each answer, from results of baseline 0
        # extract raw_answer in baseline 0, append every key, value pair to a list
        # 指定文件夹路径
        folder_path = f'test/output/rag_dataset/{dataset_name}'
        # extracted_question_path = f'test/output/provenance/questionset_{dataset_name}_{model_name}.json'


        # 获取文件夹内所有JSON文件的路径
        file_paths = glob.glob(os.path.join(folder_path, '*.json'))

        logger, file_handler, console_handler, timestamp = setup_logging()
        logging.info(f"run baseline1.py for {dataset_name} with {model_name}")
        logging.info(f"folder_path: {folder_path}")
        # logging.info(f"extracted_question_path: {extracted_question_path}")
        logging.info(f"file number: {len(file_paths)}")
        close_logging(logger, [file_handler, console_handler])

        run_info = {
            "dataset_name": dataset_name,
            "model_name": model_name,
            "file_number": len(file_paths),
            # "extracted_question_path": extracted_question_path,
            "folder_path": folder_path,
            "threshold": threshold,
        }
        with open(f'test/output/logging/experiment/run_info_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(run_info, f, ensure_ascii=False, indent=4)

        # 依次读取每个JSON文件并解析为字典
        for file_path in file_paths:
            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                node_info = {}
                logger, file_handler, console_handler, timestamp = setup_logging()

                logging.info(f"folder_path: {folder_path}")
                # logging.info(f"extracted_question_path: {extracted_question_path}")
                logging.info(f"file_path: {file_path}")

                content = json.load(file)  # 将JSON内容解析为字典
                question = content["question"]
                question_index = content["question_id"]
                raw_answer = content["raw_answer"]
                document_path = content["document_path"]
                document_index = content["document_id"]
                raw_provenance = content["provenance"] # provenance is a list of str
                evaluation_instruction = content["evaluation_instruction"]

                logging.info(f"question: {question}")
                logging.info(f"answer: {raw_answer}")
                logging.info(f"document_path: {document_path}")
                logging.info(f"raw_provenance: {raw_provenance}")
                logging.info(f"raw_provenance_len: {len(raw_provenance)}")

                # extracted_question_list = get_extracted_question(question, extracted_question_path)
                extracted_question_list = [question]
                logging.info(f"extracted_question_list: {extracted_question_list}")
                llm_call = answer_extractor(raw_answer, model_name=model_name) # model should be the same as 'extracted_question_path'
                print("llm_call", llm_call)
                extracted_answer_list = llm_call["content"]
                cost_list.append(llm_call["cost"])
                logging.info(f"extracted_answer_list: {extracted_answer_list}")

                extracted_search_list = extracted_question_list + extracted_answer_list
                extracted_search_list = list(set(extracted_search_list))
                extracted_search_list = [x for x in extracted_search_list if x]
                logging.info(f"extracted_search_list: {extracted_search_list}")


                sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)
                
                total_token_num = get_token_num_for_list(sentences)
                all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
                logging.info(f"sentences: {sentences}")
                logging.info(f"sentences_len: {len(sentences)}")
                logging.info(f"all_splits: {all_splits}")
                logging.info(f"all_splits_len: {len(all_splits)}")
                
        # 4. embedding list in 2 and all sentences in 3, get the most similar sentence for each key, value pair. We can set a threshold for the similarity score, return those above the threshold. Get evidence
                evidence = []
                unsorted_unfiltered_evidence_with_index = []
                unsorted_evidence_with_index = []
                less_similar_evidence_with_index = []
                searched_docs = []

                vector_store = store_splits(all_splits, "baseline1")
                for list_index, extracted_search in enumerate(extracted_search_list):
                    searched_docs.append(vector_store.similarity_search_with_score(extracted_search, k=30)) # using large k to return all chunks' score, then we can filter by threshold. # return is a list of tuple, (Document, score) # lower score more similar
                    # logging.info(f"searched_docs: {searched_docs}")   
                
                    # for doc in searched_docs:
                    #     if doc[1] < 0.3: # doc is a tuple, (Document, score)
                    #         evidence.append(doc[0].page_content)
                    # evidence = list(set(evidence))

                    # logging.info(f"evidence_len: {len(evidence)}")
                vector_store.delete_collection()

                logging.info(f"searched_docs: {searched_docs}")

                # cosine distance to cosine similarity
                searched_docs = [[(doc[0], 0+doc[1]) for doc in docs] for docs in searched_docs]

                # bfs style
                # 从每个list中取出score最高的tuple，放入evidence中，直到evidence中的token数量超过总token数量的20%
                for i in range(len(searched_docs[0])): # i is the index of top i in each list element
                    if get_token_num_for_list(evidence) < total_token_num * 0.2:
                    # if True: # get all evidence astisfies the threshold
                        for j in range(len(searched_docs)): # j is the index of search_pool list
                            if searched_docs[j][i][0].page_content in evidence:
                                continue
                            elif searched_docs[j][i][1] > threshold: # filter out less similar ones:
                                less_similar_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                                unsorted_unfiltered_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                                continue
                            else:
                                unsorted_unfiltered_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                                evidence.append(searched_docs[j][i][0].page_content)
                                unsorted_evidence_with_index.append([searched_docs[j][i][0].page_content, j, searched_docs[j][i][1]])
                    else:
                        break
                
                evidence = sort_substrings(raw_provenance, evidence)
                logging.info(f"evidence: {evidence}")
                searched_docs_with_score = [[(doc[0].page_content, doc[1]) for doc in docs] for docs in searched_docs ]
                logging.info(f"searched_docs_with_score: {searched_docs_with_score}")
                sorted_data_with_score = [[(doc[0].page_content, doc[1]) for doc in docs] for docs in searched_docs ]
                            
                logging.info(f"evidence_token_num: {get_token_num_for_list(evidence)}")
                logging.info(f"total_token_num: {total_token_num}")



        # 5. generate answer from evidence

                llm_call = generate_from_evidence(question+evaluation_instruction, evidence, model_name)
                evidence_answer = llm_call["content"]
                cost_list.append(llm_call["cost"])
                logging.info(f"prompt_instruction: {question+evaluation_instruction}")
                logging.info(f"evidence_answer: {evidence_answer}")

                provenance_dict = {
                    "dataset": dataset_name,
                    "model_name": model_name,
                    "baseline_name": baseline_name,
                    "question": question,
                    "provenance": raw_provenance,
                    "evidence": evidence,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "jaccard_similarity": jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer),
                    "search_pool": extracted_search_list,
                    "document_path": document_path,
                    "evaluation_instruction": evaluation_instruction,
                    "question_id": question_index,
                    "document_id": document_index,
                    "logging_file": f"test/output/logging/logging_{timestamp}.log",
                    "unsorted_evidence": unsorted_evidence_with_index,
                    "less_similar_evidence": less_similar_evidence_with_index,
                    "unsorted_unfiltered_evidence": unsorted_unfiltered_evidence_with_index
                }

                logging_dict = {
                    "question": question,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "evidence_token_num": get_token_num_for_list(evidence),
                    "total_token_num": total_token_num,
                    "extracted_search_list": extracted_search_list,
                    "searched_docs": searched_docs_with_score,
                    "sorted_data": sorted_data_with_score,
                    "evidence": evidence,
                    "unsorted_evidence": unsorted_evidence_with_index,
                    "less_similar_evidence": less_similar_evidence_with_index,
                    "unsorted_unfiltered_evidence": unsorted_unfiltered_evidence_with_index
                }

                logging.info(f"all_splits: {all_splits}")
                
                # output_filename = convert_baseline(os.path.basename(file_path))
                # with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', 'w', encoding='utf-8') as f:
                #     json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
                append_to_json_file(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', provenance_dict)
                with open(f'test/output/logging/logging_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(logging_dict, f, ensure_ascii=False, indent=4)
                close_logging(logger, [file_handler, console_handler])
        cost_dict = {
            "baseline_name": baseline_name,
            "dataset_name": dataset_name,
            "model_name": model_name,
            "cost": sum(cost_list),
            "run_time": len(cost_list),
            "average_cost": sum(cost_list)/len(cost_list),
            "gpt35_call_count": gpt_35.call_count,
            "gpt4o_call_count": gpt_4o.call_count,
            "gpt4o_mini_call_count": gpt_4o_mini.call_count,
            "gpt4_turbo_call_count": gpt_4_turbo.call_count,
        }
        append_to_json_file(f'test/output/provenance/{baseline_name}/cost_count.json', cost_dict)



def baseline2_greedy_search(dataset_name: str, model_names:list[str], threshold = 0.99, baseline_name="baseline2_greedy"):
    return linear_search(dataset_name, model_names, threshold, baseline_name, greedy_search_sentences)

def linear_search(dataset_name: str, model_names:list[str], threshold: int, baseline_name: str, search_function: callable):
    # baseline1 uses generated data from baseline0
    # 2. extract each answer, from results of baseline 0
    # extract raw_answer in baseline 0, append every key, value pair to a list
    # 指定文件夹路径
    for model_name in model_names:
        gpt35_total_count = 0
        gpt4o_total_count = 0
        gpt4o_mini_total_count = 0
        gpt4_turbo_total_count = 0
        cost_list = []
        folder_path = f'test/output/rag_dataset/{dataset_name}'


        # 获取文件夹内所有JSON文件的路径
        file_paths = glob.glob(os.path.join(folder_path, '*.json'))

        logger, file_handler, console_handler, timestamp = setup_logging()
        logging.info(f"run baseline2.py for {dataset_name} with {model_name}")
        logging.info(f"folder_path: {folder_path}")
        logging.info(f"file number: {len(file_paths)}")
        close_logging(logger, [file_handler, console_handler])

        run_info = {
            "baseline_name": baseline_name,
            "dataset_name": dataset_name,
            "model_name": model_name,
            "file_number": len(file_paths),
            "folder_path": folder_path
        }
        with open(f'test/output/logging/experiment/run_info_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(run_info, f, ensure_ascii=False, indent=4)

        # 依次读取每个JSON文件并解析为字典
        for file_path in file_paths:
            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                gpt_4o.call_count = 0
                gpt_35.call_count = 0
                gpt_4o_mini.call_count = 0
                gpt_4_turbo.call_count = 0
                node_info = {}
                logger, file_handler, console_handler, timestamp = setup_logging()

                logging.info(f"folder_path: {folder_path}")
                logging.info(f"file_path: {file_path}")

                content = json.load(file)  # 将JSON内容解析为字典
                question = content["question"]
                raw_answer = content["raw_answer"]
                document_path = content["document_path"]
                raw_provenance = content["provenance"] # provenance is a list of str
                question_index = content["question_id"]
                document_index = content["document_id"]
                evaluation_instruction = content["evaluation_instruction"]
                logging.info(f"question: {question}")
                logging.info(f"answer: {raw_answer}")
                logging.info(f"document_path: {document_path}")
                logging.info(f"raw_provenance: {raw_provenance}")
                logging.info(f"raw_provenance_len: {len(raw_provenance)}")


                sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)
                
                total_token_num = get_token_num_for_list(sentences)

                logging.info(f"evaluation_instruction: {evaluation_instruction}")
                
                result, cost, index_to_delete = search_function(sentences, question, evaluation_instruction, raw_answer, model_name, threshold)
                # return {"evidence": evidence,"evidence_answer": evidence_answer,"jaccard_similarity": jaccard_similarity,}, cost_list, index_to_delete
                evidence = result["evidence"]
                evidence_answer = result["evidence_answer"]
                jaccard_similarity = result["jaccard_similarity"]
                cost_list.extend(cost)

                logging.info(f"evidence: {evidence}")
                logging.info(f"sentences: {sentences}")
                logging.info(f"sentences_len: {len(sentences)}")
                logging.info(f"evidence_token_num: {get_token_num_for_list(evidence)}")
                logging.info(f"total_token_num: {total_token_num}")
                logging.info(f"prompt_instruction: {question+evaluation_instruction}")
                logging.info(f"evidence_answer: {evidence_answer}")

                provenance_dict = {
                    "dataset": dataset_name,
                    "model_name": model_name,
                    "baseline_name": baseline_name,
                    "question": question,
                    "provenance": raw_provenance,
                    "evidence": evidence,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "jaccard_similarity": jaccard_similarity,
                    "index_to_delete": index_to_delete,
                    "cost": sum(cost),
                    "gpt35_call_count": gpt_35.call_count,
                    "gpt4o_call_count": gpt_4o.call_count,
                    "gpt4o_mini_call_count": gpt_4o_mini.call_count,
                    "gpt4_turbo_call_count": gpt_4_turbo.call_count,
                    "document_path": document_path,
                    "evaluation_instruction": evaluation_instruction,
                    "question_id": question_index,
                    "document_id": document_index,
                    "logging_file": f"test/output/logging/logging_{timestamp}.log",
                    "sentences": sentences
                }
                gpt35_total_count += gpt_35.call_count
                gpt4o_total_count += gpt_4o.call_count
                gpt4o_mini_total_count += gpt_4o_mini.call_count
                gpt4_turbo_total_count += gpt_4_turbo.call_count

                logging_dict = {
                    "question": question,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "evidence_token_num": get_token_num_for_list(evidence),
                    "total_token_num": total_token_num,
                    "evidence": evidence,
                }
                
                # output_filename = convert_baseline(os.path.basename(file_path))
                # with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', 'w', encoding='utf-8') as f:
                #     json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
                append_to_json_file(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', provenance_dict)
                with open(f'test/output/logging/logging_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(logging_dict, f, ensure_ascii=False, indent=4)
                close_logging(logger, [file_handler, console_handler])
        cost_dict = {
        "baseline_name": baseline_name,
        "dataset_name": dataset_name,
        "model_names": model_name,
        "cost": sum(cost_list),
        "run_time": len(cost_list),
        "average_cost": sum(cost_list)/len(cost_list), 
        "gpt35_call_count": gpt35_total_count,
        "gpt4o_call_count": gpt4o_total_count,
        "gpt4o_mini_call_count": gpt4o_mini_total_count,
        "gpt4_turbo_call_count": gpt4_turbo_total_count,
        }
        append_to_json_file(f'test/output/provenance/{baseline_name}/cost_count.json', cost_dict)

def baseline2_binary_search(dataset_name: str, model_names:list[str], threshold = 0.99, baseline_name="baseline2_binary"):
    # baseline1 uses generated data from baseline0
    # 2. extract each answer, from results of baseline 0
    # extract raw_answer in baseline 0, append every key, value pair to a list
    # 指定文件夹路径
    for model_name in model_names:
        gpt_4o.call_count = 0
        gpt_35.call_count = 0
        gpt_4o_mini.call_count = 0
        gpt_4_turbo.call_count = 0
        cost_list = []
        folder_path = f'test/output/rag_dataset/{dataset_name}'


        # 获取文件夹内所有JSON文件的路径
        file_paths = glob.glob(os.path.join(folder_path, '*.json'))

        logger, file_handler, console_handler, timestamp = setup_logging()
        logging.info(f"run baseline2.py for {dataset_name} with {model_name}")
        logging.info(f"folder_path: {folder_path}")
        logging.info(f"file number: {len(file_paths)}")
        close_logging(logger, [file_handler, console_handler])

        run_info = {
            "baseline_name": baseline_name,
            "dataset_name": dataset_name,
            "model_name": model_name,
            "file_number": len(file_paths),
            "folder_path": folder_path
        }
        with open(f'test/output/logging/experiment/run_info_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(run_info, f, ensure_ascii=False, indent=4)

        # 依次读取每个JSON文件并解析为字典
        for file_path in file_paths:
            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                node_info = {}
                logger, file_handler, console_handler, timestamp = setup_logging()

                logging.info(f"folder_path: {folder_path}")
                logging.info(f"file_path: {file_path}")

                content = json.load(file)  # 将JSON内容解析为字典
                question = content["question"]
                raw_answer = content["raw_answer"]
                document_path = content["document_path"]
                question_index = content["question_id"]
                document_index = content["document_id"]
                raw_provenance = content["provenance"] # provenance is a list of str
                evaluation_instruction = content["evaluation_instruction"]
                logging.info(f"question: {question}")
                logging.info(f"answer: {raw_answer}")
                logging.info(f"document_path: {document_path}")
                logging.info(f"raw_provenance: {raw_provenance}")
                logging.info(f"raw_provenance_len: {len(raw_provenance)}")


                sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)
                
                total_token_num = get_token_num_for_list(sentences)


                # random.shuffle(iterate_list) # random initializaion
                logging.info(f"evaluation_instruction: {evaluation_instruction}")

                binary_result, cost_list_to_plus, intervals_to_be_removed = binary_search_sentences(sentences, question, evaluation_instruction, raw_answer, model_name)
                cost_list += cost_list_to_plus
                evidence = binary_result["evidence"]
                jaccard_similarity = binary_result["jaccard_similarity"]
                evidence_answer = binary_result["evidence_answer"]
                index_to_delete = list(convert_intervals_to_set(intervals_to_be_removed))

                if not index_to_delete: # empty
                    evidence = raw_provenance
                    evidence_answer = raw_answer
                    jaccard_similarity = 1

                
                
                logging.info(f"evidence: {evidence}")


                logging.info(f"sentences: {sentences}")
                logging.info(f"sentences_len: {len(sentences)}")
                
                
                
                logging.info(f"evidence_token_num: {get_token_num_for_list(evidence)}")
                logging.info(f"total_token_num: {total_token_num}")



        # 5. generate answer from evidence
                



                logging.info(f"prompt_instruction: {question+evaluation_instruction}")
                logging.info(f"evidence_answer: {evidence_answer}")
                provenance_dict = {
                    "dataset": dataset_name,
                    "model_name": model_name,
                    "baseline_name": baseline_name,
                    "question": question,
                    "provenance": raw_provenance,
                    "evidence": evidence,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "jaccard_similarity": jaccard_similarity,
                    "index_to_delete": index_to_delete,
                    "document_path": document_path,
                    "evaluation_instruction": evaluation_instruction,
                    "question_id": question_index,
                    "document_id": document_index,
                    "logging_file": f"test/output/logging/logging_{timestamp}.log",
                    "sentences": sentences
                }

                logging_dict = {
                    "question": question,
                    "raw_answer": raw_answer,
                    "evidence_answer": evidence_answer,
                    "evidence_token_num": get_token_num_for_list(evidence),
                    "total_token_num": total_token_num,
                    "evidence": evidence,
                }
                
                # output_filename = convert_baseline(os.path.basename(file_path))
                # with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', 'w', encoding='utf-8') as f:
                #     json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
                append_to_json_file(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', provenance_dict)
                with open(f'test/output/logging/logging_{timestamp}.json', 'w', encoding='utf-8') as f:
                    json.dump(logging_dict, f, ensure_ascii=False, indent=4)
                close_logging(logger, [file_handler, console_handler])
        cost_dict = {
        "baseline_name": baseline_name,
        "dataset_name": dataset_name,
        "model_names": model_name,
        "cost": sum(cost_list),
        "run_time": len(cost_list),
        "average_cost": sum(cost_list)/len(cost_list), 
        "gpt35_call_count": gpt_35.call_count,
        "gpt4o_call_count": gpt_4o.call_count,
        "gpt4o_mini_call_count": gpt_4o_mini.call_count,
        "gpt4_turbo_call_count": gpt_4_turbo.call_count,
        }
        append_to_json_file(f'test/output/provenance/{baseline_name}/cost_count.json', cost_dict)
        # with open(f'test/output/provenance/{baseline_name}/{dataset_name}/cost_count.json', 'w', encoding='utf-8') as f:
        #     json.dump(cost_dict, f, ensure_ascii=False, indent=4)

def baseline3_reverse_search(dataset_name: str, model_names:list[str], threshold = 0.99, baseline_name="baseline2_greedy"):
    return linear_search(dataset_name, model_names, threshold, baseline_name, reverse_search_sentences_with_early_stop)