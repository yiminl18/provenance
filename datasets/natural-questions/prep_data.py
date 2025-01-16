import base64, gzip, json, os, re, sys
from collections import Counter
from json.decoder import JSONDecodeError
from pathlib import Path


# can be repeated on training dataset
dataset = "dev"
DATA_DIR = os.path.join(os.path.expanduser("~"), "data", "v1.0", f"{dataset}")

pattern = f"simplified-nq-{dataset}-??.jsonl.gz"
files = sorted(Path(DATA_DIR).glob(pattern))



def get_question(data_dir, dataset = "dev", start_file = 0, end_file = None):

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
