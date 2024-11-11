def nltk_sent_tokenize(text:str, minimum_token_num=10):
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text) # is a list[str]
    new_sentences = [sentences[0]]
    for sentence_index, sentence in enumerate(sentences[1:]):
        if get_token_num(new_sentences[-1])<minimum_token_num:
            new_sentences[-1] = new_sentences[-1] + ' ' + sentence

        else:
            if sentence_index == len(sentences)-2: # start from one
                if get_token_num(sentence) >= minimum_token_num:
                    new_sentences.append(sentence)
                else:
                    new_sentences[-1] = new_sentences[-1] + ' ' + sentence
            else:
                new_sentences.append(sentence)
    return new_sentences

def nltk_sent_tokenize_for_list(text_list: list, minimum_token_num=10):
    sentences = []
    for text in text_list:
        sentences += nltk_sent_tokenize(text, minimum_token_num=minimum_token_num)
    return sentences

# regular expression method
# def get_token_num_for_list(text_list: list):
#     token_num = 0
#     for text in text_list:
#         token_num += get_token_num(text)
#     return token_num

# def get_token_num(text:str):
#     import re
#     words = re.findall(r'\b\w+\b', text)
#     return len(words)

# openai tiktoken method
def get_token_num(text:str, model_name="gpt-4o-mini"):
    import tiktoken
    tokenizer = tiktoken.encoding_for_model(model_name)
    tokens = tokenizer.encode(text)
    return len(tokens)

def get_token_num_for_list(text_list: list, model_name="gpt-4o-mini"):
    token_num = 0
    for text in text_list:
        token_num += get_token_num(text, model_name=model_name)
    return token_num

def tiktoken_tokenize(text:str, model_name="gpt-4o-mini"):
    import tiktoken
    tokenizer = tiktoken.encoding_for_model(model_name)
    tokens = tokenizer.encode(text)
    tokens = [tokenizer.decode([token]) for token in tokens]
    return tokens