from fastapi import FastAPI , requests

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}