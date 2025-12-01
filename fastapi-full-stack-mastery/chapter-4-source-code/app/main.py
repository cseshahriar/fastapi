from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def home():
    ''' home '''
    return {"message": "Hello Fast aPI"}
