from model import model
from pipeline.utils.tokenizer import get_token_num, nltk_sent_tokenize
from pipeline.utils.similarity import get_jaccard_similarity
from pipeline.baseline.template import llm_query_example

# ask llm to choose evidence sentences from given context list, use few shot prompt
def llm_query(Q: str, A: str, P: str, model_name = 'gpt4omini') -> list[str]:
    prompt = f"""
    Given a question, and the answer to the question, and a list of relevant context sentences,
    Return a set of sentences from the relevant context that can provide evidence for the given answer to the given question.
    These evidence sentences must be CHOSEN from the given context list, meaning that they must be EXACTLY the same as the sentence elements in the context list.
    Each returned evidence sentence must not be edited, say no omission, no addition, no modification.
    The number of evidences should be as few as possible, being the most concise and informative.
    Concatenate multiple evidences to a string in sequence. If no evidence can be found, return None.
    """ + \
    f"""
    For example, if the question is {llm_query_example.example_Q()},
    the answer is {llm_query_example.example_A()}, 
    and the context is: {preprocess_P(llm_query_example.example_P())}.
    So the expected output should be: {llm_query_example.example_output()}
    which can not start from the middle of a context element, can not end in the middle of a context element.
    """ + \
    f"""
    Now consider the following question, answer and context:
    ###{Q}##
    ###{A}###
    ###{preprocess_P(P)}###
    Your output here:
    """

    print(prompt)
    
    result = model(model_name,prompt)
    print(result)
    filtered_result_list = clean_llm_result(result, P)
    
    return filtered_result_list

def clean_llm_result(result: str, reference: str, similarity_threshold: float = 0.7) -> str:
    # 1. Remove empty strings
    None_list = ['None', 'none', 'NONE', 'None.', '##None##', 'None##', '##None', 'None##.', '##None##.', 'None.', 'None.##', '##None.'] # list of strings that should be considered as empty
    if result in None_list:
        result =''
        return ''
    
    # 2. Avoid hallucination
    original_result_list = nltk_sent_tokenize(result, 10)
    filtered_result_list = []
    for r in original_result_list: # check if response is choosing the reference
        if get_jaccard_similarity(r, reference, 'intersection') > similarity_threshold:
            # check format, remove prefix
            prefix_to_remove = '- '
            r = r[len(prefix_to_remove):] if r.startswith(prefix_to_remove) else r
            filtered_result_list.append(r)

    return filtered_result_list

def preprocess_P(P: str) -> str:
    P_sent_list = nltk_sent_tokenize(P)
    P_sent_list_str = repr(P_sent_list) # explicitly convert to string, show to LLM
    return P_sent_list_str
