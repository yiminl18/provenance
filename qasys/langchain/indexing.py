import glob
from langchain_community.document_loaders import TextLoader

def sample_folders():
    q = []
    q.append("data/civic/extracted_data") # Civic
    q.append("data/paper/extracted_data") # Paper
    

    return q 

def load_local_folder_of_txt(folder_path = "data/civic/extracted_data"):
    '''
    Input: folder_path, str
    Output: docs, list of class Document
    '''
    
    # get all txt files in the folder
    txt_files = glob.glob(folder_path+"/*.txt")

    docs = []

    for file in txt_files:
        loader = TextLoader(file)
        docs.append(loader.load()[0])

    # docs is a list of class documents
    return docs

def load_local_txt(file_path):
    '''
    Input: file_path, str
    Output: doc, class Document
    '''
    docs = []
    loader = TextLoader(file_path)
    doc = loader.load()[0]
    docs.append(doc)
    return docs


def split_docs(docs, chunk_size=1000, chunk_overlap=200, add_start_index=True):
    '''
    Input: docs, list of class Document
    Output: all_splits, list of class Document
    '''

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=add_start_index
    )
    all_splits = text_splitter.split_documents(docs)

    # # see how chunk works
    # with open("output.txt", "w", encoding="utf-8") as file:
    #     for split in all_splits:
    #         file.write("chunk_data: ")
    #         file.write (str(split.metadata) + "\n")
    #         file.write(split.page_content + "\n----------chunk_end--------\n")
    # print(len(all_splits)) # print number of chunks
    return all_splits

def store_splits(all_splits):
    '''
    Input: all_splits, list of class Document
    Output: vectorstore, class Chroma
    '''
    
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings

    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
    return vectorstore