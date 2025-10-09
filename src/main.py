from fastapi import FastAPI

#1. Create an instance of the FastAPI applicaton 
app = FastAPI()

#2. Define a 'path operation decorator" 
@app.get("/")
def read_root():
    #3. Define the path operation function 
    return {"Hello": "World"}

