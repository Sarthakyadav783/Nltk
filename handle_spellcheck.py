import string
import re
from nltk_spellchecking import name_spellchecking

def punctuation_spacing(prompt: str) -> str:
    """
    Add space around punctuation
    """
    special_regex_chars = [".", "+", "*", "?", "^",
                           "$", "(", ")", "[", "]", "{", "}", "|", "\\"]
    already_seen = []
    ans = prompt
    for char in prompt:
        if char not in already_seen:
            already_seen.append(char)
            if char in special_regex_chars:
                ans = re.sub("\{}".format(char), " {} ".format(char), ans)
            elif char in string.punctuation:
                ans = re.sub(char, " {} ".format(char), ans)
    return ans


def give_suggestion(original: str, list_of_dicts: list) -> str:
    """
    Take in the list of dictionaries given by model
    spell check name, whole sentence
    return suggestion
    """
    # example = [{'span': 'John', 'label': 'PERSON', 'score': 0.9854856729507446, 'char_start_index': 6, 'char_end_index': 10},
    #            {'span': '15', 'label': 'DATE', 'score': 0.9371686577796936, 'char_start_index': 22, 'char_end_index': 24}]

    # # ================ SOLUTION 1 ========================
    # # extract name strings, call the spell check on them,
    # # then call the spell check on the whole string with the corrected names
    # #  - not sure if the names will interfere when checking rest of sentence?

    correct_name_prompt = original
    original_names = []

    for dict in list_of_dicts:
        span_name = dict['span']
        if dict['label'] == 'PERSON' and span_name not in original_names:
            original_names.append(span_name)

            # corrected_name = func(span_name)
            corrected_name = name_spellchecking.edit_dist_suggestion(span_name)
            correct_name_prompt = re.sub(" {old_name} ".format(
                old_name=span_name), " {new_name} ".format(new_name=corrected_name), correct_name_prompt)

    # # ================ SOLUTION 2 ========================
    # # extract name strings, call the spell check on them,
    # # call spell check on the remaining sentence
    # # with placeholder values for the name.

    # # If time, implement multithreading?

    # # spell check name
    # # spell check rest of sentence?

    suggestion = ""
    return suggestion
