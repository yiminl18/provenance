import os
import json

def replace_spaces_in_keys(json_obj):
    if isinstance(json_obj, dict):
        new_obj = {}
        for k, v in json_obj.items():
            new_key = k.replace(' ', '_')
            new_obj[new_key] = replace_spaces_in_keys(v)
        return new_obj
    elif isinstance(json_obj, list):
        return [replace_spaces_in_keys(item) for item in json_obj]
    else:
        return json_obj

def process_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            updated_data = replace_spaces_in_keys(data)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)

folder_path = 'test/output/provenance/baseline1/notice/gpt4o'  # 替换为实际文件夹路径
process_json_files(folder_path)