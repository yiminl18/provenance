def retrieve_and_generation(question, vectorstore, folder_path = "data/civic/extracted_data", k = 6):
    '''
    Input : question, str
            folder_path, str
            chunk_size, int
            chunk_overlap, int
            add_start_index, bool
    Output: final_answer, str
            retrieved_docs
    '''
    
    # Load and split documents
    

    # Retrieve
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

    # see how retrieve works 
    retrieved_docs = retriever.invoke(question)

    # Get chunk indices of retrieved documents
    retrieved_chunk_indices = [doc.metadata.get('chunk_index', -1) for doc in retrieved_docs]

    # generate
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


    from langchain import hub
    prompt = hub.pull("rlm/rag-prompt")

    # example_messages = prompt.invoke(
    #     {"context": "filler context", "question": "filler question"}
    # ).to_messages()


    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Intercept the prompt before it is sent to the LLM
    formatted_docs = format_docs(retrieved_docs)
    question_for_evaluation = question+' Only return the answer required by the question. There is no need to include extra information such as reasons. Separate the answers with commas if there are multiple items. Return None if no answer is found.'
    prompt_content = prompt.invoke({"context": "skip for short", "question": question_for_evaluation}).to_messages()[0]
    

    return rag_chain.invoke(question_for_evaluation), retrieved_docs, retrieved_chunk_indices, prompt_content

def generate_from_evidence(question, evidence):
    '''
    Input: question, str
            evidence, list of str
    Output: final_answer, str
    '''
    from model import model
    system = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise."""
    question_for_evaluation = question+' Only return the answer required by the question. There is no need to include extra information such as reasons. Separate the answers with commas if there are multiple items. Return None if no answer is found.'
    evidence_str = '\n\n'.join(evidence)
    text = f"""Question: {question_for_evaluation}\n\nContext: {evidence_str}\n\nAnswer: """
    prompt = (system, text)
    final_answer = model('gpt35', prompt)
    return final_answer
# print(retrieve_and_generation(question))