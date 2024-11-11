
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
            evidence_token_number_list = []
            provenance_token_number_list = []

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
                    provenance = content["provenance"]
                    evidence_token_number_list.append(get_token_num_for_list(content["evidence"]))
                    provenance_token_number_list.append(get_token_num_for_list(content["provenance"]))
                    # evidence_sentence_number.append(len(content["evidence"]))
                    
            result = {
                "baseline_name": baseline_name,
                "model_name": model_name,
                "dataset_name": dataset_name,
                "average_jaccard_similarity": sum(scores) / len(scores),
                "average_sentence_number": len(evidence) / len(evidence_token_number_list),
                # "accuracy": len(success_scores) / len(scores),
                "average_len_of_success_evidence": get_token_num_for_list(evidence) / len(evidence),
                "compression_rate": sum( e / p for e, p in zip(evidence_token_number_list, provenance_token_number_list)) / len(evidence_token_number_list)
                # "average_sentence_number_of_success_evidence": sum(success_evidence_sentence_number) / len(success_evidence_sentence_number)
            }

            file_path_to_save = f'test/output/provenance/{baseline_name}/average_result.json'
            append_to_json_file(file_path_to_save, result)