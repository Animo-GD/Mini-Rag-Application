from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/home")
def home():
    return {"message":"Hello To Home Page"}


