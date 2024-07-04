import re, os

# def txt2pdf_path(input_str):

#     # 替换路径中的部分和文件扩展名
#     output_str = re.sub(r'data/civic/txt_data/(.+?)\.txt',
#                     r'https://zhujuneray.github.io/assets/provenance/data/civic/raw_data/\1.pdf',
#                     input_str)

#     # print(output_str)
#     # return os.path.abspath(output_str)
#     return output_str

def txt2pdf_path(input_str):
    # Use a regular expression to capture the folder name and the file name
    match = re.search(r'data/([^/]+)/txt_data/(.+?)\.txt', input_str)
    
    if match:
        folder_name = match.group(1)
        file_name = match.group(2)
        # Create the output path using the captured folder name and file name
        output_str = f'https://zhujuneray.github.io/assets/provenance/data/{folder_name}/raw_data/{file_name}.pdf'
        return output_str
    else:
        return None

# def pdf2pdf_path(input_str):

#     # 替换路径中的部分和文件扩展名
#     output_str = re.sub(r'data/civic/raw_data/(.+?)\.pdf',
#                     r'https://zhujuneray.github.io/assets/provenance/data/civic/raw_data/\1.pdf',
#                     input_str)

#     # print(output_str)
#     # return os.path.abspath(output_str)
#     return output_str


def pdf2pdf_path(input_str):
    # Use a regular expression to capture the folder name and the file name
    match = re.search(r'data/([^/]+)/raw_data/(.+?)\.pdf', input_str)
    
    if match:
        folder_name = match.group(1)
        file_name = match.group(2)
        # Create the output path using the captured folder name and file name
        output_str = f'https://zhujuneray.github.io/assets/provenance/data/{folder_name}/raw_data/{file_name}.pdf'
        return output_str
    else:
        return None

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
