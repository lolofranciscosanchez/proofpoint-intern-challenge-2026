import sys
import string
import re
from collections import Counter

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract words ignoring punctuation using regex
        # This regex matches blocks of alphabetical characters and numbers
        words = re.findall(r'\b[a-zA-Z0-9]+\b', text)
        
        # Make the comparison strictly case-insensitive
        words = [word.lower() for word in words]
        
        # Count frequencies
        word_counts = Counter(words)
        
        # Get the 10 most frequent words
        most_common = word_counts.most_common(10)
        
        print(f"Top 10 most frequent words in '{file_path}':")
        print("-" * 40)
        for i, (word, count) in enumerate(most_common, 1):
            print(f"{i}. '{word}': {count} times")
            
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error occurred while processing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python word_frequency.py <file_path>")
    else:
        process_file(sys.argv[1])
