import base64, gzip, json, os, re, sys
from collections import Counter
from json.decoder import JSONDecodeError
from pathlib import Path


def load_hp_data(data_dir: str, dataset = "fullwiki"):
    """
    Load HotpotQA dataset
    
    Args:
        data_dir: Base directory containing the dataset
    """
    return json.load(open(f"{data_dir}/hotpot_dev_{dataset}_v1.json", 'r'))


def load_ca_data(dataset):

    DATA_DIR = os.path.join(os.path.expanduser("~"), "data", "chroniclingamericaQA")
    
    parsed_objects = []
    file_path = f"{DATA_DIR}/{dataset}.json"
    # Determine file opening method based on extension
    open_method = gzip.open if file_path.endswith('.gz') else open
    mode = 'rt' if file_path.endswith('.gz') else 'r'
    with open_method(file_path, mode, encoding='utf-8') as file:
        # Read the entire file content
        content = file.read()
    # Split the content into lines or use a streaming approach
    lines = content.splitlines()
    for line in lines:
        try:
            # Try to parse each line as a separate JSON object
            parsed_object = json.loads(line.strip())
            parsed_objects.append(parsed_object)
        except JSONDecodeError:
            # If line parsing fails, try parsing entire content as a single JSON
            if not parsed_objects:
                try:
                    parsed_objects = json.loads(content)
                    break
                except JSONDecodeError:
                    continue
    # If no objects parsed, return an empty list
    return parsed_objects if parsed_objects else []

def load_nq_data(dataset = "dev"):
    """
    Load Natural Questions dataset
    
    Args:
        data_dir: Base directory containing the dataset
    """


    DATA_DIR = os.path.join(os.path.expanduser("~"), "data", "v1.0", f"{dataset}")

    pattern = f"combined-nq-{dataset}-??.jsonl.gz"
    files = sorted(Path(DATA_DIR).glob(pattern))

    def get_question(data_dir,  start_file = 0, end_file = None):

        # Extract file number using string operations
        def get_file_num(filepath):
            # Get the two digits before .jsonl.gz
            return int(filepath.name.split('.')[0][-2:])

        # Filter files based on start/end numbers if specified
        if end_file is not None:
            files = [f for f in files if get_file_num(f) <= end_file]
        files = [f for f in files if get_file_num(f) >= start_file]

        for file in files:
            print(f"Reading {file.name}")
            with gzip.open(file, 'rt', encoding='utf-8') as f:
                for line in f:
                    yield json.loads(line.strip())

    return get_question(DATA_DIR)



def load_qa_dataset(dataset_name: str, dataset_type: str):
    """
    Load QA dataset based on name
    
    Args:
        dataset_name: One of 'hotpotqa', 'chroniclingamericaqa', or 'natural-questions'
        data_dir: Base directory containing the datasets
    """
    dataset_loaders = {
        'hotpot': lambda: load_hp_data(dataset_type),
        'chroniclingamerica': lambda: load_ca_data(dataset_type),
        'naturalquestions': lambda: load_nq_data(dataset_type)
    }
    
    dataset_name = dataset_name.lower()  # normalize input
    if dataset_name not in dataset_loaders:
        raise ValueError(f"Unknown dataset: {dataset_name}. Available datasets: {list(dataset_loaders.keys())}")
    
    return dataset_loaders[dataset_name]()

def standardize_keys(example, dataset_type):
    """
    Standardize the keys of a QA dataset example.
    
    Args:
        example (dict): A QA dataset example
        dataset_type (str): Type of the dataset (e.g., 'squad', 'nq', 'triviaqa')
    
    Returns:
        dict: Standardized example with keys 'title', 'context', 'question', 'answers'
    """
    if dataset_type == 'chroniclingamerica':
        return {
            'x_id': example['query_id'],
            'question': example['question'],
            'answer': example['answer'],
            'context': example['context']
        }
    elif dataset_type == 'hotpot':
        return {
            'title': example['title'],
            'context': example['context'],
            'question': example['question'],
            'answers': example['answer']
        }
    elif dataset_type == 'naturalquestions':
        return {
            'title': example['title'],
            'context': example['context'],
            'question': example['question'],
            'answers': example['answer']
        }
    else:
        raise ValueError(f"Unsupported dataset type: {dataset_type}")

def process_dataset(dataset_name: str, dataset_type: str):
    """
    Load and standardize a dataset
    """
    
    try:
        data = load_qa_dataset(dataset_name, dataset_type)
        
        if data is None:
            print("Warning: load_qa_dataset returned None")
            return []
            
        if isinstance(data, list):
            if len(data) > 0:
                print(f"First item keys: {data[0].keys()}")
            standardized = [standardize_keys(example, dataset_name) for example in data]
            print(f"Standardized {len(standardized)} examples")
            return standardized
        else:
            return [standardize_keys(example, dataset_name) for example in data]
            
    except Exception as e:
        print(f"Error in process_dataset: {e}")
        raise