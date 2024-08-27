# 获取文件夹内所有JSON文件的路径
import os, glob, json
from nltk import word_tokenize
from questions import civic_q, paper_q, notice_q, civic_path, paper_path, notice_path

baseline_names = ['baseline0', 'baseline1_0.4', 'baseline1_0.5', 'baseline1_0.6', 'baseline1_0.7', 'baseline1_0.8', 'baseline2']
baseline_types = [0, 1, 1, 1, 1, 1, 2]
dataset_names = ['civic','paper','notice']
question_set = [civic_q(), paper_q(), notice_q()] # same index as dataset_names
document_path_set = [civic_path(), paper_path(), notice_path()] # same index as dataset_names
model_names = ['gpt4o']

def insert_layer(input_str, layer_to_insert, after_segment):
    # 找到需要插入的位置
    index = input_str.find(after_segment) + len(after_segment)
    
    # 插入新的层级
    new_str = input_str[:index] + layer_to_insert + input_str[index:]
    
    return new_str

def append_to_json_file(file_path, data_to_append):
    # 如果文件不存在，初始化一个空列表
    if not os.path.exists(file_path):
        existing_data = []
    else:
        # 读取现有文件内容
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

    # 将新数据添加到现有数据中
    if isinstance(existing_data, list):
        existing_data.append(data_to_append)
    elif isinstance(existing_data, dict):
        existing_data.update(data_to_append)

    # 将合并后的数据写回文件
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)



# print(f"baseline_name: {baseline_name}, total file number: {len(length_of_provenance)}")

def compare_q():
    for baseline_name in baseline_names:
        for model_name in model_names:
            for dataset_index, dataset_name in enumerate(dataset_names):
                folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
                file_paths = glob.glob(os.path.join(folder_path, '*.json'))
                # # 依次读取每个JSON文件并解析为字典
                for file_path in file_paths:
                    # 打开文件并读取内容
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # print(f"file_path: {file_path}")
                        content = json.load(file)
                        content["file_path"] = file_path
                        question = content["question"]
                        question_index = question_set[dataset_index].index(question) #
                        baseline_type = content["baseline_type"] #
                        document_path = content["document_path"]
                        document_path_index = document_path_set[dataset_index].index(document_path) #
                        # raw_provenance = content["raw_provenance"]
                        # evidence = content["evidence"]
                        # raw_answer = content["raw_answer"]
                        # evidence_answer = content["evidence_answer"]
                        # search_pool = content["search_pool"]
                        file_path_to_save = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}/labeled_file/b{baseline_type}_{dataset_name}_{model_name}_q{question_index}_d{document_path_index}.json'
                        append_to_json_file(file_path_to_save, content)

def clean_baseline2():
    for baseline_name in ['baseline2']:
        for model_name in model_names:
            for dataset_index, dataset_name in enumerate(dataset_names):
                folder_path = f'test/output/provenance/{baseline_name}/{dataset_name}/{model_name}'
                file_paths = glob.glob(os.path.join(folder_path, '*.json'))
                
                # # 依次读取每个JSON文件并解析为字典
                for file_path in file_paths:
                    # 打开文件并读取内容
                    content = {}
                    with open(file_path, 'r', encoding='utf-8') as file:
                        # print(f"file_path: {file_path}")
                        content = json.load(file)
                        # if 'jasccard_similarity' in content:
                        #     del content['jasccard_similarity']
                    # if not content['index_to_delete']:
                        # content['evidence_answer'] = content['raw_answer']
                        # content['jaccard_similarity'] = 1
                    content['baseline_type'] = 2
                    # modify the opened file
                    with open(file_path, 'w') as file:
                        json.dump(content, file, indent=4)


# compare_q()
clean_baseline2()
