def retrieve_and_generation(question, vectorstore, folder_path = "data/civic/extracted_data"):
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
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

    # see how retrieve works 
    retrieved_docs = retriever.invoke(question)
    # print(len(retrieved_docs))
    # print(retrieved_docs[0].page_content)
    # with open("output.txt", "w", encoding="utf-8") as file:
    #     for doc in retrieved_docs:
    #         file.write("retrieved_chunk_data: ")
    #         file.write (str(doc.metadata) + "\n")
    #         file.write(doc.page_content + "\n----------retrieved_chunk_end--------\n")

    # generate

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


    from langchain import hub

    prompt = hub.pull("rlm/rag-prompt")


    example_messages = prompt.invoke(
        {"context": "filler context", "question": "filler question"}
    ).to_messages()


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

    # stream output
    # for chunk in rag_chain.stream(question):
    #     print(chunk, end="", flush=True)

    return rag_chain.invoke(question), retrieved_docs


# print(retrieve_and_generation(question))