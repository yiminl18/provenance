from openai import OpenAI
import openai
import os
import time

# Access the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

def chatGPT_api(message_content, temperature=0, max_retries=3):
    # Initialize the client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    for attempt in range(max_retries):
        try:
            # Call the OpenAI API to generate a response
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": message_content,
                    }
                ],
                model="gpt-4-turbo",
                temperature=temperature,
            )

            # Extract the generated content from the response
            output_content = response.choices[0].message.content

            # Get the number of tokens used for the input and output
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Define the price per token (you should adjust these based on actual costs)
            input_price_per_token = 10 / 10**6  # Price per input token
            output_price_per_token = 30 / 10**6  # Price per output token

            # Calculate the total cost
            cost = (input_tokens * input_price_per_token) + (output_tokens * output_price_per_token)

            # Return a dictionary with the generated content, token counts, and cost
            return {
                "content": output_content,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost
            }

        except openai.error.OpenAIError as e:  # This is the correct way to catch exceptions
            if isinstance(e, openai.error.InternalServerError):
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff before retrying
                    continue  # Retry the request
                else:
                    print(f"Failed after {max_retries} attempts: {str(e)}")
                    raise  # Reraise the exception after max retries
            else:
                print(f"Error: {str(e)}")
                raise  # Reraise other exceptions

def gpt_4_turbo(prompt):
    gpt_4_turbo.call_count += 1
    message_content = prompt[0] + prompt[1]
    return chatGPT_api(message_content)