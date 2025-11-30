from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    ''' home api '''
    return {"message": "Hello World"}
