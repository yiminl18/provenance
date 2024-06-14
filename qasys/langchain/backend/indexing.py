import glob, logging
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain.schema import Document

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
            docs, a list of class Document
    '''
    docs = []
    loader = TextLoader(file_path)
    doc = loader.load()[0]
    docs.append(doc)
    return docs

def load_local_pdf(file_path):
    '''
    Input: file_path, str
    Output: doc, class Document
    '''
    docs = []
    loader = PyMuPDFLoader(file_path)
    docs = loader.load_and_split()
    return docs

def load_local_pdf_as_one_page(file_path):
    '''
    Input: file_path, str
    Output: doc, class Document
    '''
    # Load the PDF document
    loader = PyMuPDFLoader(file_path)
    doc = loader.load()
    
    # Concatenate the contents of each page
    full_content = ""
    for page in doc:
        full_content += page.page_content + "\n"  # Add a newline to separate pages
    
    # Create a single Document with the concatenated content
    combined_doc = Document(page_content=full_content)
    
    return combined_doc


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

    logging.info(f"Split {len(docs)} documents into {len(all_splits)} chunks")

    return all_splits

def store_splits(all_splits):
    ''' 
    Input: all_splits, list of class Document
    Output: vectorstore, class Chroma
    '''
    
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings

    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
    # num_documents = vectorstore.count()  # Assuming `len` returns the number of documents
    # logging.info(f"Number of documents stored in Chroma: {num_documents}")
    return vectorstore

# def store_splits(all_splits):
#     ''' 
#     Input: all_splits, list of class Document
#     Output: vectorstore, class Chroma
#     '''
    
#     from langchain_chroma import Chroma
#     from langchain_openai import OpenAIEmbeddings
    
#     # Create vectorstore
#     vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
#     embeddings = vectorstore.embeddings
#     logging.info("type of embeddings: " + str(type(embeddings)))
#     # logging.info(f"Stored {len(embeddings)} embeddings in the vectorstore")
#     # unique_embeddings = set(tuple(embed) for embed in embeddings)
#     # if len(unique_embeddings) != len(embeddings):
#     #     print("数据集中有重复的 embedding")
#     return vectorstore



# print(load_local_pdf('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf'))
# print(load_local_txt('data/civic/txt_data/malibucity_agenda__01272021-1626.txt'))
# print(len(load_local_pdf_as_one_page('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')))
# print(len(load_local_pdf('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')))
# print(len(load_local_txt('data/civic/txt_data/malibucity_agenda__01272021-1626.txt')))
