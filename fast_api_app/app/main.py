from fastapi import FastAPI

app=FastAPI(title="E-Commerce API")

@app.get("/")
def home():
    return{
        "message":"API Running"
    }