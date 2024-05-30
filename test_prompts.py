from nltk.corpus import words
import random
import string
import nltk_correct_txt
import nltk_spell_check
import rapidfuzz_correct_txt


# if you do not want to add noise to input then change this to 0
ADD_NOISE = 1
# should probably pick something between 0.1 and 0.15
NOISE_STRENGTH = 0.13


def perform_operation(character: str) -> str:
    """ randomly choose between add, replace, or delete for the given character,
    return resulting substring
    """

    insert = "insert"
    replace = "replace"
    delete = "delete"
    choice = random.choice([insert, replace, delete])

    if choice == delete:
        return ""
    else:
        new_char = random.choice(string.ascii_letters)
        if choice == replace:
            return new_char
        # choice is insert
        return new_char + character


def noisy(prompt: str, strength: float) -> str:
    """
    Given input string, add noise and return.
    Strength must be between 0 and 1, where 
    strength == 0 --> same prompt being returned
    strength == 1 --> will perform a change on every character
    """

    noisy_prompt = ''

    for char in prompt:
        if char == " " or random.random() > strength:
            noisy_prompt += char
        else:
            # perform change
            noisy_prompt += perform_operation(char)
    return noisy_prompt


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
    print(
        f"Output from rapidfuzz_correct_txt.did_you_mean(): {rapidfuzz_correct_txt.did_you_mean(input)}")
    print(
        f"Output from rapidfuzz_correct_txt.fuzzy_did_you_mean(): {rapidfuzz_correct_txt.fuzzy_did_you_mean(input, word_list)}")
    print("\n")


if __name__ == "__main__":
    # dont change this line!
    random.seed(100)

    word_list = set(words.words())
    with open("general_english_prompts.txt", "r") as file:
        for prompt in file:
            input = ""
            if ADD_NOISE:
                input += noisy(prompt, NOISE_STRENGTH)
            else:
                input += prompt
            test_general_english(input)
