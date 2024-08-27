import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def find_with_fuzzy_match(text, query, match_type='exact', threshold=75):
    """
    Find a matching string in the text, supporting exact and fuzzy matching.
    
    Parameters:
    text (str): The text to search within.
    query (str): The query string to search for.
    match_type (str): The type of match, 'exact' for exact match, 'fuzzy' for fuzzy match.
    threshold (int): The similarity threshold for fuzzy matching, used only for fuzzy match.
    
    Returns:
    int: The index of the match if found, or -1 if not found.
    """
    if match_type == 'exact':
        # Perform exact match using regular expression
        match = re.search(re.escape(query), text)
        if match:
            return match.start()
        else:
            return -1
    
    elif match_type == 'fuzzy':
        # Perform fuzzy match using fuzzywuzzy
        matches = process.extract(query, [text], limit=1)
        best_match = matches[0]
        if best_match[1] >= threshold:
            return text.find(best_match[0])
        else:
            return -1
    else:
        raise ValueError("match_type must be 'exact' or 'fuzzy'.")

# Example usage
text = "Hello, this is a sample text."
query_exact = "sample"
query_fuzzy = "sampel"

# Exact match
result_exact = find_with_fuzzy_match(text, query_exact, match_type='exact')
print(result_exact)  # Output: 17 (expected)

# Fuzzy match
result_fuzzy = find_with_fuzzy_match(text, query_fuzzy, match_type='fuzzy')
print(result_fuzzy)  # Output: 17 (expected if threshold is met) or -1 if not