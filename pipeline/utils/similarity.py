from nltk import word_tokenize
import numpy as np 
from openai import OpenAI
from typing import Literal

def clean_string(input_string):
    # Use the isalnum() method to keep only letters and Arabic numerals
    cleaned_string = ''.join(char for char in input_string if char.isalnum())
    return cleaned_string

def get_embedding(text:str, model="text-embedding-3-small"):
    client = OpenAI()
    return np.array(client.embeddings.create(input = [text], model=model).data[0].embedding)

def normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def centralize(vector: np.ndarray, mean_vector: np.ndarray) -> np.ndarray:
    return vector - mean_vector

def get_cosine_similarity(str1:str, str2:str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def get_cosine_distance(str1:str, str2:str):
    cosine_similarity = get_cosine_similarity(str1, str2)
    return 1 - cosine_similarity

def get_l2_distance(str1: str, str2: str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    distance = np.linalg.norm(vec1 - vec2) ** 2
    return distance

def get_inner_product_similarity(str1: str, str2: str):
    vec1 = get_embedding(str1)
    vec2 = get_embedding(str2)
    inner_product = np.dot(vec1, vec2)
    return inner_product

def get_jaccard_similarity(str1: str, str2:str, mode: Literal['union', 'intersection'] = 'union'):
    """
    Compute the Jaccard similarity between two strings by counting the number of common words.

    Parameters:
    str1 (str): The first string
    str2 (str): The second string
    mode (str): The mode of Jaccard similarity. 'union' for the normal Jaccard similarity, 'intersection' for the Jaccard similarity based on the intersection of the two sets.
    Returns:
    float: The Jaccard similarity
    """
    # Split the strings into words
    words1_list = word_tokenize(str1.lower())
    words2_list = word_tokenize(str2.lower())
    words1_list = [clean_string(w) for w in words1_list]
    words2_list = [clean_string(w) for w in words2_list]
    words1 = set(words1_list)
    words2 = set(words2_list)
    words1.discard('')
    words2.discard('')
    
    # Compute the intersection and union of the two sets
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if mode == 'union':
        if len(union) == 0:
            return 0.0  # Prevent division by zero
        jaccard_sim = len(intersection) / len(union)
    elif mode == 'intersection':
        if len(words1) == 0 or len(words2) == 0:
            return 0.0
        jaccard_sim = len(intersection) / min(len(words1), len(words2))
    return jaccard_sim