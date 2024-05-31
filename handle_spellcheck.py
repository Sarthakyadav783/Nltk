from transformers import pipeline
from span_marker import SpanMarkerModel
import warnings
import string
import re
from nltk import edit_distance
from nltk_spellchecking import name_spellcheck


def load_models() -> list:
    """ load the model that checks for names
    and the english spelling pipeline
    """
    ner_model = SpanMarkerModel.from_pretrained(
        "tomaarsen/span-marker-roberta-large-ontonotes5")
    ner_model.cuda()
    eng_spell_pipeline = pipeline(
        "text2text-generation", model="oliverguhr/spelling-correction-english-base")
    return ner_model, eng_spell_pipeline


def final_check(prompt: str, suggestion: str) -> str:
    """
    the spell checking model seems to add a few unnecessary tokens
    at the end that are completely false. add a check for this
    and return the real answer.
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
            corrected_name = name_spellcheck.edit_dist_suggestion(
                span_name, include_transpositions)
            correct_prompt = re.sub(" {old_name} ".format(
                old_name=span_name), " {new_name} ".format(new_name=corrected_name), correct_prompt)
    return correct_prompt


# ================ MAIN FUNCTION ========================
def handle_spellcheck(input: str, transpositions=False):
    """
    separate punctuation from letters, 
    load ner model and run inference, load pipeline
    get corrected name prompt,
    run spellcheck on full sentence
    return suggestion
    """
    warnings.simplefilter(action='ignore', category=FutureWarning)
    ner_model, spelling_pipeline = load_models()
    prompt = punctuation_spacing(input)
    # # ================ SOLUTION 1 ========================
    # # extract name strings, call the spell check on them,
    # # then call the spell check on the whole string with the corrected names
    # #  - not sure if the names will interfere when checking rest of sentence?
    correct_name_prompt = correct_name(
        prompt, ner_model.predict(prompt), transpositions)
    pipeline_output = spelling_pipeline(correct_name_prompt, max_length=2048)
    suggestion = final_check(prompt, pipeline_output[0]['generated_text'])
    return suggestion

    # # ================ SOLUTION 2 ========================
    # # extract name strings, call the spell check on them,
    # # call spell check on the remaining sentence
    # # with placeholder values for the name.
    # # If time, implement multithreading? might not be worth the hassle though
