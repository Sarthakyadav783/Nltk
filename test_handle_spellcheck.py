from span_marker import SpanMarkerModel
from transformers import pipeline
from handle_spellcheck import punctuation_spacing, give_suggestion
import add_noise
import string
import re


if __name__ == "__main__":

    ner_model = SpanMarkerModel.from_pretrained(
        "tomaarsen/span-marker-roberta-large-ontonotes5")
    ner_model.cuda()

    eng_spell_pipeline = pipeline("text2text-generation", model="oliverguhr/spelling-correction-english-base")

    # for char in string.punctuation:
    #     input = "I went to the park with my friend Kushagra" + char + " Vagisha joined us later" + char
    #     prompt = punctuation_spacing(input)
    name = "J. V. Ramana"
    input = add_noise.noisy(" How many votes did ", 0.15) + \
        add_noise.noisy(name, 0) + add_noise.noisy(",. have? ", 0.15)
    print("Input: {x}".format(x=input))
    prompt = punctuation_spacing(input)
    output = eng_spell_pipeline(give_suggestion(prompt, ner_model.predict(prompt)), max_length=2048)

    print("Input: {x}".format(x=input))
    print("Output: {y}\n".format(y=output))
