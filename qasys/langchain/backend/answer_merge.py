from langchain_core.prompts import ChatPromptTemplate

def merge_answers(question, sub_query_list, sub_answer):
    '''
    Input: question, str
           sub_query_list, list of str
           sub_answer, list of str
    Output: final_answer, str
    '''

    # Create the LLMChain with the OpenAI language model
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    # Define the system prompt for merging answers
    system_prompt = """You are an expert at merging sub-answers into a final answer. \
                Perform query merging, given a initial question, \
                a list of its sub-queries and sub-answers, merge them into a final answer. \
                These sub-answers are generated correspondingly from the sub-questions that \
                have been well decomposed. \
                Hence you need to find an intersection between the sub-answers to generate the final answer \
                for the initial question. \
                If there are acronyms or words you are not familiar with, do not try to rephrase them.\
                Your final answer should be a well-structured and coherent response to the initial question."""
    
    prompt = ChatPromptTemplate.from_messages(
		[
			("system", system_prompt),
			("human", "{inputs}"),
		]
	)
    
    # Format the inputs
    inputs = {
        'question': question,
        'sub_query_list': sub_query_list,
        'sub_answer': sub_answer
    }
    
    chain = prompt | llm

    # Print the prompt
    formatted_prompt = prompt.format(inputs=inputs)
    
    # Generate the final answer using LangChain
    final_answer = chain.invoke(
		{
			"system": system_prompt,
			"inputs": inputs
		}
	).content
    
    return final_answer, formatted_prompt

# # Example usage
# question = "What are the health benefits of regular exercise?"
# sub_query_list = ["What are the cardiovascular benefits of regular exercise?", "What are the mental health benefits of regular exercise?", "What are the musculoskeletal benefits of regular exercise?"]
# sub_answer = ["Regular exercise improves cardiovascular health by strengthening the heart and increasing blood circulation.", "Regular exercise can reduce symptoms of anxiety and depression, and improve mood.", "Regular exercise strengthens muscles and bones, improving overall musculoskeletal health."]

# final_answer = merge_answers_with_langchain(question, sub_query_list, sub_answer)
# print(final_answer)
