from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker

spell = SpellChecker()

input_text = "Thiss is a samplee text withh somee misspellinggs."
input_text2 = "Which constituancy is Shashi Tharoor compeeting from?"

words = word_tokenize(input_text2)
proper_nouns = ["Shashi", "Tharoor"]

corrected_text = []
for word in words:
    if word in proper_nouns:
        corrected_text.append(word)
    else:
        corrected_word = spell.correction(word)
        corrected_text.append(corrected_word)
corrected_text = " ".join(corrected_text)

print("Original text:", input_text2)
print("Corrected text:", corrected_text)
