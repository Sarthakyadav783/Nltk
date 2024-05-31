from span_marker import SpanMarkerModel
from handle_spellcheck import punctuation_spacing, give_suggestion
import add_noise
import string
import re


if __name__ == "__main__":

    ner_model = SpanMarkerModel.from_pretrained(
        "tomaarsen/span-marker-roberta-large-ontonotes5")
    ner_model.cuda()

    # for char in string.punctuation:
    #     input = "I went to the park with my friend Kushagra" + char + " Vagisha joined us later" + char
    #     prompt = punctuation_spacing(input)
    name = "J. V. Ramana"
    input = add_noise.noisy(" How many votes did ", 0.15) + \
        add_noise.noisy(name, 0) + add_noise.noisy(",. have? ", 0.15)
    prompt = punctuation_spacing(input)
    output = give_suggestion(prompt, ner_model.predict(prompt))

    print("Input: {x}".format(x=input))
    print("Output: {y}\n".format(y=output))
