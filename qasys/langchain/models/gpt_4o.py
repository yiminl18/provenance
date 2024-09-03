from openai import OpenAI
import openai
import os 
client = OpenAI()


# Access the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

# print(api_key)

def chatGPT_api(message_content,temperature=0, json_mode=False):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    

    if json_mode:
        response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message_content,
            }
        ],
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    else:
        response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message_content,
            }
        ],
        model="gpt-4o",
        temperature=temperature,
    )

    # Extract the generated content from the response
    output_content = response.choices[0].message.content

    # Get the number of tokens used for the input and output
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    # Define the price per token (you should adjust these based on actual costs)
    input_price_per_token = 5 / 10 ** 6  # Price per input token
    output_price_per_token = 15 / 10 ** 6  # Price per output token

    # Calculate the total cost
    cost = (input_tokens * input_price_per_token) + (output_tokens * output_price_per_token)

    # Return a dictionary with the generated content, token counts, and cost
    return {
        "content": output_content,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost": cost
    }

def gpt_4o(prompt, json_mode=False):
    gpt_4o.call_count += 1
    message_content = prompt[0] + prompt[1]
    return chatGPT_api(message_content, json_mode=json_mode)

