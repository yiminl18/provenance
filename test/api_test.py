from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex


def read_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def load_data(text_file):
    reader = SimpleDirectoryReader(input_files=[text_file])
    return reader.load_data()

def simple_test():
    file = read_text('/Users/yiminglin/Documents/Codebase/TextDB/Text-DB/data/paper/extracted_data/A Lived Informatics Model of Personal Informatics.txt')
    data = load_data(file)
    index = VectorStoreIndex.from_documents(data)
    query_engine = index.as_query_engine()
    response = query_engine.query('What is the publication year of this paper? Only return a single number. If cannot find, return "None" .')
    print(response)

simple_test()