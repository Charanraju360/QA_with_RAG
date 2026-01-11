from fastapi import APIRouter
from pydantic import BaseModel
from core.embeddings import embed_text
from utils.chroma_manager import search_vectors
from core.llm import generate_answer

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(req: AskRequest):
    try:
        # embed the question
        query_embedding = embed_text([req.question])[0]

        # search chroma
        chunks = search_vectors(query_embedding)

        # generate answer using LLM
        answer = generate_answer(req.question, chunks)

        return {"answer": answer}

    except Exception as e:
        print("ASK ERROR >>>", str(e))
        return {"error": str(e)}
