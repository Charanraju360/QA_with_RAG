def extract_text(file_path):
    """
    Fallback extractor for .txt and unknown formats.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print("TEXT EXTRACT ERROR:", e)
        return ""
