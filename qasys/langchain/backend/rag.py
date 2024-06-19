import os, sys
import json
import logging

from query_decompose import query_decomposition, civic_questions
from retrieve_and_generation import retrieve_and_generation
from indexing import load_local_txt, load_local_pdf, load_local_pdf_as_one_page, split_docs, store_splits
from answer_merge import merge_answers
from setup_logging import setup_logging, close_logging
from txt2pdf_path import txt2pdf_path, txt2pdf_path_list, pdf2pdf_path
from node_process import next_node



def rag():
    node_info = {}
    logger, file_handler, console_handler = setup_logging()
    # step0: load sample question and folder path
    question = civic_questions()[0]
    folder_path = 'data/civic/raw_data/malibucity_agenda__01262022-1835.pdf'

    logging.info(f"folder_path: {folder_path}")

    next_node(node_info, {
         "node_id" : 1,
         "node_name": "start",
         "in_nodes": [],
         "out_nodes": [2],
         "in_data": [],
         "out_data": [f"{question}"]
    })

    # step1: indexing
    # docs = load_local_txt(folder_path)
    docs = load_local_pdf(folder_path)

    vectorstore = store_splits(split_docs(docs, chunk_size=2000, chunk_overlap=10, add_start_index=True))

    # Initialize a list to store the results
    results = []

    # for question in questions:

    # step2: query decomposition
    sub_querys = query_decomposition(question)
    sub_query_list = [sub_query.sub_query for sub_query in sub_querys]
    sub_query_len = len(sub_query_list)
    logging.info(f"question: {question}")
    logging.info(f"sub_query_list: {sub_query_list}")

    next_node(node_info, {
        "node_id" : 2,
        "node_name": "query_decomposition",
        "in_nodes": [1],
        "out_nodes": [i+3 for i in range(sub_query_len)],
        "in_data": [f"{question}"],
        "out_data": [f"{sub_query_list}"]
    })

    # step3: retrieve and generation for each sub-query
    sub_answers = []
    retrieved_docs = [] # index for sub_answer and retrieved_docs should be the same

    logging.info("len of sub_query_list: " + str(len(sub_query_list)))
    for sub_query_index, sub_query in enumerate(sub_query_list):
        sub_ans, sub_retrieved_docs, chunk_index = retrieve_and_generation(sub_query, vectorstore, k = 3)
        sub_answers.append(sub_ans)
        retrieved_docs.append([[doc.page_content, doc.metadata["page"]] for doc in sub_retrieved_docs]) # retrieved_docs is a list of list of strings
        logging.info(f"For sub_query: {sub_query}") # print each sub-query
        logging.info(f"Using following chunks:") # print each sub-answer
        logging.info(f"chunk_index: {chunk_index}")
        k = 0 # print top k retrieved docs
        for doc in sub_retrieved_docs:
                k += 1
                logging.info(f"top{k}\n retrieved_docs:\n {doc.metadata}\n {doc.page_content}\n {'-'*10}") # print each retrieved doc
        next_node(node_info, {
            "node_id" : 3+sub_query_index,
            "node_name": "retrival",
            "in_nodes": [2],
            "out_nodes": [3+sub_query_index+sub_query_len],
            "in_data": [f"{sub_query}"],
            "out_data": [f"{sub_retrieved_docs}"]
        })
        
        next_node(node_info,{
            "node_id" : 3+sub_query_len+sub_query_index,
            "node_name": "generation",
            "in_nodes": [3+sub_query_index],
            "out_nodes": [3+sub_query_len*2],
            "in_data": [f"{sub_retrieved_docs}"],
            "out_data": [f"{sub_ans}"]
        })

    # with open("output_101.txt", "w", encoding="utf-8") as file:
    #     for sub_query in sub_query_list:
    #         # file.write("RETRIEDED_DOCS[0]" + str(retrieved_docs[0]))
    #         # print("LEN_RETRIEVED_DOCS[0]", len(retrieved_docs[0]))
    #         # file.write("type of retrieved_docs: " + str(type(retrieved_docs[0])) + "\n")
    #         file.write("LEN OF RETRIEVED_DOCS[0]: " + str(len(retrieved_docs[0])) + "\n")
    #         file.write("--------------------\n")
    #         for doc in retrieved_docs[0]:
    #             file.write("retrieved_chunk_data: ")
    #             # file.write("type of doc: " + str(type(doc)) + "\n") # doc is a tuple
    #             # file.write (str(doc[0].metadata) + "\n")
    #             file.write("For sub_query: " + sub_query + "\n")
    #             file.write(str(doc[0]) + "\n----------retrieved_chunk_end--------\n")

            
    #         # print("LEN_SUB_RETRIEVED_DOCS", len(sub_retrieved_docs))
            

    # step4: answer merging
    final_answer = merge_answers(question, sub_query_list, sub_answers)

    next_node(node_info,{
        "node_id" : 3+sub_query_len*2,
        "node_name": "answer_merging",
        "in_nodes": [3+sub_query_len+sub_query_index for sub_query_index in range(sub_query_len)],
        "out_nodes": [3+sub_query_len*2+1],
        "in_data": [f"{sub_answers}"],
        "out_data": [f"{final_answer}"]
    })

    next_node(node_info,{
         "node_id" : 3+sub_query_len*2+1,
        "node_name": "end",
        "in_nodes": [3+sub_query_len*2],
        "out_nodes": [],
        "in_data": [f"{final_answer}"],
        "out_data": []
    })

    # Append the question and final answer to the results list
    results.append({
        "question": question,
        "final_answer": final_answer
    })

    logging.info(f"sub_answer: {sub_answers}")
    logging.info(f"final_answer: {final_answer}")

    # Save results to a JSON file
    with open('test/output/langchain_civic_RAG_1.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    result = {
        "question": question,
        "sub_query": sub_query_list,
        "document_path": pdf2pdf_path(folder_path),
        "final_answer": final_answer,
        "sub_answers": sub_answers,
        "retrieved_docs": retrieved_docs # retrieved_docs is a list of list of PURE strings (not Document objects, for easy json serialization)
    }
    # print(result)
    close_logging(logger, [file_handler, console_handler])

    with open('test/output/node_info.json', 'w', encoding='utf-8') as f:
        json.dump(node_info, f, ensure_ascii=False, indent=4)

    return result

    # return result, node_info
