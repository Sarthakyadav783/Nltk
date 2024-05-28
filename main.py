from fastapi import FastAPI
app=FastAPI()
 
@app.get("/")
def string_correct():
    pass