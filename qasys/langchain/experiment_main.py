import time
from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path
from calculate_str_similarity import calculate_str_similarity
from json_average import draw_average_result, draw_average_result_all, get_average_result_baseline1, get_average_result_baseline2
# #TODO: store vectorstore to disk


from baseline import baseline0, baseline1, baseline2_greedy_search, baseline2_binary_search, rag_dataset_generation
dataset_names = ['civic', 'notice', 'paper']
model_names = ['gpt4o']
question_sets = [civic_q(), notice_q(), paper_q()]
document_sets = [civic_path(), notice_path(), paper_path()]
baseline_names = ['baseline0', 'baseline1', 'baseline2_greedy', 'baseline2_binary']
# thresholds = [0.4, 0.6, 0.7]

# for dataset_name, question_set, document_set in zip(dataset_names, question_sets, document_sets):
#     rag_dataset_generation(dataset_name, question_set, document_set)
for _ in range(3):
    for dataset_name in dataset_names:
        baseline0(dataset_name, model_names, "baseline0")

    # for dataset_name in dataset_names:
    #     baseline1(dataset_name, model_names, 0.7, "baseline1")

# for dataset_name in dataset_names:
#     baseline2_binary_search(dataset_name, model_names, baseline_name="baseline2_binary")


    # for dataset_name in dataset_names:
    #     baseline2_greedy_search(dataset_name, model_names, baseline_name="baseline2_greedy")

    # for dataset_name in dataset_names:
    #     baseline2_binary_search(dataset_name, model_names, baseline_name="baseline2_binary")

# for dataset_name, question_set, folder_path in zip(dataset_names, question_sets, folder_paths):
#     for doc in folder_path:
#         baseline0(dataset_name, model_names, question_set, doc)

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     for model_name in model_names:
#         baseline1(dataset_name, model_name, question_set, 0.7, "baseline1")

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     for model_name in model_names:
#         baseline1(dataset_name, model_name, question_set, 0.5, "baseline1_0.5")

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     for model_name in model_names:
#         baseline1(dataset_name, model_name, question_set, 0.6, "baseline1_0.6")

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     baseline1(dataset_name, model_names, question_set, 0.75, "baseline1")

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     for model_name in model_names:
#         baseline1(dataset_name, model_name, question_set, 0.8, "baseline1_0.8")

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     for model_name in model_names:
#         for baseline_name in baseline_names:
#             baseline1(dataset_name, model_name, question_set, 0.522, baseline_name)

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     baseline2_binary_search(dataset_name, model_names, question_set, baseline_name="baseline2_greedy")

# for dataset_name, question_set in zip(dataset_names, question_sets):
#     baseline2_binary_search(dataset_name, model_names, question_set, baseline_name="baseline2_binary")

 




# for dataset_name, question_set in zip(dataset_names, question_sets):
#     for baseline_name in baseline_names:
#         for model_name in model_names:
#             calculate_str_similarity(baseline_name, dataset_name, model_name, question_set)
#             print(f"baseline_name: {baseline_name}, dataset_name: {dataset_name}, model_name: {model_name}")

# for baseline_name in ['baseline0', 'baseline1_0.4', 'baseline1_0.5', 'baseline1_0.6', 'baseline1_0.7', 'baseline1_0.8']:
#     get_average_result_baseline1(baseline_name, dataset_names, model_names)

# for baseline_name in ['baseline2']:
#     get_average_result_baseline2(baseline_name, dataset_names, model_names)

# for baseline_name in baseline_names:
#     draw_average_result_all(baseline_name)