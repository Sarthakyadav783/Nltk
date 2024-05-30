# libraries
from nltk.corpus import words
import random
from nltk_spellchecking import nltk_correct_txt, nltk_spell_check
import add_noise


# if you do not want to add noise to input then change this to 0
ADD_NOISE = 1
# should probably pick something between 0.1 and 0.15
NOISE_STRENGTH = 0.13


def test_general_english(input: str):
    """
    Print the input prompt, and the output from the various 
    corrector functions in this module
    """
    print(f"\nInput text: {input}")
    print(
        f"Output from nltk_correct_txt.did_you_mean(): {nltk_correct_txt.did_you_mean(input)}")
    print(
        f"Output from nltk_correct_txt.fuzzy_did_you_mean(): {nltk_correct_txt.fuzzy_did_you_mean(input, word_list)}")
    print(
        f"Output from nltk_spell_check.spell_check(): {nltk_spell_check.spell_check(input)}")


if __name__ == "__main__":
    # dont change this line!
    random.seed(100)

    word_list = set(words.words())
    with open("general_english_prompts.txt", "r") as file:
        for prompt in file:
            input = ""
            if ADD_NOISE:
                input += add_noise.noisy(prompt, NOISE_STRENGTH)
            else:
                input += prompt
            test_general_english(input)
