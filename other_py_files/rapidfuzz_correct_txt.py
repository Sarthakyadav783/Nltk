import nltk
from nltk.corpus import words
from autocorrect import Speller
from rapidfuzz import process, fuzz

# Download NLTK word corpus
nltk.download('words')

# Load the word list from NLTK
word_list = set(words.words())

# Initialize the spell checker
spell = Speller()
def did_you_mean(input_text):
    # Tokenize and normalize the input text
    tokens = nltk.word_tokenize(input_text.lower())
    
    suggestions = []
    for token in tokens:
        if token not in word_list:
            # Use spell checker to correct misspelled words
            correction = spell(token)
            suggestions.append(correction)
        else:
            suggestions.append(token)
    
    corrected_text = ' '.join(suggestions)
    
    return corrected_text

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

# Example usage
input_text = "I lovve progrmming in Pythn"
corrected_text_spell = did_you_mean(input_text)
corrected_text_fuzzy = fuzzy_did_you_mean(corrected_text_spell, word_list)
print(f"Did you mean: {corrected_text_fuzzy}?")
