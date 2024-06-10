import os, sys, json
from query_decompose import query_decomposition, sample_questions, civic_questions, paper_questions # sample_questions() returns a list of sample questions
from retrieve_and_generation import retrieve_and_generation
from indexing import load_local_folder_of_txt, load_local_txt, split_docs, store_splits, sample_folders
from answer_merge import merge_answers

# step0: load sample question and folder path ----------------------------
# question = sample_questions()[0] # 0 is Civic, 1 is Paper
# folder_path = sample_folders()[0]
questions = paper_questions() 
folder_path = sample_folders()[1] # 0 is Civic, 1 is Paper

# step1: indexing ----------------------------
docs = load_local_folder_of_txt(folder_path)
vectorstore = store_splits(split_docs(docs, chunk_size=1000, chunk_overlap=200, add_start_index=True))

# Initialize a list to store the results
results = []

for question in questions:

    # step2: query decomposition --------------------------------
    sub_querys = query_decomposition(question)
    # print(sub_querys)
    sub_query_list = [sub_query.sub_query for sub_query in sub_querys]
    # print(sub_query_list)

    # step3: retrieve and generation for each sub-query----------------------------
    sub_answer = []
    for sub_query in sub_query_list:
        sub_answer.append(retrieve_and_generation(sub_query, vectorstore))

    # step4: answer merging ----------------------------
    final_answer = merge_answers(question, sub_query_list, sub_answer)

    # Append the question and final answer to the results list
    results.append({
        "question": question,
        "final_answer": final_answer
    })

    # print(question)
    # print(final_answer)

# Save results to a JSON file
with open('test/output/paper_langchain_RAG.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("output saved to json file!")

#TODO: store vectorstore to disk