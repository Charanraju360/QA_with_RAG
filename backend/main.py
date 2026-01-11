from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router
from api.ask import router as ask_router

import openai

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "YOUR_OPENROUTER_API_KEY"

app = FastAPI(title="RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(ask_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Backend running"}


