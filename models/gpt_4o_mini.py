from openai import OpenAI
import openai
import os 
client = OpenAI()


# Access the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

#print(api_key)

def chatGPT_api(message_content,temperature=0):
    ##message_content is string
    response = client.chat.completions.create(model = "gpt-4o-mini",
        messages = [
            {"role": "user", "content": message_content}],
        temperature = temperature)

    return response.choices[0].message.content
    #return response["choices"][0]["message"]["content"]

def gpt_4o_mini(prompt):
    return chatGPT_api(prompt)
