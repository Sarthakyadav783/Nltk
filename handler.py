from transformers import pipeline
from span_marker import SpanMarkerModel
import warnings
from handler_helper import punctuation_spacing, correct_name, ask_spellcheck_pipeline
from nltk_correct_txt import did_you_mean


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


# ================ MAIN FUNCTION ========================
def handle_spellcheck(input: str, transpositions=False) -> list:
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
    # # can't decide between the two spellchecking solutions for the sentence
    # # will simply try both and pick better one each time for now
    correct_name_prompt = correct_name(
        prompt, ner_model.predict(prompt), transpositions)

    pipeline_suggestion = ask_spellcheck_pipeline(
        spelling_pipeline, correct_name_prompt)
    nltk_suggestion = did_you_mean(correct_name_prompt)

    return [pipeline_suggestion, nltk_suggestion]

    # # ================ SOLUTION 2 ========================
    # # extract name strings, call the spell check on them,
    # # call spell check on the remaining sentence
    # # with placeholder values for the name.
    # # If time, implement multithreading? might not be worth the hassle though
