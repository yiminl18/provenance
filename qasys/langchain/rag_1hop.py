import os, sys
import json
import logging

from query_decompose import query_decomposition, civic_questions
from retrieve_and_generation import retrieve_and_generation, generate_from_evidence
from indexing import load_local_txt, load_local_pdf, load_local_pdf_as_one_page, split_docs, store_splits, path_extracted2raw, path_raw2extracted
from answer_merge import merge_answers
from setup_logging import setup_logging, close_logging
from txt2pdf_path import txt2pdf_path, txt2pdf_path_list, pdf2pdf_path
from node_process import next_node
from attention_span import attention_span_llm_approach



def rag(question, folder_path):
    node_info = {}
    logger, file_handler, console_handler, timestamp = setup_logging()
    # step0: load sample question and folder path

    logging.info(f"folder_path: {folder_path}")

    next_node(node_info, {
         "node_id" : 1,
         "node_name": "start",
         "in_nodes": [],
         "out_nodes": [2],
         "in_data": [],
         "out_data": [f"{question}"],
         "label": "",
         "prompt:": ""
    })

    # step1: indexing
    # docs = load_local_txt(folder_path)
    docs = load_local_txt(path_raw2extracted(folder_path))

    all_splits = split_docs(docs, chunk_size=1000, chunk_overlap=100, add_start_index=True)

    vectorstore = store_splits(all_splits)

    # Initialize a list to store the results
    results = []

    # for question in questions:

    # do not decompose
    sub_query_list = [question]
    decomposition_prompt = ""

    sub_query_len = len(sub_query_list)
    logging.info(f"question: {question}")
    logging.info(f"sub_query_list: {sub_query_list}")


    # step3: retrieve and generation for each sub-query
    sub_answers = []
    retrieved_docs = [] # index for sub_answer and retrieved_docs should be the same

    logging.info("len of sub_query_list: " + str(len(sub_query_list)))
    for sub_query_index, sub_query in enumerate(sub_query_list):
        sub_ans, sub_retrieved_docs, chunk_index, rag_prompt = retrieve_and_generation(sub_query, vectorstore, k = 5)
        print(f"rag_prompt: {rag_prompt}")
        sub_answers.append(sub_ans)
        # retrieved_docs.append([[doc.page_content, doc.metadata["page"]] for doc in sub_retrieved_docs]) # retrieved_docs is a list of list of strings
        retrieved_docs.append([doc.page_content for doc in sub_retrieved_docs]) # retrieved_docs is a list of list of strings
        logging.info(f"\nFor sub_query: {sub_query}") # print each sub-query
        logging.info(f"Using following chunks:") # print each sub-answer
        logging.info(f"chunk_index: {chunk_index}")
        k = 0 # print top k retrieved docs
        for doc in sub_retrieved_docs:
                k += 1
                logging.info(f"top{k}\n retrieved_docs:\n {doc.metadata}\n {doc.page_content}\n {'-'*10}") # print each retrieved doc
        next_node(node_info, {
            "node_id" : 2+sub_query_index,
            "node_name": "retrival",
            "in_nodes": [1],
            "out_nodes": [2+sub_query_index+sub_query_len],
            "in_data": [f"{sub_query}"],
            "out_data": [f"{sub_retrieved_docs}"],
            "label": "",
            "prompt": ""
        })
        
        next_node(node_info,{
            "node_id" : 2+sub_query_len+sub_query_index,
            "node_name": "generation",
            "in_nodes": [2+sub_query_index],
            "out_nodes": [2+sub_query_len*2],
            "in_data": [f"{sub_retrieved_docs}"],
            "out_data": [f"{sub_ans}"],
            "label": "LLM",
            "prompt": str(rag_prompt)
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
    final_answer  = sub_answers[0]
    # final_answer, merge_prompt = merge_answers(question, sub_query_list, sub_answers)
    # print(f"merge_prompt: {merge_prompt}")

    next_node(node_info,{
         "node_id" : 2+sub_query_len*2,
        "node_name": "end",
        "in_nodes": [1+sub_query_len*2],
        "out_nodes": [],
        "in_data": [f"{final_answer}"],
        "out_data": [],
        "label": "",
        "prompt:": ""
    })

    # Append the question and final answer to the results list
    results.append({
        "question": question,
        "final_answer": final_answer
    })

    logging.info(f"sub_answer: {sub_answers}")
    logging.info(f"final_answer: {final_answer}")

    # # Save results to a JSON file
    # with open('test/output/langchain_civic_RAG_1.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)

    # find attention span
    evdience_finding_model_name = 'gpt4o'
    chunks = []
    chunks_text = []
    chunks_info = []
    for subquery_index, chunks_for_subquery in enumerate(retrieved_docs): # sub_query
        for topk, chunk in enumerate(chunks_for_subquery): # each chunk
            if chunk not in chunks_text:
                chunk_info = f"sq{subquery_index}t{topk}"
                
                
                chunks.append([chunk, chunk_info, []])
                attention_span, attention_span_response, valid_flag = attention_span_llm_approach(sub_query_list[subquery_index], sub_answers[subquery_index], chunk, model_name = evdience_finding_model_name)
                chunks[-1][2].append(attention_span)
                logging.info(f"attention_span: {attention_span}")
                chunks_text.append(chunk)
                # chunk_info is for json logging
                chunks_info.append([chunk, chunk_info, [], attention_span_response, valid_flag])
                chunks_info[-1][2].append(attention_span)
            else:
                for chunk_id in range(len(chunks)):
                    c = chunks[chunk_id]
                    if c[0] == chunk:
                        c[1] = c[1]+(f"sq{subquery_index}t{topk}")
                        attention_span, attention_span_response, valid_flag = attention_span_llm_approach(sub_query_list[subquery_index], sub_answers[subquery_index], chunk, model_name = evdience_finding_model_name)
                        c[2].append(attention_span)
                        logging.info(f"attention_span: {attention_span}")

                        chunks_info[chunk_id][1] = chunks_info[chunk_id][1]+(f"sq{subquery_index}t{topk}")
                        chunks_info[chunk_id][2].append(attention_span)
            

    evidence = list(set([attention_span for chunk in chunks for attention_spans in chunk[2] for attention_span in attention_spans]))
    logging.info(f"evidence: {evidence}")
    evidence_answer = generate_from_evidence(question, evidence)
    logging.info(f"evidence_answer: {evidence_answer}")



    result = {
        "question": question,
        "sub_query": sub_query_list,
        "document_path": pdf2pdf_path(folder_path),
        "final_answer": final_answer,
        "sub_answers": sub_answers,
        # "retrieved_docs": retrieved_docs # retrieved_docs is a list of list of PURE strings (not Document objects, for easy json serialization)
        "chunks": chunks
    }
    # print(result)
    logging.info(f"\nAll splits\n{all_splits}")
    # logging.info(f"\n load pdf:{docs}")
    close_logging(logger, [file_handler, console_handler])

    logging_dict = {
        "evidence finding model": evdience_finding_model_name,
        "folder_path": folder_path,
        "chunk_num": len(all_splits),
        "all splits length": [len(split.page_content) for split in all_splits],
        "question": question,
        "sub_query_list": sub_query_list,
        "sub_answers": sub_answers,
        "final_answer": final_answer,
        "chunks_info": chunks_info,
        "retrieved_docs": [[doc.metadata, doc.page_content] for doc in sub_retrieved_docs],

    }

    provenance_dict = {
        "model name": evdience_finding_model_name,
        "baseline type": 0,
        "document path": folder_path,
        "question": question,
        "raw provenance": retrieved_docs,
        "evidence": evidence,
        "raw answer": final_answer,
        "evidence answer": evidence_answer
    }

    

    with open(f'test/output/node_info/node_info_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(node_info, f, ensure_ascii=False, indent=4)

    with open(f'test/output/highlight_result/result_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    with open(f'test/output/logging/evidence_logging_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(logging_dict, f, ensure_ascii=False, indent=4)

    with open(f'test/output/provenance/provenance_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(provenance_dict, f, ensure_ascii=False, indent=4)

    return result

    # return result, node_info
