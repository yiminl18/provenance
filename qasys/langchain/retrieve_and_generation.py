from collections import Counter

def most_frequent_element(input_list):
    """
    Returns the most frequent element in the input list.
    If there are multiple elements with the same highest frequency, 
    one of them will be returned.

    Parameters:
    input_list (list): A list of elements.

    Returns:
    element: The most frequent element in the list.
    """
    # Count the frequency of each element in the list
    counter = Counter(input_list)
    
    # Return the most common element
    return counter.most_common(1)[0][0]

def retrieve_and_generation(question, vectorstore, k = 6, evaluation_instruction = "", model_name='gpt4turbo'):
    '''
    Input : question, str
            folder_path, str
            chunk_size, int
            chunk_overlap, int
            add_start_index, bool
    Output: final_answer, str
            retrieved_docs
    evaluation_instruction is only for evaluation step, as an additional prompt. Cna be specified for individual questions.
    '''
    
    # Load and split documents
    

    # Retrieve
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

    # see how retrieve works 
    retrieved_docs = retriever.invoke(question)

    # Get chunk indices of retrieved documents
    retrieved_chunk_indices = [doc.metadata.get('chunk_index', -1) for doc in retrieved_docs]

    # generate

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Intercept the prompt before it is sent to the LLM
    formatted_docs = format_docs(retrieved_docs)
    provenance = ([doc.page_content for doc in retrieved_docs]) # retrieved_docs is a list of list of strings
    
    return generate_from_evidence(question+evaluation_instruction, provenance, model_name), retrieved_docs, retrieved_chunk_indices, ""

# version 0
# def generate_from_evidence(question, evidence):
#     '''
#     Input: question, str
#             evidence, list of str
#     Output: final_answer, str
#     '''
#     from model import model
#     system = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise."""
#     question_for_evaluation = question+' Only return the answer required by the question. There is no need to include extra information such as reasons. Separate the answers with commas if there are multiple items. Return None if no answer is found.'
#     evidence_str = '\n\n'.join(evidence)
#     text = f"""Question: {question_for_evaluation}\n\nContext: {evidence_str}\n\nAnswer: """
#     prompt = (system, text)
#     final_answer = model('gpt35', prompt)
#     return final_answer
# print(retrieve_and_generation(question))

# version 1
def generate_from_evidence(question:str, evidence:list[str], model_name='gpt4o'):
    '''
    Input: question, str
            evidence, list of str
    Output: final_answer, str
    '''
    from model import model
    system = """ You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use a maximum of three sentences and keep the answer concise."""
    # system = """ You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. Different pieces of retrieved context are seperated by '||' delimiter. If you don't know the answer, just say that you don't know. Use a maximum of three sentences and keep the answer concise."""
    question_for_evaluation = question+' Only return the answer without any explanations. Separate the answers with commas if there are multiple items. Return None if no answer is found. Please answer this question based on the following description, which contains a set of evidences to help answer the question.'
    # evidence_str = '\n\n'.join(evidence)
    evidence_str = ' '.join(evidence)
    text = f""" Question: {question_for_evaluation}\n\nRetrieved context: {evidence_str}\n\nAnswer: """
    prompt = (system, text)
    # final_answers = []
    # for i in range(10):
    #     final_answers.append(model('gpt4turbo', prompt))
    # print(final_answers)
    return model(model_name, prompt) # a dict, "content", "input_tokens", "output_tokens", "cost"


# evidence = \
# [
#             "CHI 2010, April 10\u201315, 2010, Atlanta, Georgia, USA. Copyright 2010 ACM  978-1-60558-929-9/10/04....$10.00.",
#             "Ubicomp\u201906,  2006,  pp. 177-193. 11. Hsieh, G., Li, I., Dey, A., Forlizzi, J., and Hudson, S.E.",
#             "IEEE Transactions on Visualization and \nComputer Graphics, 2002, pp. 1145-1152.",
#             "Journal of Happiness Studies, 4, 2003, pp. 5-34. 21.",
#             "Wired,  17.07, \n2009, pp. 92-95. 22. Yau,  N. and Schneider,  J.  Self-Surveillance.",
#             "Bulletin of \n\nASIS&T, June/July 2009, pp. 24-30.",
#             "CHI 2010: Performance, Stagecraft, and MagicApril 10\u201315, 2010, Atlanta, GA, USA566",
#             "1-10. 3. Consolvo,  S.,  McDonald,  D.W.,  Toscos,  T.,  et  al.",
#             "CHI\u201808, 2008, pp. 1797-1806. 4. Froehlich, J., Dillahunt, T., Klasnja, P., et al.",
#             "Communications  of \nthe ACM, 2006, pp. 88-95."
#         ]
question = "Does this paper involve the theory \"A Model of Personal Informatics\"?"
evaluation_instruction = " Return yes or no."
evidence = [
            "Proceedings of \nthe ACM conference on Computer Supported \nCooperative Work (CSCW 2012): 853. \nhttp://doi.org/10.1145/2145204.2145331 \n\n28.",
            "Jina Huh, Leslie S Liu, Tina Neogi, Kori Inkpen, and \n\nWanda Pratt.",
            "2014. Health Vlogs as Social Support for \nChronic Illness Management.",
            "ACM Transactions on \nComputer-Human Interaction (TOCHI) 21, 4: 23. \nhttp://doi.org/10.1145/2630067 \n\n29.",
            "Ian Li, Anind Dey, and Jodi Forlizzi. 2010. A Stage-\nBased Model of Personal Informatics Systems."
        ]
from models.gpt_4o import gpt_4o
from models.gpt_4_turbo import gpt_4_turbo
from models.gpt_4o_mini import gpt_4o_mini
gpt_4o.call_count = 0
gpt_4_turbo.call_count = 0
gpt_4o_mini.call_count = 0
for i in range(20):
    print(f"Run time : ", generate_from_evidence(question + evaluation_instruction, evidence, model_name = "gpt4o"))