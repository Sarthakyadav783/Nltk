from transformers import pipeline
from span_marker import SpanMarkerModel
import string
import re
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
            print(span_name)
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
    prompt = punctuation_spacing(input)
    ner_model, spelling_pipeline = load_models()

    # # ================ SOLUTION 1 ========================
    # # extract name strings, call the spell check on them,
    # # then call the spell check on the whole string with the corrected names
    # #  - not sure if the names will interfere when checking rest of sentence?
    correct_name_prompt = correct_name(
        prompt, ner_model.predict(prompt), transpositions)
    suggestion = spelling_pipeline(correct_name_prompt, max_length=2048)
    return suggestion

    # # ================ SOLUTION 2 ========================
    # # extract name strings, call the spell check on them,
    # # call spell check on the remaining sentence
    # # with placeholder values for the name.
    # # If time, implement multithreading?
