from fastapi import FastAPI


# create fast api instance
app = FastAPI()


@app.get("/")
def home():
    ''' root api '''
    return {"message": "Hello Fast API"}


# run: fastapi dev main.py
# run: uvicorn main:app --reload
