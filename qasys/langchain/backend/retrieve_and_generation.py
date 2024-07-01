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
    prompt_content = prompt.invoke({"context": "skip for short", "question": question}).to_messages()[0]
    

    return rag_chain.invoke(question), retrieved_docs, retrieved_chunk_indices, prompt_content


# print(retrieve_and_generation(question))