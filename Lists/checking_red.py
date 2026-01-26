from collections import Counter
import re

# Read your text file
with open('lorem_data.txt', 'r') as f:
    text = f.read().lower()  # convert to lowercase to treat 'Word' and 'word' as same

# Remove punctuation (optional)
text = re.sub(r'[^\w\s]', '', text)

# Split into words
words = text.split()

# Count word occurrences
word_counts = Counter(words)

# Find repeated words
repeated_words = {word: count for word, count in word_counts.items() if count > 1}

print("Repeated words and their counts:")
for word, count in repeated_words.items():
    print(f"{word}: {count}")
