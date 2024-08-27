import os, glob, json
from label_file import append_to_json_file
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pretrain_sentence_splitter import get_token_num_for_list, get_token_num
from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path, get_evaluation_instruction
from retrieve_and_generation import generate_from_evidence


# def get_average_result(baseline_name, dataset_name, model_name):

#     # 获取文件夹内所有JSON文件的路径
#     folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

#     file_paths = glob.glob(os.path.join(folder_path+"/jaccard_union", '*.json'))

#     scores = []

#     # 依次读取每个JSON文件并解析为字典
#     for file_path in file_paths:
#         # 打开文件并读取内容
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = json.load(file)
#             print(f"file_path: {file_path}")
#             scores.append(content["jaccard_similarity"])

            
#     result = {
#         "baseline_name": baseline_name,
#         "model_name": model_name,
#         "dataset_name": dataset_name,
#         "average_jaccard_similarity": sum(scores) / len(scores)
#     }

def get_average_result_baseline1(baseline_name:str, dataset_names:list[str], model_names:list[str]):

    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            scores = []
            success_scores = []
            success_evidence = []
            success_evidence_sentence_number = []

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    print(f"file_path: {file_path}")
                    scores.append(content["jaccard_similarity"])
                    if scores[-1] > 0.99: # valid index list
                        success_scores.append(content["jaccard_similarity"])
                        success_evidence += content["evidence"] # evidence is a list of str
                        success_evidence_sentence_number.append(len(content["evidence"]))
                    
            result = {
                "baseline_name": baseline_name,
                "model_name": model_name,
                "dataset_name": dataset_name,
                "average_jaccard_similarity": sum(scores) / len(scores),
                "accuracy": len(success_scores) / len(scores),
                "average_len_of_success_evidence": get_token_num_for_list(success_evidence) / len(success_evidence),
                "average_sentence_number_of_success_evidence": sum(success_evidence_sentence_number) / len(success_evidence_sentence_number)
            }

            file_path_to_save = f'test/output/provenance/{baseline_name}/average_result.json'
            append_to_json_file(file_path_to_save, result)

def get_average_result_baseline2(baseline_name:str, dataset_names:list[str], model_names:list[str]):

    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            scores = []
            success_scores = []
            success_evidence = []
            success_evidence_sentence_number = []

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    print(f"file_path: {file_path}")
                    scores.append(content["jaccard_similarity"])
                    index_to_delete = content["index_to_delete"]
                    if len(index_to_delete) >= 5 and scores[-1] > 0.99: # valid index list
                        success_scores.append(content["jaccard_similarity"])
                        success_evidence += content["evidence"] # evidence is a list of str
                        success_evidence_sentence_number.append(len(content["evidence"]))
                    
            result = {
                "baseline_name": baseline_name,
                "model_name": model_name,
                "dataset_name": dataset_name,
                "average_jaccard_similarity": sum(scores) / len(scores),
                "accuracy": len(success_scores) / len(scores),
                "average_len_of_success_evidence": get_token_num_for_list(success_evidence) / len(success_evidence),
                "average_sentence_number_of_success_evidence": sum(success_evidence_sentence_number) / len(success_evidence_sentence_number)
            }

            file_path_to_save = f'test/output/provenance/{baseline_name}/average_result.json'
            append_to_json_file(file_path_to_save, result)

def draw_score_distribution(baseline_name:str, dataset_names:list[str], model_names:list[str]):
    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            scores = []

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                file_path = file_path.replace(f"provenance/{baseline_name}/{dataset_name}/{model_name}/provenance", f"logging/logging")
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    print(f"file_path: {file_path}")
                    searched_docs = content["searched_docs"] # is a list of list, each list contains the search results for a question
                    for search_results in searched_docs:
                        for search_result in search_results:
                            scores.append(search_result[1])
            # 设置bin的宽度和范围
            bin_width = 0.05
            bins = np.arange(0, 1 + bin_width, bin_width)

            # 画频数条形图
            plt.hist(scores, bins=bins, edgecolor='black')

            # 设置图表标题和标签
            plt.title(f'{baseline_name} {dataset_name} {model_name} Score Distribution')
            plt.xlabel('Value')
            plt.ylabel('Frequency')

            # 保存图表到指定目录
            save_path = f'test/output/provenance/{baseline_name}/score_distribution_{dataset_name}_{model_name}.png'
            plt.savefig(save_path)
            plt.close()

def draw_average_result(baseline_name:str):
    file_path = f'test/output/provenance/{baseline_name}/average_result.json'
    # Data provided by the user for baseline1_0.5
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Create DataFrame for the new data
    df_new = pd.DataFrame(data)
    

    # Pivot the dataframe to get models as columns and datasets as rows
    pivot_df_new = df_new.pivot(index='dataset_name', columns='model_name', values='average_jaccard_similarity')

    # Plotting the data with updated title and data labels for the new data
    ax_new = pivot_df_new.plot(kind='bar', figsize=(10, 6), edgecolor='black')
    plt.title(baseline_name)
    plt.xlabel('Dataset')
    plt.ylabel('Average Jaccard Similarity')
    plt.xticks(rotation=0)
    plt.legend(title='Model')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding data labels
    for p in ax_new.patches:
        ax_new.annotate(format(p.get_height(), '.2f'),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha = 'center', va = 'center',
                        xytext = (0, 9),
                        textcoords = 'offset points')

    plt.tight_layout()

    save_path = f'test/output/provenance/{baseline_name}/average_result.png'
    plt.savefig(save_path)
    plt.close()

def draw_average_result_all(baseline_name='baseline2'):
    file_path = f'test/output/provenance/{baseline_name}/average_result.json'
    # Data provided by the user for baseline1_0.5
    with open(file_path, 'r') as file:
        data = json.load(file)

    datasets = [item['dataset_name'] for item in data]
    average_jaccard_similarity = [item['average_jaccard_similarity'] for item in data]
    accuracy = [item['accuracy'] for item in data]
    average_len_of_success_evidence = [item['average_len_of_success_evidence'] for item in data]
    average_sentence_number_of_success_evidence = [item['average_sentence_number_of_success_evidence'] for item in data]


    import matplotlib.cm as cm
    x = np.arange(len(datasets))
    bar_width = 0.4
    # Use a colormap for better aesthetics
    colors = cm.viridis(np.linspace(0.2, 0.8, 4))

    # Create a figure with three subplots
    plt.figure(figsize=(14, 10))

    # Column chart for Average Jaccard Similarity
    plt.subplot(2, 2, 1)
    plt.bar(x, average_jaccard_similarity, color=colors[0], width=bar_width)
    for i, v in enumerate(average_jaccard_similarity):
        plt.text(i, v - 0.02, f"{v:.2f}", ha='center', va='top', color='white')
    plt.title('Average Jaccard Similarity by Dataset')
    plt.ylim(0, 1)
    plt.ylabel('Avg Jaccard Similarity')
    plt.xticks(x, datasets)

    # Column chart for Accuracy
    plt.subplot(2, 2, 2)
    plt.bar(x, accuracy, color=colors[1], width=bar_width)
    for i, v in enumerate(accuracy):
        plt.text(i, v - 0.02, f"{v:.2f}", ha='center', va='top', color='white')
    plt.ylim(0, 1)
    plt.title('Accuracy by Dataset')
    plt.ylabel('Accuracy')
    plt.xticks(x, datasets)

    # Column chart for Average Length of Success Evidence
    plt.subplot(2, 2, 3)
    plt.bar(x, average_len_of_success_evidence, color=colors[2], width=bar_width)
    for i, v in enumerate(average_len_of_success_evidence):
        plt.text(i, v - 0.5, f"{v:.2f}", ha='center', va='top', color='white')
    plt.title('Average Length of Success Evidence by Dataset')
    plt.ylabel('Avg Length of Success Evidence')
    plt.xlabel('Dataset')
    plt.xticks(x, datasets)

    # Column chart for Average sentence number of Success Evidence
    plt.subplot(2, 2, 4)
    plt.bar(x, average_sentence_number_of_success_evidence, color=colors[3], width=bar_width)
    for i, v in enumerate(average_sentence_number_of_success_evidence):
        plt.text(i, v - 0.5, f"{v:.2f}", ha='center', va='top', color='white')
    plt.title('Average Number of Success Evidence Sentence by Dataset')
    plt.ylabel('Avg Number of Success Evidence Sentence')
    plt.xlabel('Dataset')
    plt.xticks(x, datasets)

    plt.tight_layout()

    save_path = f'test/output/provenance/{baseline_name}/average_result.png'
    plt.savefig(save_path)
    plt.close()

def check_failed_case(baseline_name:str, dataset_names:list[str], model_names:list[str]):

    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))


            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    score=content["jaccard_similarity"]
                    index_to_delete = content["index_to_delete"]
                    if score < 0.99:
                        if index_to_delete:
                            print(f"file_path: {file_path}")



def check_evidence_diff(baseline_names:list[str], dataset_names:list[str], model_names:list[str], baseline_type:float, question_set, document_path_set):
    evidence_diff_info = []
    both_success_case_number = 0
    # 获取文件夹内所有JSON文件的路径
    for dataset_index, dataset_name in enumerate(dataset_names):
        for model_name in model_names:
            for question_index, question in enumerate(question_set[dataset_index]):
                for document_path_index, document_path in enumerate(document_path_set[dataset_index]):
                # 打开文件并读取内容
                    file_path_0 = f'test/output/provenance/{baseline_names[0]}/{dataset_name}/{model_name}/labeled_file/b{baseline_type}_{dataset_name}_{model_name}_q{question_index}_d{document_path_index}.json'
                    file_path_1 = f'test/output/provenance/{baseline_names[1]}/{dataset_name}/{model_name}/labeled_file/b{baseline_type}_{dataset_name}_{model_name}_q{question_index}_d{document_path_index}.json'
                    with open(file_path_0, 'r', encoding='utf-8') as file:
                        content_0 = json.load(file)[0]
                        score_0=content_0["jaccard_similarity"]
                        evidence_0 = content_0["evidence"]
                        answer_0 = content_0["raw_answer"]
                    with open(file_path_1, 'r', encoding='utf-8') as file:
                        content_1 = json.load(file)[0]
                        score_1=content_1["jaccard_similarity"]
                        evidence_1 = content_1["evidence"]
                        answer_1 = content_1["raw_answer"]
                    if score_0 > 0.95 and score_1 > 0.95:
                        both_success_case_number += 1
                        if evidence_0 != evidence_1:
                            print(f"file_path_0: {file_path_0}")
                            print(f"file_path_1: {file_path_1}")
                            print(f"evidence_0: {evidence_0}")
                            print(f"evidence_1: {evidence_1}")
                            evidence_diff_info.append(
                                {
                                "file_name": f"b{baseline_type}_{dataset_name}_{model_name}_q{question_index}_d{document_path_index}.json",
                                "question": question,
                                "document_path": document_path,
                                "evidence_0": evidence_0,
                                "evidence_1": evidence_1,
                                "answer_0": answer_0,
                                "answer_1": answer_1
                            }
                            )
    file_to_save = f'test/output/provenance/{baseline_names[0]}_{baseline_names[1]}_evidence_diff.json'
    print(f"len(evidence_diff_info): {len(evidence_diff_info)}")
    print(f"both_success_case_number: {both_success_case_number}")
    with open(file_to_save, 'w', encoding='utf-8') as f:
        json.dump(evidence_diff_info, f, indent=4)

def check_uncertainty(baseline_names:list[str], dataset_names:list[str], model_names:list[str], question_sets):
    # 获取文件夹内所有JSON文件的路径
    for baseline_index, baseline_name in enumerate(baseline_names):
        file_to_save = f'test/output/provenance/{baseline_name}/uncertainty.json'
        for dataset_name, question_set in zip(dataset_names, question_sets):
            for model_name in model_names:
                folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

                file_paths = glob.glob(os.path.join(folder_path, '*.json'))


                # 依次读取每个JSON文件并解析为字典
                for file_path in file_paths:
                    # 打开文件并读取内容
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = json.load(file)
                        question = content["question"]
                        raw_provenance = content["raw_provenance"]
                        evidence = content["evidence"]
                        raw_answer = content["raw_answer"]
                        evidence_answer = content["evidence_answer"]
                        evaluation_instruction = get_evaluation_instruction(question, question_set, dataset_name)
                        for i in range(20):
                            reproduce_raw_answer = generate_from_evidence(question + evaluation_instruction, raw_provenance)
                            print(f"question: {question}")
                            print(f"evaluation_instruction: {evaluation_instruction}")
                            print(f"raw_answer: {raw_answer}")
                            print(f"reproduce_raw_answer: {reproduce_raw_answer}")
                            if raw_answer != reproduce_raw_answer:
                                append_to_json_file(file_to_save, {
                                    "question": question,
                                    "raw_provenance": raw_provenance,
                                    "evidence": "",
                                    "raw_answer": raw_answer,
                                    "evidence_answer": "",
                                    "reproduce_raw_answer": reproduce_raw_answer,
                                    "reproduce_raw_provenance": "",
                                    "file_path": file_path,
                                    "run": i
                                })
                        for i in range(20):
                            reproduce_evidence_answer = generate_from_evidence(question + evaluation_instruction, evidence)
                            print(f"question: {question}")
                            print(f"evaluation_instruction: {evaluation_instruction}")
                            print(f"evidence_answer: {evidence_answer}")
                            print(f"reproduce_evidence_answer: {reproduce_evidence_answer}")
                            if evidence_answer != reproduce_evidence_answer:
                                append_to_json_file(file_to_save, {
                                    "question": question,
                                    "raw_provenance": "",
                                    "evidence": evidence,
                                    "raw_answer": "",
                                    "reproduce_raw_answer": "",
                                    "evidence_answer": evidence_answer,
                                    "reproduce_evidence_answer": reproduce_evidence_answer,
                                    "file_path": file_path,
                                    "run": i
                                })

if __name__ == "__main__":
    baseline_names = ["baseline2_sequential"]
    dataset_names = ['civic', 'paper', 'notice']
    model_names = ['gpt4o']
    question_sets = [civic_q(), paper_q(), notice_q()] # same index as dataset_names
    document_path_sets = [civic_path(), paper_path(), notice_path()] # same index as dataset_names
    check_uncertainty(baseline_names, dataset_names, model_names, question_sets)
