import nltk

# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('words')

from nltk.corpus import words
from autocorrect import Speller
from rapidfuzz import process, fuzz

# Ensure necessary NLTK datasets are downloaded
nltk.download('punkt')
nltk.download('words')

# Load the word list from NLTK
word_list = set(words.words())

# Initialize the spell checker
spell = Speller()

# Function using autocorrect
def did_you_mean(input_text):
    # Tokenize and normalize the input text
    tokens = nltk.word_tokenize(input_text.lower())
    
    suggestions = []
    for token in tokens:
        if token not in word_list:
            # Suggest a correction if the word is not in the word list
            correction = spell(token)
            suggestions.append(correction)
        else:
            suggestions.append(token)
    
    # Join the suggestions into a single corrected sentence
    corrected_text = ' '.join(suggestions)
    
    return corrected_text

# Function using fuzzy matching
def fuzzy_did_you_mean(input_text, word_list):
    tokens = nltk.word_tokenize(input_text.lower())
    
    suggestions = []
    for token in tokens:
        if token not in word_list:
            # Get the best match from the word list using fuzzy matching
            best_match = process.extractOne(token, word_list, scorer=fuzz.ratio)
            suggestions.append(best_match[0])
        else:
            suggestions.append(token)
    
    corrected_text = ' '.join(suggestions)
    
    return corrected_text

# Example usagec
input_text = "I lovve progrmming in Pythn"

# Using autocorrect method
corrected_text_autocorrect = did_you_mean(input_text)
print(f"Autocorrect - Did you mean: {corrected_text_autocorrect}?")

# Using fuzzy matching method
corrected_text_fuzzy = fuzzy_did_you_mean(input_text, word_list)
print(f"Fuzzy Matching - Did you mean: {corrected_text_fuzzy}?")
