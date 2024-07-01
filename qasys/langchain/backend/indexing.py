import glob, logging
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, PyPDFLoader, PyPDFium2Loader
from langchain.schema import Document

def sample_folders():
    q = []
    q.append("data/civic/extracted_data") # Civic
    q.append("data/paper/extracted_data") # Paper
    

    return q 

def civic_path():
    q = []
    q.append('data/civic/raw_data/malibucity_agenda__01262022-1835.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03022021-1648.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03232022-1869.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__03242021-1665.pdf')
    q.append('data/civic/raw_data/malibucity_agenda__04282021-1687.pdf')
    return q

def paper_path():
    q = []
    q.append('data/paper/raw_data/A Lived Informatics Model of Personal Informatics.pdf')
    q.append('data/paper/raw_data/A Stage-based Model of Personal Informatics Systems.pdf')
    q.append('data/paper/raw_data/A Trip to the Moon: Personalized Animated Movies for Self-reflection.pdf')
    q.append('data/paper/raw_data/A Wee Bit More Interaction: Designing and Evaluating an Overactive Bladder App.pdf')
    q.append('data/paper/raw_data/ArmSleeve: A Patient Monitoring System to Support Occupational Therapists in Stroke Rehabilitation.pdf')
    q.append('data/paper/raw_data/Barriers and Negative Nudges: Exploring Challenges in Food Journaling.pdf')
    q.append('data/paper/raw_data/Barriers to Engagement with a Personal Informatics Productivity Tool.pdf')
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


def split_docs(docs, chunk_size=1000, chunk_overlap=0, add_start_index=True):
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
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=add_start_index, separators=["\n\n", ". \r\n", "\n", " ", ""]
    )
    all_splits = text_splitter.split_documents(docs)

    # Add index to each chunk's metadata
    for i, split in enumerate(all_splits):
        split.metadata['chunk_index'] = i

    # # see how chunk works
    # with open("output.txt", "w", encoding="utf-8") as file:
    #     for split in all_splits:
    #         file.write("chunk_data: ")
    #         file.write (str(split.metadata) + "\n")
    #         file.write(split.page_content + "\n----------chunk_end--------\n")
    # print(len(all_splits)) # print number of chunks

    logging.info(f"Split {len(docs)} documents into {len(all_splits)} chunks")

    all_splits_len = [len(split.page_content) for split in all_splits]
    logging.info(f"all splits length: {all_splits_len}")
    # logging.info(all_splits)

    return all_splits

# def store_splits(all_splits):
#     ''' 
#     Input: all_splits, list of class Document
#     Output: vectorstore, class Chroma
#     '''
    
#     from langchain_chroma import Chroma
#     from langchain_pinecone import PineconeVectorStore
#     from langchain_openai import OpenAIEmbeddings

  
#     pc = PineconeVectorStore()
#     embeddings = OpenAIEmbeddings()
#     index_name = "my-index"
#     namespace = "my-namespace"
#     vectorstore = Pinecone(
#         index_name=index_name,
#         embedding=embedding,
#         namespace=namespace,
#     )
#     pc.delete(delete_all=True)
    
#     vectorstore = pc.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), ids=[str(i) for i in range(len(all_splits))], index_name="civic")

#     return vectorstore
#TODO: don't know how to delete in langchian, diff from the official one




def store_splits(all_splits):
    ''' 
    Input: all_splits, list of class Document
    Output: vectorstore, class Chroma
    '''
    
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    
    # Create vectorstore
    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), ids=[str(i) for i in range(len(all_splits))])
    embedding_vectors = vectorstore._collection.get(include=['embeddings']).get('embeddings')
    if len(embedding_vectors) != len(set(tuple(embed) for embed in embedding_vectors)):
        raise ValueError("Repeated embedding found in dataset")
    return vectorstore



# print(load_local_pdf('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf'))
# print(load_local_txt('data/civic/txt_data/malibucity_agenda__01272021-1626.txt'))
# print(len(load_local_pdf_as_one_page('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')))
# print(len(load_local_pdf('data/civic/raw_data/malibucity_agenda__01272021-1626.pdf')))
# print(len(load_local_txt('data/civic/txt_data/malibucity_agenda__01272021-1626.txt')))
for doc in load_local_pdf('data/paper/raw_data/A Trip to the Moon: Personalized Animated Movies for Self-reflection.pdf'):
    print(doc)