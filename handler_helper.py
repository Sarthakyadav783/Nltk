import string
import re
from nltk.metrics import edit_distance
from name_spellcheck import edit_dist_suggestion


def final_check(prompt: str, suggestion: str) -> str:
    """
    the spell checking model seems to add a few unnecessary tokens
    at the end that are completely false. add a check for this
    and return the real answer.

    currently kinda slow; should think about faster solution?
    """
    prompt_tokens = prompt.split(" ")
    last_word = ""
    for i in range(len(prompt_tokens) - 1, -1, -1):
        prompt_token = prompt_tokens[i]
        if prompt_token not in string.punctuation and prompt_token not in string.whitespace:
            last_word += prompt_token
            break

    suggestion_tokens = suggestion.split(" ")
    n = len(suggestion_tokens)

    # loop from the end and go backwards
    # keep in mind that the spellcheck suggestion adds proper punctuation
    for i in range(n-1, -1, -1):
        # go backwards; see if token in prompt (some similarity threshold)
        # once you find the first token that meets the threshold
        # and is not punctuation, break the loop
        token = suggestion_tokens[i]
        if token not in string.punctuation and edit_distance(token, last_word) < 4:
            return " ".join(suggestion_tokens[: i+1])
    return ""


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


def correct_name(original: str, list_of_dicts: list, include_transpositions=False) -> str:
    """
    Take in the list of dictionaries given by model
    spell check name, whole sentence
    return suggestion
    """

    correct_prompt = original
    original_names = []

    for dict in list_of_dicts:
        span_name = dict['span']
        if dict['label'] == 'PERSON' and span_name not in original_names:
            original_names.append(span_name)

            # corrected_name = func(span_name)
            corrected_name = edit_dist_suggestion(
                span_name, include_transpositions)
            correct_prompt = re.sub(" {old_name} ".format(
                old_name=span_name), " {new_name} ".format(new_name=corrected_name), correct_prompt)
    return correct_prompt
