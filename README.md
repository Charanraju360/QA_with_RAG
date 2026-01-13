# RAG Document Assistant

A Retrieval-Augmented Generation (RAG) system that allows users to upload documents (PDF, DOCX, TXT) and ask questions about their content. The system uses vector embeddings and a large language model to provide accurate, context-aware answers.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT file formats
- **Intelligent Q&A**: Ask questions about uploaded documents and get context-aware answers
- **Vector Search**: Uses ChromaDB for efficient vector similarity search
- **Modern UI**: Clean, responsive web interface
- **FastAPI Backend**: High-performance REST API
- **Embeddings**: Sentence transformers for text vectorization
- **LLM Integration**: Powered by OpenRouter API with GPT-4o-mini for answer generation

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **ChromaDB**: Vector database for storing document embeddings
- **Sentence Transformers**: For generating text embeddings
- **OpenRouter API**: For LLM-powered answer generation
- **PyMuPDF**: PDF text extraction
- **python-docx**: DOCX text extraction
- **NLTK**: Natural language processing utilities

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Prerequisites
- Python 3.8+
- Node.js (for serving frontend, optional)
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Charanraju360/QA_with_RAG.git
cd QA_with_RAG
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the backend directory with:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

5. Run the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

The frontend is static HTML/CSS/JS files. Simply open `frontend/index.html` in your browser, or serve it using any static file server.

For development, you can use Python's built-in server:
```bash
cd frontend
python -m http.server 3000
```

Then open `http://localhost:3000` in your browser.

## Usage

1. **Start the Backend**: Ensure the FastAPI server is running on port 8000
2. **Open Frontend**: Open `frontend/index.html` in your browser
3. **Upload Document**: Click "Choose File" and select a PDF, DOCX, or TXT file
4. **Process Document**: Click "Process Document" to upload and process the file
5. **Ask Questions**: Once processed, you can ask questions about the document content

## API Endpoints

### POST /api/upload
Upload a document for processing.

**Request**: Multipart form data with `file` field
**Supported formats**: PDF, DOCX, TXT
**Response**:
```json
{
  "message": "Document processed successfully",
  "chunks": 42
}
```

### POST /api/ask
Ask a question about the uploaded document.

**Request**:
```json
{
  "question": "What is the main topic of the document?"
}
```

**Response**:
```json
{
  "answer": "The main topic is machine learning and AI applications."
}
```

## Project Structure

```
QA_with_RAG/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── api/
│   │   ├── upload.py        # Document upload endpoint
│   │   └── ask.py           # Question answering endpoint
│   ├── core/
│   │   ├── embeddings.py    # Text embedding utilities
│   │   ├── llm.py           # LLM integration
│   │   └── text_splitter.py # Document chunking
│   └── utils/
│       ├── chroma_manager.py # Vector database operations
│       ├── extract_pdf.py    # PDF text extraction
│       ├── extract_docx.py   # DOCX text extraction
│       └── extract_text.py   # General text processing
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── style.css            # CSS styles
│   └── script.js            # Frontend JavaScript
└── README.md                # This file
```

## How It Works

1. **Document Upload**: When a document is uploaded, it's processed and split into chunks
2. **Text Extraction**: Content is extracted based on file type (PDF/DOCX/TXT)
3. **Embedding Generation**: Each chunk is converted to a 384-dimensional vector using sentence transformers
4. **Vector Storage**: Embeddings are stored in ChromaDB for efficient retrieval
5. **Question Processing**: User questions are embedded and used to find similar document chunks
6. **Answer Generation**: Relevant chunks are passed to the LLM along with the question to generate a contextual answer

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Sentence Transformers](https://www.sbert.net/) for embeddings

