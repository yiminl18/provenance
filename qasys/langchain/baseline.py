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

def baseline0(dataset_name:str, model_names:list[str], question_set:list[str], document_path:str):
    node_info = {}
    
    # step0: load sample question and folder path
    docs = load_local_txt(path_raw2extracted(document_path))

    # step1: indexing
    all_splits = split_docs(docs, chunk_size=1000, chunk_overlap=0, add_start_index=True)
    vectorstore = store_splits(all_splits, "baseline0")

    

    for question_index, question in enumerate(question_set):
        logger, file_handler, console_handler, timestamp = setup_logging()
        logging.info(f"folder_path: {document_path}")
        logging.info(f"question: {question}")

        # step3: retrieve and generation for each question

        evaluation_instruction = get_evaluation_instruction(question, question_set, dataset_name)
        logging.info(f"evaluation_instruction: {evaluation_instruction}")

        raw_answer, sub_retrieved_docs, chunk_index, rag_prompt = retrieve_and_generation(question, vectorstore, k = 5, evaluation_instruction = evaluation_instruction)
        logging.info(f"rag_prompt: {rag_prompt}")
        print(f"rag_prompt: {rag_prompt}")

        # record
        # retrieved_docs = [] # index for sub_answer and retrieved_docs should be the same
        provenance = ([doc.page_content for doc in sub_retrieved_docs]) # retrieved_docs is a list of list of strings

        # sentences = nltk_sent_tokenize_for_list(provenance, 10)
        # total_token_num = get_token_num_for_list(sentences)
        # provenance_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
        # provenance_vectorstore = store_splits(provenance_splits, "baseline1")

        logging.info(f"Using following chunks:") # print each sub-answer
        logging.info(f"chunk_index: {chunk_index}")
        k = 0 # print top k retrieved docs
        for doc in sub_retrieved_docs:
                k += 1
                logging.info(f"top{k}\n retrieved_docs:\n {doc.metadata}\n {doc.page_content}\n {'-'*10}") # print each retrieved doc

        # step4: evidence finding
        evidence = []
        evidence_unfiltered = []

        for model_name in model_names:
            for chunk_index, chunk in enumerate(provenance): # find attention for each chunk
                chunk_text = str(chunk)
                logging.info("chunk_index: " + str(chunk_index))
                logging.info(f"chunk_text: {chunk_text}")
                attention_span, original_attention_span, attention_span_response, valid_flag = find_evidence(question, raw_answer, chunk_text, model_name = model_name) # w/o filter, first two returned ele are the same
                logging.info(f"original_attention_span: {original_attention_span}")
                logging.info(f"attention_span: {attention_span}")
                logging.info(f"attention_span_response: {attention_span_response}")
                logging.info(f"valid_flag: {valid_flag}")
                evidence_unfiltered += original_attention_span
                if valid_flag:
                    evidence+=attention_span # attention_sapn is a string

            

            # evidence = list(set([attention_span for attention_spans in evidence for attention_span in attention_spans])) # regardless of chunk_index


            # step5: generate answer using evidence
            evidence_answer = generate_from_evidence(question+evaluation_instruction, evidence)

            provenance_dict = {
            "model_name": model_name,
            "baseline_type": 0,
            "document_path": document_path,
            "question": question,
            "raw_provenance": provenance,
            "evidence": evidence,
            "raw_answer": raw_answer,
            "evidence_answer": evidence_answer,
            "jaccard_similarity": jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer),
            "search_pool": [],
            "unfiltered_evidence": evidence_unfiltered
            }

            logging.info(f"\nAll splits\n{all_splits}")
            close_logging(logger, [file_handler, console_handler])

            with open(f'test/output/provenance/baseline0/{dataset_name}/{model_name}/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
        
    vectorstore.delete_collection()

def baseline1(dataset_name, model_name, question_set, threshold = 0.5, baseline_name="baseline1"):
    # baseline1 uses generated data from baseline0
    # 2. extract each answer, from results of baseline 0
    # extract raw_answer in baseline 0, append every key, value pair to a list
    # 指定文件夹路径
    folder_path = f'test/output/provenance/baseline0/{dataset_name}/{model_name}'
    extracted_question_path = f'test/output/provenance/questionset_{dataset_name}_{model_name}.json'


    # 获取文件夹内所有JSON文件的路径
    file_paths = glob.glob(os.path.join(folder_path, '*.json'))

    logger, file_handler, console_handler, timestamp = setup_logging()
    logging.info(f"run baseline1.py for {dataset_name} with {model_name}")
    logging.info(f"folder_path: {folder_path}")
    logging.info(f"extracted_question_path: {extracted_question_path}")
    logging.info(f"file number: {len(file_paths)}")
    close_logging(logger, [file_handler, console_handler])

    run_info = {
        "dataset_name": dataset_name,
        "model_name": model_name,
        "file_number": len(file_paths),
        "extracted_question_path": extracted_question_path,
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
            logging.info(f"extracted_question_path: {extracted_question_path}")
            logging.info(f"file_path: {file_path}")

            content = json.load(file)  # 将JSON内容解析为字典
            question = content["question"]
            if question == 'Does this paper involve the theory “A Model of Personal Informatics”?':
                question = 'Does this paper involve the theory "A Model of Personal Informatics"?'
            raw_answer = content["raw_answer"]
            document_path = content["document_path"]
            raw_provenance = content["raw_provenance"] # provenance is a list of str
            logging.info(f"question: {question}")
            logging.info(f"answer: {raw_answer}")
            logging.info(f"document_path: {document_path}")
            logging.info(f"raw_provenance: {raw_provenance}")
            logging.info(f"raw_provenance_len: {len(raw_provenance)}")

            # extracted_question_list = get_extracted_question(question, extracted_question_path)
            extracted_question_list = [question]
            logging.info(f"extracted_question_list: {extracted_question_list}")
            extracted_answer_list = answer_extractor(raw_answer, model_name=model_name) # model should be the same as 'extracted_question_path'
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
            evaluation_instruction = get_evaluation_instruction(question, question_set, dataset_name)


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
                "raw_answer": raw_answer,
                "evidence_answer": evidence_answer,
                "jaccard_similarity": jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer),
                "search_pool": extracted_search_list,
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
            with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
            with open(f'test/output/logging/logging_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(logging_dict, f, ensure_ascii=False, indent=4)
            close_logging(logger, [file_handler, console_handler])

    # 6. store the results in a json file, same format as baseline 0



# def baseline1(question, raw_answer, raw_provenance, document_path, model_name, threshold = 0.5, baseline_name="baseline1"):

#     logging.info(f"question: {question}")
#     logging.info(f"answer: {raw_answer}")
#     logging.info(f"document_path: {document_path}")
#     logging.info(f"raw_provenance: {raw_provenance}")
#     logging.info(f"raw_provenance_len: {len(raw_provenance)}")

#     # extracted_question_list = get_extracted_question(question, extracted_question_path)
#     extracted_question_list = [question]
#     logging.info(f"extracted_question_list: {extracted_question_list}")
#     extracted_answer_json = query_extractor(raw_answer, model_name=model_name) # model should be the same as 'extracted_question_path'
#     logging.info(f"extracted_answer_json: {extracted_answer_json}")
#     extracted_answer_list = json_flatten_2list(extracted_answer_json)
#     logging.info(f"extracted_answer_list: {extracted_answer_list}")

#     extracted_search_list = extracted_question_list + extracted_answer_list
#     extracted_search_list = list(set(extracted_search_list)) # remove duplicates
#     extracted_search_list = [x for x in extracted_search_list if x] # remove empty strings
#     logging.info(f"extracted_search_list: {extracted_search_list}")

#     sentences = []
#     sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)
    
#     total_token_num = get_token_num_for_list(sentences)
#     all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
#     logging.info(f"sentences: {sentences}")
#     logging.info(f"sentences_len: {len(sentences)}")
#     logging.info(f"all_splits: {all_splits}")
#     logging.info(f"all_splits_len: {len(all_splits)}")
    
# # 4. embedding list in 2 and all sentences in 3, get the most similar sentence for each key, value pair. We can set a threshold for the similarity score, return those above the threshold. Get evidence
#     evidence = []
#     unsorted_unfiltered_evidence_with_index = []
#     unsorted_evidence_with_index = []
#     less_similar_evidence_with_index = []
#     searched_docs = []

#     vector_store = store_splits(all_splits)
#     for list_index, extracted_search in enumerate(extracted_search_list):
#         searched_docs.append(vector_store.similarity_search_with_score(extracted_search, k=30)) # using large k to return all chunks' score, then we can filter by threshold. # return is a list of tuple, (Document, score) # lower score more similar
#         # logging.info(f"searched_docs: {searched_docs}")   
    
#         # for doc in searched_docs:
#         #     if doc[1] < 0.3: # doc is a tuple, (Document, score)
#         #         evidence.append(doc[0].page_content)
#         # evidence = list(set(evidence))

#         # logging.info(f"evidence_len: {len(evidence)}")
#     vector_store.delete_collection()

#     logging.info(f"searched_docs: {searched_docs}")

#     # cosine distance to cosine similarity
#     searched_docs = [[(doc[0], 0+doc[1]) for doc in docs] for docs in searched_docs]

#     # 对每个list中的tuple根据第二个元素进行降序排序
#     # sorted_data = [sorted(lst, key=lambda x: x[1], reverse=True) for lst in searched_docs]
#     # logging.info(f"sorted_data: {sorted_data}")

#     # bfs style
#     # 从每个list中取出score最高的tuple，放入evidence中，直到evidence中的token数量超过总token数量的20%
#     for i in range(len(searched_docs[0])): # i is the index of top i in each list element
#         if get_token_num_for_list(evidence) < total_token_num * 0.2:
#             for j in range(len(searched_docs)): # j is the index of search_pool list
#                 if searched_docs[j][i][0].page_content in evidence:
#                     continue
#                 elif searched_docs[j][i][1] > threshold: # filter out less similar ones:
#                     less_similar_evidence_with_index.append([searched_docs[j][i][0].page_content, j])
#                     unsorted_unfiltered_evidence_with_index.append([searched_docs[j][i][0].page_content, j])
#                     continue
#                 else:
#                     unsorted_unfiltered_evidence_with_index.append([searched_docs[j][i][0].page_content, j])
#                     evidence.append(searched_docs[j][i][0].page_content)
#                     unsorted_evidence_with_index.append([searched_docs[j][i][0].page_content, j])
#         else:
#             break
    
#     evidence = sort_substrings(raw_provenance, evidence)
#     logging.info(f"evidence: {evidence}")
#     searched_docs_with_score = [[(doc[0].page_content, doc[1]) for doc in docs] for docs in searched_docs ]
#     logging.info(f"searched_docs_with_score: {searched_docs_with_score}")
#     sorted_data_with_score = [[(doc[0].page_content, doc[1]) for doc in docs] for docs in searched_docs ]

#     logging.info(f"evidence_token_num: {get_token_num_for_list(evidence)}")
#     logging.info(f"total_token_num: {total_token_num}")



# # 5. generate answer from evidence
#     evaluation_instruction = get_evaluation_instruction(question, question_set, dataset_name)


#     evidence_answer = generate_from_evidence(question+evaluation_instruction, evidence)
#     logging.info(f"prompt_instruction: {question+evaluation_instruction}")
#     logging.info(f"evidence_answer: {evidence_answer}")
#     provenance_dict = {
#         "model_name": model_name,
#         "baseline_type": 1,
#         "document_path": document_path,
#         "question": question,
#         "raw_provenance": raw_provenance,
#         "evidence": evidence,
#         "raw_answer": raw_answer,
#         "evidence_answer": evidence_answer,
#         "jaccard_similarity": jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer),
#         "search_pool": extracted_search_list,
#         "unsorted_evidence": unsorted_evidence_with_index,
#         "less_similar_evidence": less_similar_evidence_with_index,
#         "unsorted_unfiltered_evidence": unsorted_unfiltered_evidence_with_index
#     }

#     logging_dict = {
#         "question": question,
#         "raw_answer": raw_answer,
#         "evidence_answer": evidence_answer,
#         "evidence_token_num": get_token_num_for_list(evidence),
#         "total_token_num": total_token_num,
#         "extracted_search_list": extracted_search_list,
#         "searched_docs": searched_docs_with_score,
#         "sorted_data": sorted_data_with_score,
#         "evidence": evidence,
#         "unsorted_evidence": unsorted_evidence_with_index,
#         "less_similar_evidence": less_similar_evidence_with_index,
#         "unsorted_unfiltered_evidence": unsorted_unfiltered_evidence_with_index
#     }

#     logging.info(f"all_splits: {all_splits}")
    
#     # output_filename = convert_baseline(os.path.basename(file_path))
#     with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
#         json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
#     with open(f'test/output/logging/logging_{timestamp}.json', 'w', encoding='utf-8') as f:
#         json.dump(logging_dict, f, ensure_ascii=False, indent=4)
#     close_logging(logger, [file_handler, console_handler])

#     # 6. store the results in a json file, same format as baseline 0


def baseline2(dataset_name, model_name, question_set, threshold = 0.99, baseline_name="baseline2"):
    # baseline1 uses generated data from baseline0
    # 2. extract each answer, from results of baseline 0
    # extract raw_answer in baseline 0, append every key, value pair to a list
    # 指定文件夹路径
    folder_path = f'test/output/provenance/baseline0/{dataset_name}/{model_name}'


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
            raw_provenance = content["raw_provenance"] # provenance is a list of str
            logging.info(f"question: {question}")
            logging.info(f"answer: {raw_answer}")
            logging.info(f"document_path: {document_path}")
            logging.info(f"raw_provenance: {raw_provenance}")
            logging.info(f"raw_provenance_len: {len(raw_provenance)}")


            sentences = nltk_sent_tokenize_for_list(raw_provenance, 10)
            
            total_token_num = get_token_num_for_list(sentences)

            index_to_delete = []
            evidence_answer = ""
            jaccard_similarity = 0
            temp_evidence_answer = ""

            iterate_list = list(range(len(sentences)))
            # random.shuffle(iterate_list) # random initializaion
            evaluation_instruction = get_evaluation_instruction(question, question_set, dataset_name)
            logging.info(f"evaluation_instruction: {evaluation_instruction}")
            for i in iterate_list:
                print(len(sentences))
                logging.info(f"i: {i}")
                temp_index_to_delete = index_to_delete.copy()
                logging.info(f"index_to_delete: {index_to_delete}")
                temp_index_to_delete.append(i)
                logging.info(f"temp_index_to_delete: {temp_index_to_delete}")
                temp_sentence = remove_elements_by_indexes(sentences, temp_index_to_delete)
                logging.info(f"temp_sentence: {temp_sentence}")
                temp_evidence_answer = generate_from_evidence(question+evaluation_instruction, temp_sentence)
                logging.info(f"temp_evidence_answer: {temp_evidence_answer}")
                temp_jaccard_similarity = jaccard_similarity_word_union_cleaned(raw_answer, temp_evidence_answer)
                logging.info(f"temp_jaccard_similarity: {temp_jaccard_similarity}")
                if temp_jaccard_similarity > threshold: # no influence on the result
                    index_to_delete = temp_index_to_delete
                    logging.info(f"index {i} is deleted")
                    logging.info(f"index_to_delete: {index_to_delete}")
                    evidence_answer = temp_evidence_answer
                    jaccard_similarity = temp_jaccard_similarity
                    continue
            if not evidence_answer:
                evidence_answer = raw_answer
                jaccard_similarity = temp_jaccard_similarity
            
            evidence = remove_elements_by_indexes(sentences, index_to_delete)
            logging.info(f"evidence: {evidence}")


            logging.info(f"sentences: {sentences}")
            logging.info(f"sentences_len: {len(sentences)}")
            
            
            
            logging.info(f"evidence_token_num: {get_token_num_for_list(evidence)}")
            logging.info(f"total_token_num: {total_token_num}")



    # 5. generate answer from evidence
            



            logging.info(f"prompt_instruction: {question+evaluation_instruction}")
            logging.info(f"evidence_answer: {evidence_answer}")
            provenance_dict = {
                "model_name": model_name,
                "baseline_type": 2,
                "document_path": document_path,
                "question": question,
                "raw_provenance": raw_provenance,
                "evidence": evidence,
                "raw_answer": raw_answer,
                "evidence_answer": evidence_answer,
                "jaccard_similarity": jaccard_similarity_word_union_cleaned(raw_answer, evidence_answer),
                "index_to_delete": index_to_delete,
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
            with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(provenance_dict, f, ensure_ascii=False, indent=4)
            with open(f'test/output/logging/logging_{timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(logging_dict, f, ensure_ascii=False, indent=4)
            close_logging(logger, [file_handler, console_handler])