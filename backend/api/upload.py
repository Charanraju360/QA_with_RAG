from fastapi import APIRouter, UploadFile, File
import os
from utils.extract_pdf import extract_pdf
from utils.extract_docx import extract_docx
from utils.extract_text import extract_text

from utils.nlp_processor import clean_text
from core.text_splitter import split_into_chunks
from core.embeddings import embed_text
from utils.chroma_manager import store_vectors

router = APIRouter()
UPLOAD_DIR = "uploaded_files/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    print("=== UPLOAD STARTED ===")

    try:
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        print("Saving file to:", file_path)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        print("File saved successfully")

        # Extract text
        print("Extracting text...")
        if file.filename.endswith(".pdf"):
            raw_text = extract_pdf(file_path)
        elif file.filename.endswith(".docx"):
            raw_text = extract_docx(file_path)
        else:
            raw_text = extract_text(file_path)

        print("Text extraction complete, length:", len(raw_text))

        # Clean text
        print("Cleaning text...")
        cleaned = clean_text(raw_text)
        print("Cleaned length:", len(cleaned))

        # Split
        print("Splitting into chunks...")
        chunks = split_into_chunks(cleaned)
        print("Chunks:", len(chunks))

        # Embed
        print("Generating embeddings...")
        embeddings = embed_text(chunks)
        print("Embedding complete. Example vector length:", len(embeddings[0]))

        # Store
        print("Storing vectors in Chroma...")
        store_vectors(chunks, embeddings)
        print("Stored successfully")

        print("=== UPLOAD FINISHED ===")
        return {"message": "Document processed", "chunks": len(chunks)}

    except Exception as e:
        print("UPLOAD ERROR >>>", str(e))
        return {"error": str(e)}
