from fastapi import APIRouter, UploadFile, File
import os

from utils.extract_pdf import extract_pdf
from utils.extract_docx import extract_docx
from utils.extract_text import extract_text
from utils.nlp_processor import clean_text
from core.text_splitter import split_into_chunks
from core.embeddings import embed_text
from utils.chroma_manager import store_vectors, reset_chroma

router = APIRouter()
UPLOAD_DIR = "uploaded_files/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        print("=== UPLOAD STARTED ===")

        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("File saved:", file_path)

        # Remove old uploaded files (keep only current)
        for existing in os.listdir(UPLOAD_DIR):
            if existing != file.filename:
                os.remove(os.path.join(UPLOAD_DIR, existing))
        print("Old uploaded files cleared.")

        # Extract text
        if file.filename.endswith(".pdf"):
            raw_text = extract_pdf(file_path)
        elif file.filename.endswith(".docx"):
            raw_text = extract_docx(file_path)
        else:
            raw_text = extract_text(file_path)

        print("Text extraction done. Length:", len(raw_text))

        # Clean text
        cleaned = clean_text(raw_text)
        print("Cleaned text length:", len(cleaned))

        # Split text into chunks
        chunks = split_into_chunks(cleaned)
        print("Total chunks:", len(chunks))

        # Embed chunks
        embeddings = embed_text(chunks)
        print("Embeddings completed.")

        # IMPORTANT: Reset database so ONLY this new file exists
        reset_chroma()

        # Store vectors
        store_vectors(chunks, embeddings)

        print("=== UPLOAD FINISHED ===")
        return {"message": "Document processed successfully", "chunks": len(chunks)}

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return {"error": str(e)}
