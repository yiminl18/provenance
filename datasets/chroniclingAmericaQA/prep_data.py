# chroniclingamericaQA
import gzip
import json
from json.decoder import JSONDecodeError


def get_question():
    def read_json(file_path):
        """
        Robustly read and parse a JSON or gzipped JSON file with multiple JSON objects.

        Args:
            file_path (str): Path to the JSON or gzipped JSON file

        Returns:
            list: List of parsed JSON objects
        """
        parsed_objects = []

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
    return read_json('dev.json')
