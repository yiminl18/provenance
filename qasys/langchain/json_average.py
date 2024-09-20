import os, glob, json
from label_file import append_to_json_file
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pretrain_sentence_splitter import get_token_num_for_list, get_token_num
from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path, get_evaluation_instruction
from retrieve_and_generation import generate_from_evidence
from baseline12_result_merge import get_precision, get_recall, get_jaccard_sentences
import seaborn as sns


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
            # success_scores = []
            evidence = []
            evidence_sentence_number = []

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)[0]
                    print(f"file_path: {file_path}")
                    scores.append(content["jaccard_similarity"])
                    # if scores[-1] > 0.99: # valid index list
                    # success_scores.append(content["jaccard_similarity"])
                    evidence += content["evidence"] # evidence is a list of str
                    # evidence_sentence_number.append(len(content["evidence"]))
                    
            result = {
                "baseline_name": baseline_name,
                "model_name": model_name,
                "dataset_name": dataset_name,
                "average_jaccard_similarity": sum(scores) / len(scores),
                # "accuracy": len(success_scores) / len(scores),
                "average_len_of_success_evidence": get_token_num_for_list(evidence) / len(evidence),
                # "average_sentence_number_of_success_evidence": sum(success_evidence_sentence_number) / len(success_evidence_sentence_number)
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
            provenance_token_number_list = []
            evidence_token_number_list = []

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)

                    # for content in content_list: # if use append_to_json in baseline function

                    print(f"file_path: {file_path}")
                    scores.append(content["jaccard_similarity"])
                    # index_to_delete = content["index_to_delete"]
                    # if len(index_to_delete) >= 5 and scores[-1] > 0.99: # valid index list
                    success_scores.append(content["jaccard_similarity"])
                    success_evidence += content["evidence"] # evidence is a list of str
                    success_evidence_sentence_number.append(len(content["evidence"]))
                    provenance_token_number_list.append(get_token_num_for_list(content["provenance"]))
                    evidence_token_number_list.append(get_token_num_for_list(content["evidence"]))
                    
            average_token_number_of_evidence = sum(evidence_token_number_list) / len(evidence_token_number_list)
            average_token_number_of_provenance = sum(provenance_token_number_list) / len(provenance_token_number_list)
            result = {
                "baseline_name": baseline_name,
                "model_name": model_name,
                "dataset_name": dataset_name,
                "average_jaccard_similarity": sum(scores) / len(scores),
                # "accuracy": len(success_scores) / len(scores),
                "average_token_number_of_evidence": average_token_number_of_evidence,
                "average_token_number_of_provenance": average_token_number_of_provenance,
                "compression_rate": average_token_number_of_evidence / average_token_number_of_provenance
            }

            file_path_to_save = f'test/output/provenance/{baseline_name}/average_result.json'
            append_to_json_file(file_path_to_save, result)

def compression_rate_heatmap(baseline_name: str, dataset_names: list[str], model_names: list[str]):
    
    

    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            # 定义一个字典用于存储每个 (question_index, document_index) 对应的 compression_rate
            compression_rates = {}
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)[0]

                    print(f"file_path: {file_path}")
                    question_index = content["question_id"]
                    document_index = content["document_id"]
                    provenance_token_number = get_token_num_for_list(content["provenance"])
                    evidence_token_number = get_token_num_for_list(content["evidence"])
                    compression_rate = evidence_token_number / provenance_token_number

                    # 使用 question_index 和 document_index 作为键，存储对应的 compression_rate
                    compression_rates[(question_index, document_index)] = compression_rate

            # 获取所有 unique 的 question 和 document 索引
            question_indices = sorted(set([q for q, _ in compression_rates.keys()]))
            document_indices = sorted(set([d for _, d in compression_rates.keys()]))

            # 初始化一个二维数组用于存储 compression_rate 值
            heatmap_data = np.zeros((len(question_indices), len(document_indices)))

            # 将 compression_rate 数据填充到二维数组中
            for (q, d), compression_rate in compression_rates.items():
                q_idx = question_indices.index(q)
                d_idx = document_indices.index(d)
                heatmap_data[q_idx, d_idx] = compression_rate

            # 创建保存热图的文件路径
            save_path = f'test/output/provenance/{baseline_name}/{dataset_name}_{model_name}_compression_rate_heatmap.png'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 确保目录存在

            # 绘制热图
            plt.figure(figsize=(10, 8))
            sns.heatmap(heatmap_data, xticklabels=document_indices, yticklabels=question_indices, cmap='coolwarm', annot=True)
            plt.xlabel('Document Index')
            plt.ylabel('Question Index')
            plt.title(f'Compression Rate Heatmap for {dataset_name} - {model_name}')

            # 保存热图为图片
            plt.savefig(save_path)
            plt.close()  # 关闭图像，释放内存

            print(f"Heatmap saved to {save_path}")


def robustness_heatmap(baseline_name: str, dataset_names: list[str], model_names: list[str]):

    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            # 定义字典来保存不同 content_index 的 precision, recall, f1_score
            precision_dict = {}
            recall_dict = {}
            f1_dict = {}

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content_list = json.load(file)
                    gt_evidence = []
                    for context_index, content in enumerate(content_list):  # 如果使用 append_to_json
                        if context_index == 0:
                            gt_evidence = content["evidence"]
                            continue

                        evidence = content["evidence"]
                        precision = get_precision(evidence, gt_evidence)
                        recall = get_recall(evidence, gt_evidence)
                        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                        question_index = content["question_id"]
                        document_index = content["document_id"]

                        # 将 precision, recall, f1_score 存储到对应的 content_index 字典中
                        if context_index not in precision_dict:
                            precision_dict[context_index] = {}
                            recall_dict[context_index] = {}
                            f1_dict[context_index] = {}

                        precision_dict[context_index][(question_index, document_index)] = precision
                        recall_dict[context_index][(question_index, document_index)] = recall
                        f1_dict[context_index][(question_index, document_index)] = f1_score

            # 针对每个 content_index 生成一张 heatmap
            for context_index in precision_dict.keys():
                # 获取所有 unique 的 question 和 document 索引
                question_indices = sorted(set([q for q, _ in precision_dict[context_index].keys()]))
                document_indices = sorted(set([d for _, d in precision_dict[context_index].keys()]))

                # 初始化三个二维数组分别用于存储 precision, recall, f1_score 的值
                precision_data = np.zeros((len(question_indices), len(document_indices)))
                recall_data = np.zeros((len(question_indices), len(document_indices)))
                f1_data = np.zeros((len(question_indices), len(document_indices)))

                # 填充数据到二维数组中
                for (q, d), precision in precision_dict[context_index].items():
                    q_idx = question_indices.index(q)
                    d_idx = document_indices.index(d)
                    precision_data[q_idx, d_idx] = precision

                for (q, d), recall in recall_dict[context_index].items():
                    q_idx = question_indices.index(q)
                    d_idx = document_indices.index(d)
                    recall_data[q_idx, d_idx] = recall

                for (q, d), f1 in f1_dict[context_index].items():
                    q_idx = question_indices.index(q)
                    d_idx = document_indices.index(d)
                    f1_data[q_idx, d_idx] = f1

                # 保存热图的文件路径
                precision_save_path = f'test/output/provenance/{baseline_name}/{dataset_name}_{model_name}_precision_heatmap_{context_index}.png'
                recall_save_path = f'test/output/provenance/{baseline_name}/{dataset_name}_{model_name}_recall_heatmap_{context_index}.png'
                # f1_save_path = f'test/output/provenance/{baseline_name}/{dataset_name}_{model_name}_f1_heatmap_{context_index}.png'

                os.makedirs(os.path.dirname(precision_save_path), exist_ok=True)

                # 绘制并保存 precision 热图
                plt.figure(figsize=(8, 8))
                sns.heatmap(precision_data, xticklabels=document_indices, yticklabels=question_indices, cmap='coolwarm', annot=True)
                plt.xlabel('Document Index')
                plt.ylabel('Question Index')
                plt.title(f'Precision Heatmap for {dataset_name} - {model_name} (Run {context_index})')
                plt.savefig(precision_save_path)
                plt.close()

                # 绘制并保存 recall 热图
                plt.figure(figsize=(8, 8))
                sns.heatmap(recall_data, xticklabels=document_indices, yticklabels=question_indices, cmap='coolwarm', annot=True)
                plt.xlabel('Document Index')
                plt.ylabel('Question Index')
                plt.title(f'Recall Heatmap for {dataset_name} - {model_name} (Run {context_index})')
                plt.savefig(recall_save_path)
                plt.close()

                print(f"Precision heatmap saved to {precision_save_path}")
                print(f"Recall heatmap saved to {recall_save_path}")


def robustness_heatmap_combined(baseline_name: str, dataset_names: list[str], model_names: list[str], content_index_list: list[int]):

    # Number of rows (metrics) and columns (datasets)
    rows = 2  # Precision and Recall for each row
    cols = len(dataset_names)  # Each dataset will have its own column

    # Create the figure with subplots
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10), constrained_layout=True)

    # Loop through datasets and models to fill the heatmaps for precision and recall
    # dataloading
    precision_dict = {} # {dataset_name: {model_name: {content_index: {(question_index, document_index): precision}}}}
    recall_dict = {}
    for col_idx, dataset_name in enumerate(dataset_names):
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
            file_paths = glob.glob(os.path.join(folder_path, '*.json'))
            # Initialize dictionaries to store precision and recall


            # Loop through JSON files and parse data
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content_list = json.load(file)
                    gt_evidence = []
                    for content_idx, content in enumerate(content_list):
                        if content_idx == 0:
                            gt_evidence = content["evidence"]
                            continue

                        evidence = content["evidence"]
                        precision = get_precision(evidence, gt_evidence)
                        recall = get_recall(evidence, gt_evidence)
                        question_index = content["question_id"]
                        document_index = content["document_id"]

                        # Save precision and recall for each content_index
                        if content_idx not in precision_dict:
                            precision_dict[content_idx] = {}
                            recall_dict[content_idx] = {}

                        precision_dict[content_idx][(question_index, document_index)] = precision
                        recall_dict[content_idx][(question_index, document_index)] = recall

            # Generate heatmap for precision and recall for the current dataset and model
            for context_idx in precision_dict.keys():
                # Get unique question and document indices
                question_indices = sorted(set([q for q, _ in precision_dict[context_idx].keys()]))
                document_indices = sorted(set([d for _, d in precision_dict[context_idx].keys()]))

                # Create 2D arrays for precision and recall
                precision_data = np.zeros((len(question_indices), len(document_indices)))
                recall_data = np.zeros((len(question_indices), len(document_indices)))

                # Fill precision and recall data arrays
                for (q, d), precision in precision_dict[context_idx].items():
                    q_idx = question_indices.index(q)
                    d_idx = document_indices.index(d)
                    precision_data[q_idx, d_idx] = precision

                for (q, d), recall in recall_dict[context_idx].items():
                    q_idx = question_indices.index(q)
                    d_idx = document_indices.index(d)
                    recall_data[q_idx, d_idx] = recall

                # Plot precision heatmap (1st row)
                sns.heatmap(precision_data, ax=axes[0, col_idx], cmap='coolwarm', annot=True, cbar=True)
                axes[0, col_idx].set_title(f'{dataset_name.capitalize()} - Precision')
                axes[0, col_idx].set_xlabel('Document Index')
                if col_idx == 0:
                    axes[0, col_idx].set_ylabel('Question Index (Precision)')

                # Plot recall heatmap (2nd row)
                sns.heatmap(recall_data, ax=axes[1, col_idx], cmap='coolwarm', annot=True, cbar=True)
                axes[1, col_idx].set_title(f'{dataset_name.capitalize()} - Recall')
                axes[1, col_idx].set_xlabel('Document Index')
                if col_idx == 0:
                    axes[1, col_idx].set_ylabel('Question Index (Recall)')

            # Save the combined figure
            combined_save_path = f'test/output/provenance/{baseline_name}_combined_heatmap_context_{context_index}.png'
            os.makedirs(os.path.dirname(combined_save_path), exist_ok=True)
            plt.savefig(combined_save_path)
            plt.close()

            print(f"Combined heatmap saved to {combined_save_path}")

                    

# def get_robustness(baseline_name: str, dataset_names: list[str], model_names: list[str]):

#     for dataset_name in dataset_names:
#         for model_name in model_names:
#             folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
#             file_paths = glob.glob(os.path.join(folder_path, '*.json'))

#             # 存储不同 context_index 的 evidence 和度量值
#             precision_dict = {}
#             recall_dict = {}
#             jaccard_dict = {}
#             score_dict = {}

#             # 依次读取每个JSON文件并解析为字典
#             for file_path in file_paths:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     content_list = json.load(file)
#                     gt_evidence = []
#                     for context_index, content in enumerate(content_list): 
#                         if context_index == 2: # choose as ground truth
#                             gt_evidence = content["evidence"]
#                             # 初始化 score_dict
#                             if context_index not in score_dict:
#                                 score_dict[context_index] = []
#                             score_dict[context_index].append(content["jaccard_similarity"])
#                             continue

#                     for context_index, content in enumerate(content_list): 
#                         if context_index == 2:
#                             continue
#                         # 记录每个文件的 evidence 和其他度量值
#                         evidence = content["evidence"]
#                         if context_index not in precision_dict:
#                             precision_dict[context_index] = []
#                             recall_dict[context_index] = []
#                             jaccard_dict[context_index] = []
#                             score_dict[context_index] = []
                        
#                         precision_dict[context_index].append(get_precision(evidence, gt_evidence))
#                         recall_dict[context_index].append(get_recall(evidence, gt_evidence))
#                         jaccard_dict[context_index].append(get_jaccard_sentences(evidence, gt_evidence))
#                         score_dict[context_index].append(content["jaccard_similarity"])

#             # 计算每个 context_index 的平均值
#             results = []
#             for context_index in precision_dict:
#                 ave_precision = sum(precision_dict[context_index]) / len(precision_dict[context_index])
#                 ave_recall = sum(recall_dict[context_index]) / len(recall_dict[context_index])
#                 ave_f1 = 2 * ave_precision * ave_recall / (ave_precision + ave_recall) if (ave_precision + ave_recall) != 0 else 0
#                 ave_jaccard = sum(jaccard_dict[context_index]) / len(jaccard_dict[context_index])
                
#                 result = {
#                     "baseline_name": baseline_name,
#                     "model_name": model_name,
#                     "dataset_name": dataset_name,
#                     "run_time": context_index,
#                     "average_precision": ave_precision,
#                     "average_recall": ave_recall,
#                     # "average_f1": ave_f1,
#                     "average_jaccard": ave_jaccard,
#                     # "prediction_number": len(precision_dict[context_index]),
#                 }
#                 results.append(result)

#             # 保存结果到JSON文件
#             file_path_to_save = f'test/output/provenance/{baseline_name}/robustness_result.json'
#             append_to_json_file(file_path_to_save, results)
#             # print(f"results: {results}")

def get_robustness(baseline_name: str, dataset_names: list[str], model_names: list[str]):
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            # 存储不同 context_index 的 evidence 和度量值
            precision_dict = {}
            recall_dict = {}
            jaccard_dict = {}
            score_dict = {}

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content_list = json.load(file)

                    # 遍历每个 context_index，将其作为 ground truth
                    for gt_context_index, gt_content in enumerate(content_list):
                        gt_evidence = gt_content["evidence"]

                        # 初始化 score_dict
                        if gt_context_index not in score_dict:
                            score_dict[gt_context_index] = []
                        score_dict[gt_context_index].append(gt_content["jaccard_similarity"])

                        # 对每个文件的 context_index，计算与 ground truth 的度量值
                        for context_index, content in enumerate(content_list):
                            if context_index == gt_context_index:
                                continue

                            # 记录每个文件的 evidence 和其他度量值
                            evidence = content["evidence"]
                            if context_index not in precision_dict:
                                precision_dict[context_index] = []
                                recall_dict[context_index] = []
                                jaccard_dict[context_index] = []
                                score_dict[context_index] = []

                            precision_dict[context_index].append(get_precision(evidence, gt_evidence))
                            recall_dict[context_index].append(get_recall(evidence, gt_evidence))
                            jaccard_dict[context_index].append(get_jaccard_sentences(evidence, gt_evidence))
                            score_dict[context_index].append(content["jaccard_similarity"])

            # 计算每个 context_index 对不同 ground truth 的平均值
            results = []
            for context_index in precision_dict:
                ave_precision = sum(precision_dict[context_index]) / len(precision_dict[context_index])
                ave_recall = sum(recall_dict[context_index]) / len(recall_dict[context_index])
                # ave_f1 = 2 * ave_precision * ave_recall / (ave_precision + ave_recall) if (ave_precision + ave_recall) != 0 else 0
                ave_jaccard = sum(jaccard_dict[context_index]) / len(jaccard_dict[context_index])
                
                result = {
                    "baseline_name": baseline_name,
                    "model_name": model_name,
                    "dataset_name": dataset_name,
                    "run_time": context_index,
                    "average_precision": ave_precision,
                    "average_recall": ave_recall,
                    # "average_f1": ave_f1,
                    "average_jaccard": ave_jaccard,
                    # "prediction_number": len(precision_dict[context_index]),
                }
                results.append(result)

            # 保存结果到JSON文件
            # file_path_to_save = f'test/output/provenance/{baseline_name}/robustness_result.json'
            # append_to_json_file(file_path_to_save, results)
            print(f"results: {results}")

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
                        raw_provenance = content["provenance"]
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


def clean_output_json(baseline_name:str, dataset_names:list[str], model_names:list[str]):

    # 获取文件夹内所有JSON文件的路径
    for dataset_name in dataset_names:
        for model_name in model_names:
            folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'

            file_paths = glob.glob(os.path.join(folder_path, '*.json'))

            # 依次读取每个JSON文件并解析为字典
            for file_path in file_paths:
                # 打开文件并读取内容
                content = []
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = json.load(file)
                    for dic in content:
                        dic["model_name"] = "gpt4turbo"
                    dic_to_save = content[0]
                    question_index = dic_to_save["question_id"]
                    document_index = dic_to_save["document_id"]
                    
                with open(f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/{baseline_name}_{model_name}_q{question_index}_d{document_index}.json', 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # baseline_names = ["baseline2_binary"]
    dataset_names = ['civic', 'paper', 'notice']
    model_names = ['gpt4turbo']
    question_sets = [civic_q(), paper_q(), notice_q()] # same index as dataset_names
    # document_path_sets = [civic_path(), paper_path(), notice_path()] # same index as dataset_names
    # check_uncertainty(baseline_names, dataset_names, model_names, question_sets)
    # for baseline_name in baseline_names:
    #     draw_average_result_all(baseline_name)
    # get_average_result_baseline2("baseline2_greedy_gt", dataset_names, model_names)
    # for baseline_name in baseline_names:
    #     clean_output_json(baseline_name, dataset_names, model_names)
    # get_robustness("baseline2_greedy", dataset_names, model_names)
    # compression_rate_heatmap("baseline2_greedy", dataset_names, model_names)
    # robustness_heatmap_combined("baseline2_greedy", dataset_names, model_names)
    get_average_result_baseline2("baseline1_gt", dataset_names, model_names)
