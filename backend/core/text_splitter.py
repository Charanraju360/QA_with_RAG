import re

def split_into_chunks(text, chunk_size=800, overlap=150):
    """
    Splits text into overlapping chunks.

    chunk_size: size of each chunk
    overlap: repeated content between chunks for better recall
    """

    # clean multiple spaces
    text = re.sub(r"\s+", " ", text)

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap  # move window with overlap

    return chunks
