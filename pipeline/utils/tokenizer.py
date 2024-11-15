from typing import List, Set
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

def remove_elements_by_indexes(input_list:list, input_index:list):
    my_list = input_list.copy()
    indexes_to_remove = input_index.copy()
    if indexes_to_remove == []:
        return my_list
    # 将索引列表排序并反转
    indexes_to_remove.sort(reverse=True)
    
    # 删除相应索引位置的元素
    for index in indexes_to_remove:
        del my_list[index]
    
    return my_list

def remove_elements_by_intervals(sentences: List[str], remove_intervals: List[List[int]]) -> List[str]:
    """Remove elements from sentences based on intervals"""
    remove_set = convert_intervals_to_set(remove_intervals)
    remove_indexes = list(remove_set)
    return remove_elements_by_indexes(sentences, remove_indexes)

def convert_intervals_to_set(intervals: List[List[int]]) -> Set[int]:
    """Convert list of intervals to set of indices"""
    result_set = set()
    for interval in intervals:
        start, end = interval
        result_set.update(range(start, end + 1))
    return result_set

def remove_intervals(full_intervals: List[List[int]], remove_intervals: List[List[int]]) -> List[List[int]]:
    """Remove intervals from full intervals"""
    full_set = convert_intervals_to_set(full_intervals)
    remove_set = convert_intervals_to_set(remove_intervals)
    result_set = full_set - remove_set
    return convert_set_to_intervals_without_merging(result_set, full_intervals)

def partition_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Partition intervals into smaller intervals"""
    result = []
    for interval in intervals:
        start, end = interval
        if start < end:
            mid = (start + end) // 2
            result.append([start, mid])
            result.append([mid + 1, end])
        else:
            result.append(interval)
    return result

def interval_all_len_1(interval_list: List[List[int]]) -> bool:
    """Check if all intervals have length 1"""
    for interval in interval_list:
        if interval[0] == interval[1]:
            continue
        else:
            return False
    return True

def convert_set_to_intervals_without_merging(result_set: Set[int], 
                                            original_intervals: List[List[int]]) -> List[List[int]]:
    """Convert set back to intervals using original intervals as reference"""
    if not result_set:
        return []
        
    intervals = []
    for original_interval in original_intervals:
        start, end = original_interval
        current_interval = []
        
        for i in range(start, end + 1):
            if i in result_set:
                current_interval.append(i)
            else:
                if current_interval:
                    intervals.append([current_interval[0], current_interval[-1]])
                    current_interval = []
                    
        if current_interval:
            intervals.append([current_interval[0], current_interval[-1]])
            
    return intervals