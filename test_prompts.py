# libraries
from nltk.corpus import words
import random
import pandas as pd
from nltk_spellchecking import nltk_correct_txt, nltk_spell_check
import nltk_spellchecking.correction as correction
import add_noise


# if you do not want to add noise to input then change this to 0
ADD_NOISE = 1
# should probably pick something between 0.1 and 0.15
NOISE_STRENGTH = 0.13


def english_outputs(input: str):
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


def whole_sentence_outputs(input: str):
    """
    Print the input prompt, and the output from the various 
    corrector functions in this module
    """
    print(f"\nInput text: {input}")
    print(
        f"Output from correction.correct_text(): {correction.correct_text(input, df)}")


def run_test(file_name: str, test_type: str):
    """
    file must be in same directory
    """
    with open(file_name, "r") as file:
        for prompt in file:
            input = ""
            if ADD_NOISE:
                input += add_noise.noisy(prompt, NOISE_STRENGTH)
            else:
                input += prompt

            if test_type == "just english":
                english_outputs(input)
            elif test_type == "just name":
                # not implemented yet
                return
            elif test_type == "everything":
                whole_sentence_outputs(input)
            else:
                raise ValueError


if __name__ == "__main__":
    random.seed(100)
    word_list = set(words.words())
    df = pd.read_excel('nltk_spellchecking/ELECTION_2024.xlsx')

    file_name = "name_eng_prompts.txt"
    run_test(file_name, "everything")