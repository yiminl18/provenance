import os, sys, json
from query_decompose import query_decomposition, sample_questions, civic_questions, paper_questions # sample_questions() returns a list of sample questions
from retrieve_and_generation import retrieve_and_generation
from indexing import load_local_folder_of_txt, load_local_txt, split_docs, store_splits, sample_folders
from answer_merge import merge_answers
from setup_logging import setup_logging
import logging

setup_logging()

# step0: load sample question and folder path ----------------------------
# question = sample_questions()[0] # 0 is Civic, 1 is Paper
questions = list(paper_questions()[1])
# folder_path = sample_folders()[0] # 0 is Civic, 1 is Paper
folder_path = 'data/civic/extracted_data/malibucity_agenda__01262022-1835.txt'

logging.info(f"folder_path: {folder_path}")


# step1: indexing ----------------------------
# docs = load_local_folder_of_txt(folder_path)
docs = load_local_txt(folder_path)
vectorstore = store_splits(split_docs(docs, chunk_size=1000, chunk_overlap=200, add_start_index=True))

# Initialize a list to store the results
results = []

for question in questions:

    # step2: query decomposition --------------------------------
    sub_querys = query_decomposition(question)
    # print(sub_querys)
    sub_query_list = [sub_query.sub_query for sub_query in sub_querys]
    logging.info(f"question: {question}")
    logging.info(f"sub_query_list: {sub_query_list}")


    # step3: retrieve and generation for each sub-query----------------------------
    sub_answer = []
    for sub_query in sub_query_list:
        sub_ans, retrieved_docs = retrieve_and_generation(sub_query, vectorstore)
        sub_answer.append(sub_ans)

        logging.info(f"For sub_query: {sub_query}") # print each sub-query
        logging.info(f"Its sub_answer: {sub_ans}\n Using following chunks:") # print each sub-answer
        k = 0 # print top k retrieved docs
        for doc in retrieved_docs:
            k += 1
            logging.info(f"top{k}\n retrieved_docs:\n {doc.metadata}\n {doc.page_content}\n {'-'*10}") # print each retrieved doc

    # step4: answer merging ----------------------------
    final_answer = merge_answers(question, sub_query_list, sub_answer)

    # Append the question and final answer to the results list
    results.append({
        "question": question,
        "final_answer": final_answer
    })

    # print(question)
    # print(final_answer)

logging.info(f"sub_answer: {sub_answer}")
logging.info(f"final_answer: {final_answer}")

# Save results to a JSON file
with open('test/output/langchain_civic_RAG_1.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("output saved to json file!")

#TODO: store vectorstore to disk