import os
import re

def remove_cid_texts(folder_path):
    # 正则表达式模式，用于匹配形如 (cid:数字) 的文本
    pattern = re.compile(r'\(cid:\d+\) ')

    # 遍历文件夹内所有 .txt 文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 替换所有匹配的文本
            new_content = re.sub(pattern, '', content)
            
            # 将修改后的内容写回文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)

# 使用函数时，传入目标文件夹路径
folder_path = 'data/civic/txt_data'
remove_cid_texts(folder_path)
