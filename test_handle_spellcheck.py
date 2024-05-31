from span_marker import SpanMarkerModel
from handle_spellcheck import punctuation_spacing, give_suggestion
import string, re


if __name__ == "__main__":
        
    ner_model = SpanMarkerModel.from_pretrained("tomaarsen/span-marker-roberta-large-ontonotes5")
    ner_model.cuda()

    input = "I went to the park with my friend Kushagra. Vagisha joined us later. another sentence."
    prompt = punctuation_spacing(input)

    # x = r"\."
    # ans = re.sub(x, " {c} ".format(c="."), input)
    # print(ans)

    # print(give_suggestion(prompt, ner_model.predict(prompt)))