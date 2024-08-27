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

def retrieve_and_generation(question, vectorstore, k = 6, evaluation_instruction = ""):
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
    
    return generate_from_evidence(question+evaluation_instruction, provenance), retrieved_docs, retrieved_chunk_indices, ""

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
def generate_from_evidence(question:str, evidence:list[str]):
    '''
    Input: question, str
            evidence, list of str
    Output: final_answer, str
    '''
    from model import model
    system = """ You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. Different pieces of retrieved context are seperated by '||' delimiter. If you don't know the answer, just say that you don't know. Use a maximum of three sentences and keep the answer concise."""
    question_for_evaluation = question+' Only return the answer without any explanations. Separate the answers with commas if there are multiple items. Return None if no answer is found. Please answer this question based on the following description, which contains a set of evidences to help answer the question.'
    # evidence_str = '\n\n'.join(evidence)
    evidence_str = '||'.join(evidence)
    text = f""" Question: {question_for_evaluation}\n\n{evidence_str}\n\nAnswer: """
    prompt = (system, text)
    # final_answers = []
    # for i in range(10):
    #     final_answers.append(model('gpt4turbo', prompt))
    # print(final_answers)
    return model('gpt4turbo', prompt)


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
# question = "What is the publication year of this paper?"
# evaluation_instruction = " Return only a number."
# evidence = [
#         "19. Pousman,  Z.,  Stasko,  J.T.,  and  Mateas,  M.  Casual \nInformation  Visualization:  Depictions  of  Data \nin \nEveryday Life.",
#         "IEEE Transactions on Visualization and \nComputer Graphics, 2002, pp. 1145-1152.",
#         "20. Scollon,  C.,  Kim-Prieto,  C.,  and  Diener,  E.  Experience \nSampling:  Promises  and  Pitfalls,  Strengths  and \nWeaknesses.",
#         "Journal of Happiness Studies, 4, 2003, pp. 5-34. 21.",
#         "Wolf,  G.  Know  Thyself:  Tracking  Every  Facet  of  Life, \nfrom  Sleep  to  Mood  to  Pain,  24/7/365.",
#         "Wired,  17.07, \n2009, pp. 92-95. 22. Yau,  N. and Schneider,  J.  Self-Surveillance.",
#         "Bulletin of \n\nASIS&T, June/July 2009, pp. 24-30.",
#         "CHI 2010: Performance, Stagecraft, and MagicApril 10–15, 2010, Atlanta, GA, USA566",
#         "Permission  to  make  digital  or  hard  copies  of  all  or  part  of  this  work  for \npersonal or classroom use is granted without fee provided that copies are \nnot made or distributed for profit or commercial advantage and that copies \nbear this notice and the full citation on the first page.",
#         "To copy otherwise, \nor  republish,  to  post  on  servers  or  to  redistribute  to  lists,  requires  prior \nspecific permission and/or a fee.",
#         "CHI 2010, April 10–15, 2010, Atlanta, Georgia, USA. Copyright 2010 ACM  978-1-60558-929-9/10/04....$10.00.",
#         "to \n\ninformation  brought  by \n\nbecause  of  advances  in  sensor  technologies,  ubiquity  of \nthe  Internet,  and \naccess \nimprovements  in  visualizations.",
#         "A  class  of  systems  called \npersonal  informatics  is  appearing  that  help  people  collect \nand \n(e.g.,  Mint, \nhttp://mint.com, for finance and Nike+, http://nikeplus.com, \nfor physical activity). reflect  on  personal \n\ninformation \n\ninform  people  about",
#         "8. Gemmell,  J. &  Vemuri,  S.  \"CARPE  Research  Area.\" SIGMM. Accessed \nat \n2010 \non \nhttp://www.sigmm.org/Members/jgemmell/CARPE \n9.",
#         "Hallnäs,  L.  and  Redström,  J. Slow  Technology: \nDesigning  for  Reflection.",
#         "Personal  and  Ubiquitous \nComputing, 5(3), 2001. January \n\n6, \n\n10.",
#         "Hodges, S., Williams, L., Berry, E., et al., K. SenseCam: \na  Retrospective  Memory  Aid.",
#         "Ubicomp’06,  2006,  pp. 177-193. 11. Hsieh, G., Li, I., Dey, A., Forlizzi, J., and Hudson, S.E.",
#         "in \nto \n\nUsing  Visualizations \nExperience Sampling. Ubicomp’08, 2008, pp.",
#         "164-167. 12. Intille,  S.S.,  Tapia,  E.M.,  Rondoni,  J.,  et  al.",
#         "Tools  for \nStudying Behavior and Technology in Natural Settings. Ubicomp’03, 2003, pp.",
#         "157-174. Increase  Compliance \n\n13. Jones,  W.,  and  Teevan,  J.",
#         "Personal  Information \n\nManagement. UW Press, 2007.",
#         "CHI 2010: Performance, Stagecraft, and MagicApril 10–15, 2010, Atlanta, GA, USA562 \n\fCascading  barriers  suggest  that  a  holistic  approach  to  the \ndesign of personal informatics systems is critical.",
#         "Focusing \nonly on one stage ignores the whole experience of the user \nwith  the  system.",
#         "While  we  can  take  inspiration  from \ndifferent  fields  to  resolve  barriers  within  each  stage  (e.g., \nvisualization  techniques  from  information  visualization \nresearch), creating an effective personal informatics system \nrequires the consideration of all of the system's parts.",
#         "In  the  next  section,  we  provide  a  working  definition  of \npersonal  informatics  and  review  related  literature.",
#         "We \npresent  the  method  and  findings  from  our  survey,  and  use \nthem \nintroduce  a  stage-based  model  of  personal \ninformatics  systems.",
#         "We  describe  the  barriers  encountered \nin  each  stage  and  highlight  opportunities  for  intervention \nwithin  each  stage.",
#         "We  also  compare  and  analyze  existing \nsystems to demonstrate the use of the model for diagnosing \n\nCHI 2010: Performance, Stagecraft, and MagicApril 10–15, 2010, Atlanta, GA, USA557 \n \n \n\fand  assessing  problems.",
#         "We  conclude  with  a  discussion  of \ndesign  guidelines  for  personal  informatics  systems  and \ndirections for future research."
#     ]
# for i in range(10):
# print(f"Run time : ", generate_from_evidence(question + evaluation_instruction, evidence))