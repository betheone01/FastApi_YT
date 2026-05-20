
from fastapi import FastAPI, Body


app= FastAPI() #Instantiate Fastapi 


# path operation or route
#"/" is root path 
@app.get("/") #decorator
def root():
    return {"Message":"Welcome To The FastApi"}



@app.get("/posts")
def get_posts():
    return {"data":"This is the posts"}


@app.post("/posts")
def create_post(payload:dict=Body(...)):
    print(payload)
    return {"Message":payload}