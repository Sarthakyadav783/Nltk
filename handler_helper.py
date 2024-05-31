import string
import re
from nltk.metrics import edit_distance


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


def chooser(prompt: str, suggestion1: str, suggestion2: str) -> str:
    """ Choose the best suggestion and return!"""
    return
