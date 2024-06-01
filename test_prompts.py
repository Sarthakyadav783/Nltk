# libraries
from nltk.corpus import words
import pandas as pd
import name_spellcheck
import nltk_correct_txt
import handler
import add_noise


# if you do not want to add noise to input then change this to 0
ADD_NOISE = 1
# should probably pick something between 0.1 and 0.15
NOISE_STRENGTH = 0.13
ENGLISH = "english"
JUST_NAME = "just name"


def english_outputs(input: str):
    """
    Print the input prompt, and the output from various spellchecking modules 
    """
    print(f"\nInput text: {input}")
    print(
        f"Output from nltk_correct_txt.did_you_mean(): {nltk_correct_txt.did_you_mean(input)}")
    print(
        f"Output from handle_spellcheck.handle_spellcheck(): {handler.handle_spellcheck(input)}")


def name_outputs(input: str):
    """
    Print the input prompt (only names), and the output from various spellchecking modules 
    """
    print(f"\nInput text: {input}")
    print(
        f"Output from name_spellcheck.edit_dist_suggestion(): {name_spellcheck.edit_dist_suggestion(input)}")


def run_test(file_name: str, test_type: str, limit=-1):
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
                input += add_noise.noisy(prompt,
                                         NOISE_STRENGTH, transposition=True)
            else:
                input += prompt

            if test_type == ENGLISH:
                english_outputs(input)
            elif test_type == JUST_NAME:
                name_outputs(input)
            else:
                raise ValueError


if __name__ == "__main__":

    word_list = set(words.words())
    df = pd.read_excel('other_py_files/ELECTION_2024.xlsx')

    file_name = "name_eng_prompts.txt"
    run_test(file_name, ENGLISH)
