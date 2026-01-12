import docx

def extract_docx(file_path):
    """
    Extract text from .docx using python-docx.
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    except Exception as e:
        print("DOCX EXTRACT ERROR:", e)
        return ""
