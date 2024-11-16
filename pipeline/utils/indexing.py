import glob, logging
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, PyPDFLoader, PyPDFium2Loader
from langchain.schema import Document
from pipeline.utils.tokenizer import nltk_sent_tokenize

def path_raw2extracted(input_string):
    """
    Converts the given input string from 'raw_data' to 'extracted_data'.

    Parameters:
    input_string (str): The input string to be converted.

    Returns:
    str: The converted string.
    """
    if 'raw_data' in input_string:
        converted_string = input_string.replace('raw_data', 'extracted_data')
    else:
        raise ValueError("The input string does not contain 'raw_data'")
    if converted_string.endswith('.pdf'):
        converted_string = converted_string[:-4] + '.txt'
    return converted_string
    
def path_extracted2raw(input_string):
    """
    Converts the given input string from 'extracted_data' to 'raw_data'.

    Parameters:
    input_string (str): The input string to be converted.

    Returns:
    str: The converted string.
    """
    if 'extracted_data' in input_string:
        converted_string = input_string.replace('extracted_data', 'raw_data')
    else:
        raise ValueError("The input string does not contain 'extracted_data'")
    if converted_string.endswith('.txt'):
        converted_string = converted_string[:-4] + '.pdf'
    return converted_string

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
    loader = PyPDFium2Loader(file_path)
    docs = loader.load_and_split()
    return docs

def load_local_pdf_as_one_page(file_path):
    '''
    Input: file_path, str
    Output: doc, class Document
    '''
    # Load the PDF document
    loader = PyPDFium2Loader(file_path)
    doc = loader.load()
    
    # Concatenate the contents of each page
    full_content = ""
    for page in doc:
        full_content += page.page_content + "\n"  # Add a newline to separate pages
    
    # Create a single Document with the concatenated content
    combined_doc = Document(page_content=full_content)
    
    return combined_doc


def split_docs(docs, chunk_size=1000, chunk_overlap=0, add_start_index=True, separators=["\n\n", ".\n", ". "]):
    '''
    Input: docs, list of class Document
    Output: all_splits, list of class Document

    At a high level, text splitters work as following:

    Split the text up into small, semantically meaningful chunks (often sentences).
    Start combining these small chunks into a larger chunk until you reach a certain size (as measured by some function).
    Once you reach that size, make that chunk its own piece of text and then start creating a new chunk of text with some overlap (to keep context between chunks).
    That means there are two different axes along which you can customize your text splitter:

    How the text is split
    How the chunk size is measured
    '''

    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=add_start_index, separators=separators
    )
    all_splits = text_splitter.split_documents(docs)

    # Add index to each chunk's metadata
    for i, split in enumerate(all_splits):
        split.metadata['chunk_index'] = i

    logging.info(f"Split {len(docs)} documents into {len(all_splits)} chunks")

    all_splits_len = [len(split.page_content) for split in all_splits]
    logging.info(f"all splits length: {all_splits_len}")
    logging.info(all_splits)

    return all_splits

def store_splits(all_splits, collection_name="_LANGCHAIN_DEFAULT_COLLECTION_NAME"):
    ''' 
    Input: all_splits, list of class Document
    Output: vectorstore, class Chroma
    '''
    
    from langchain_chroma import Chroma
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    
    # Create vectorstore
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(model="text-embedding-3-small"), ids=[str(i) for i in range(len(all_splits))], collection_metadata={"hnsw:space": "cosine"}, collection_name=collection_name)
    return vectorstore

def get_index_by_similarity(texts: str, question: str) -> list:
    sentences = nltk_sent_tokenize(texts)
    # get the index list by relevance
    all_splits = [Document(page_content=s, metadata={"source": "local"}) for s in sentences]
    vector_store = store_splits(all_splits, "reverse_search")
    ranked_documents = vector_store.similarity_search(question, k=99999)
    vector_store.delete_collection()
    ranked_sentences = [doc.page_content for doc in ranked_documents] # is from most relevanct to least relevant
    # get the index of ranked_sentences in sentences
    relevance_index = [] # is from most relevanct to least relevant
    for sen in ranked_sentences:
        relevance_index.append(sentences.index(sen))
    reverse_index = relevance_index[::-1]
    return reverse_index