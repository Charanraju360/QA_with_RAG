from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from api.upload import router as upload_router
from api.ask import router as ask_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(ask_router, prefix="/api")
