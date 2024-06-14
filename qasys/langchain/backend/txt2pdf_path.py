import re, os

def txt2pdf_path(input_str):

    # 替换路径中的部分和文件扩展名
    output_str = re.sub(r'data/civic/txt_data/(.+?)\.txt',
                    r'https://zhujuneray.github.io/assets/provenance/data/civic/raw_data/\1.pdf',
                    input_str)

    # print(output_str)
    # return os.path.abspath(output_str)
    return output_str

def pdf2pdf_path(input_str):

    # 替换路径中的部分和文件扩展名
    output_str = re.sub(r'data/civic/raw_data/(.+?)\.pdf',
                    r'https://zhujuneray.github.io/assets/provenance/data/civic/raw_data/\1.pdf',
                    input_str)

    # print(output_str)
    # return os.path.abspath(output_str)
    return output_str

def local2online_path(input_str):

    # 替换路径中的部分和文件扩展名
    output_str = re.sub(r'data/civic/raw_data/(.+?)\.pdf',
                    r'https://zhujuneray.github.io/assets/provenance/data/civic/raw_data/\1.pdf',
                    input_str)

    # print(output_str)
    # return os.path.abspath(output_str)
    return output_str

def txt2pdf_path_list(input_list):
    return [txt2pdf_path(input_str) for input_str in input_list]
