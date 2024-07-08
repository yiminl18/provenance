from openai import OpenAI
import openai
import os 
client = OpenAI()


# Access the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key


def chatGPT_api(message_content, temperature=0, json_mode=False):
    ##message_content is string
    
    
    if json_mode:
        response = client.chat.completions.create(model = "gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages = [
                {"role": "user", "content": message_content}],
            temperature = temperature)
    else:
        response = client.chat.completions.create(model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": message_content}],
        temperature = temperature)

    return response.choices[0].message.content
    #return response["choices"][0]["message"]["content"]

def gpt_35(prompt, json_mode=False):
    message_content = prompt[0] + prompt[1]
    return chatGPT_api(message_content, json_mode = json_mode)

