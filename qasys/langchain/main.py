import os, sys
from query_decompose import query_decomposition, sample_questions # sample_questions() returns a list of sample questions
from retrieve_and_generation import retrieve_and_generation
from indexing import load_local_folder_of_txt, load_local_txt, split_docs, store_splits, sample_folders
from answer_merge import merge_answers

# step0: load sample question and folder path ----------------------------
# question = sample_questions()[0] # 0 is Civic, 1 is Paper
# folder_path = sample_folders()[0]
question = sample_questions()[1] # 0 is Civic, 1 is Paper
folder_path = sample_folders()[1]

# step1: query decomposition --------------------------------
sub_querys = query_decomposition(question)
# print(sub_querys)
sub_query_list = [sub_query.sub_query for sub_query in sub_querys]
# print(sub_query_list)

# step2: indexing ----------------------------
docs = load_local_folder_of_txt(folder_path)
vectorstore = store_splits(split_docs(docs, chunk_size=1000, chunk_overlap=200, add_start_index=True))

# step3: retrieve and generation for each sub-query----------------------------
sub_answer = []
for sub_query in sub_query_list:
    sub_answer.append(retrieve_and_generation(sub_query, vectorstore))

# step4: answer merging ----------------------------
final_answer = merge_answers(question, sub_query_list, sub_answer)


print(final_answer)

#TODO: store vectorstore to disk