from nltk.corpus import words
import random, string
import nltk_correct_txt, nltk_spell_check, rapidfuzz_correct_txt


# if you do not want to add noise to input then change this to 0
ADD_NOISE = 1


def perform_operation(character: str) -> str:
    """ randomly choose between add, replace, or delete for the given character,
    return resulting substring"""

    insert = "insert"
    replace = "replace"
    delete = "delete"
    choice = random.choice([insert, replace, delete])
    
    if choice == "delete":
        return ""
    else:
        new_char = random.choice(string.ascii_letters)
        if choice == "replace":
            return new_char
        # choice is insert
        return new_char + character


def noisy(prompt: str, strength: float) -> str:
    # strength must be between 0 and 1 inclusive,
    # where strength of 0 will result in the same prompt being returned
    # and strength of 1 will perform a change on each character
    noisy_prompt = ''

    for char in prompt:
        if random.random() <= strength:
            # perform change
            noisy_prompt += perform_operation(char)
        else:
            noisy_prompt += char
    return noisy_prompt


def test_general_english(input: str):
    print(f"Input text: {input}")
    print(f"Output from nltk_correct_txt.did_you_mean(): {nltk_correct_txt.did_you_mean(input)}")
    print(f"Output from nltk_correct_txt.fuzzy_did_you_mean(): {nltk_correct_txt.fuzzy_did_you_mean(input, word_list)}")
    print(f"Output from nltk_spell_check.spell_check(): {nltk_spell_check.spell_check(input)}")
    print(f"Output from rapidfuzz_correct_txt.did_you_mean(): {rapidfuzz_correct_txt.did_you_mean(input)}")
    print(f"Output from rapidfuzz_correct_txt.fuzzy_did_you_mean(): {rapidfuzz_correct_txt.fuzzy_did_you_mean(input, word_list)}")
    print("\n\n")


if __name__ == "__main__":
    # ignore this line; dont change
    random.seed(100)
    word_list = set(words.words())
    with open("general_english_prompts.txt", "r") as file:
        for prompt in file:
            if ADD_NOISE:
                input = noisy(prompt, 0.2)
            else:
                input = prompt
            test_general_english(input)