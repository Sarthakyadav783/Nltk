import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
# nltk.download('wordnet')

def spell_check(text):
    # Tokenize the input text
    tokens = word_tokenize(text)

    # Initialize a list to store corrected tokens
    corrected_text = []

    for token in tokens:
        # Check if the word is in the WordNet corpus (a basic dictionary)
        if not wordnet.synsets(token):
            # If not, consider it misspelled and attempt to correct it
            corrected_word = correct_spelling(token)
            corrected_text.append(corrected_word)
        else:
            corrected_text.append(token)

    # Join the corrected tokens back into a single string
    corrected_text = ' '.join(corrected_text)
    return corrected_text

def correct_spelling(word):
    # Basic edit distance based spelling correction
    suggestions = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            suggestions.append(lemma.name())

    # Return the most likely suggestion
    if suggestions:
        return max(set(suggestions), key=suggestions.count)
    else:
        return word


if __name__ == "__main__":
    # this way, this block of code is only executed when you explicity decide to run this file, and is not run
    # when another file tries to access this one

    # Example usage
    input_text = "Ths is an exmple of misspeled text."
    corrected_text = spell_check(input_text)
    print("Original Text:", input_text)
    print("Corrected Text:", corrected_text)