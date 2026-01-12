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
        # Embed question → 384-d
        question_vec = embed_text([req.question])[0]

        # Search top chunks
        chunks = search_vectors(question_vec)

        if not chunks:
            return {"answer": "The answer is not present in the document."}

        # Combine into context
        context = "\n".join(chunks)

        # Generate LLM response
        answer = generate_answer(req.question, context)

        return {"answer": answer}

    except Exception as e:
        print("ASK ERROR:", e)
        return {"error": str(e)}
