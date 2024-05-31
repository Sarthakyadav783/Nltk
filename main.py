from fastapi import FastAPI
from handler import handle_spellcheck


app = FastAPI()


@app.get("/")
def string_correct(input: str):
    # note: Are we guaranteed input will be in english? not sure how the model
    # would respond to input in another language
    # Model struggles when name surrounded by punctuation, so:
    suggestions = handle_spellcheck(input, transpositions=True)

    suggestion = suggestions[1]
    return suggestion
