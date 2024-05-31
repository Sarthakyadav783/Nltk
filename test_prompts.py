# libraries
from nltk.corpus import words
import pandas as pd
from nltk_spellchecking import nltk_correct_txt, nltk_spell_check, correction

from nltk_spellchecking import name_spellcheck
import handle_spellcheck
import add_noise


# if you do not want to add noise to input then change this to 0
ADD_NOISE = 1
# should probably pick something between 0.1 and 0.15
NOISE_STRENGTH = 0.13
JUST_ENGLISH = "just english"
JUST_NAME = "just name"
BOTH = "whole sentence"

def english_outputs(input: str):
    """
    Print the input prompt (only general English), and the output from various spellchecking modules 
    """
    print(f"\nInput text: {input}")
    print(
        f"Output from nltk_correct_txt.did_you_mean(): {nltk_correct_txt.did_you_mean(input)}")
    print(
        f"Output from nltk_correct_txt.fuzzy_did_you_mean(): {nltk_correct_txt.fuzzy_did_you_mean(input, word_list)}")
    print(
        f"Output from nltk_spell_check.spell_check(): {nltk_spell_check.spell_check(input)}")
    print(f"Output from handle_spellcheck.handle_spellcheck(): {handle_spellcheck.handle_spellcheck(input)}")


def name_outputs(input: str):
    """
    Print the input prompt (only names), and the output from various spellchecking modules 
    """
    print(f"\nInput text: {input}")
    print(f"Output from name_spellcheck.edit_dist_suggestion(): {name_spellcheck.edit_dist_suggestion(input)}")
    


def whole_sentence_outputs(input: str):
    """
    Print the input prompt, and the output from various spellchecking modules
    """
    print(f"\nInput text: {input}")
    print(
        f"Output from correction.correct_text(): {correction.correct_text(input, df)}")


def run_test(file_name: str, test_type: str, limit = -1):
    """
    file must be in same directory
    """
    i = 0
    with open(file_name, "r") as file:
        for prompt in file:
            if i == limit:
                break
            i += 1
            input = ""
            if ADD_NOISE:
                input += add_noise.noisy(prompt, NOISE_STRENGTH)
            else:
                input += prompt

            if test_type == JUST_ENGLISH:
                english_outputs(input)
            elif test_type == JUST_NAME:
                name_outputs(input)
            elif test_type == BOTH:
                whole_sentence_outputs(input)
            else:
                raise ValueError


if __name__ == "__main__":

    word_list = set(words.words())
    df = pd.read_excel('nltk_spellchecking/ELECTION_2024.xlsx')

    file_name = "no_name_eng_prompts.txt"
    run_test(file_name, JUST_ENGLISH, 10)