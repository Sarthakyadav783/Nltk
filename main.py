from fastapi import FastAPI
from span_marker import SpanMarkerModel
from handle_spellcheck import punctuation_spacing, give_suggestion


app=FastAPI()
# note: Are we guaranteed input will be in english? not sure how the model
# would respond to input in another language 
ner_model = SpanMarkerModel.from_pretrained("tomaarsen/span-marker-roberta-large-ontonotes5")
ner_model.cuda()

@app.get("/")
def string_correct(input: str):

    # Model struggles when name surrounded by punctuation, so:
    prompt = punctuation_spacing(input)
    suggestion = give_suggestion(prompt, ner_model.predict(prompt))
    return suggestion