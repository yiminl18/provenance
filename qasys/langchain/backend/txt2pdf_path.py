import re, os

def txt2pdf_path(input_str):

    # 替换路径中的部分和文件扩展名
    output_str = re.sub(r'extracted_data/(.*)\.txt', r'raw_data/\1.pdf', input_str)

    # print(output_str)
    return os.path.abspath(output_str)

def txt2pdf_path_list(input_list):
    return [txt2pdf_path(input_str) for input_str in input_list]
