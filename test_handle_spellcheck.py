from span_marker import SpanMarkerModel
from handle_spellcheck import punctuation_spacing, give_suggestion
import add_noise
import string, re


if __name__ == "__main__":

    ner_model = SpanMarkerModel.from_pretrained("tomaarsen/span-marker-roberta-large-ontonotes5")
    ner_model.cuda()

    # for char in string.punctuation:
    #     input = "I went to the park with my friend Kushagra" + char + " Vagisha joined us later" + char
    #     prompt = punctuation_spacing(input)
    #     print("Input: {x}".format(x = input))
    #     print("Output: {y}\n".format(y = prompt))
    input = add_noise.noisy(" How many votes did Ashlok. have?", 0.15)
    prompt = punctuation_spacing(input)
    print(give_suggestion(prompt, ner_model.predict(prompt)))