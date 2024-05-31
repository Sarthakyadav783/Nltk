import pandas as pd
from spellchecker import SpellChecker
from fuzzywuzzy import process
# import nltk
from nltk import word_tokenize

# nltk.download('punkt')


df = pd.read_excel("nltk_spellchecking/ELECTION_2024.xlsx")

spell = SpellChecker()

# Function to correct candidate names using fuzzy matching
def correct_candidate_name(word, df, column_name='CANDINAME'):
    best_match = process.extractOne(word, df[column_name])
    if best_match and best_match[1] >= 90:  # threshold
        return best_match[0]
    else:
        return word  


def correct_text(text, df, column_name='CANDINAME'):
    corrected_text = []
    words = word_tokenize(text)
    for word in words:
        # First, try to correct the candidate name
        corrected_word = correct_candidate_name(word, df, column_name)
        # If the word was not changed by name correction, correct its spelling
        if corrected_word == word:
            corrected_word = spell.correction(word)
        # Append the word if the corrected word is None
        if corrected_word is not None:
            corrected_text.append(corrected_word)
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)


# text1="Which constituancy is Lokenath Gowd Suragoni from? "
# text2 = "Which constituancy is Shashi Tharore compeeting from?"

# corrected_text1=correct_text(text1,df)
# corrected_text2 = correct_text(text2, df)

# print("Original text 1:", text1)
# print("Corrected text 1:", corrected_text1)

# print("Original text 2:", text2)
# print("Corrected text 2:", corrected_text2)
