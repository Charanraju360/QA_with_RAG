import fitz  # PyMuPDF

def extract_pdf(file_path):
    """
    Extracts text from PDF using PyMuPDF (best speed + layout retention).
    """
    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    except Exception as e:
        print("PDF EXTRACT ERROR:", e)
        return ""
