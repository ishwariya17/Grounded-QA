# Grounded QA API
## Overview

Grounded QA API is a backend service built using **FastAPI** that ingests Standard Operating Procedure (SOP) documents, splits them into chunks, stores them in a SQLite database, allows users to create selections of document chunks, and answers questions using **Google Gemini 3.5 Flash**. The system is designed to provide **grounded responses**, meaning the Large Language Model (LLM) generates answers using **only the selected chunks** instead of relying on its own knowledge. Each response includes citations to the chunks that were used.

# Features

- Ingest SOP documents into a database
- Split documents into numbered chunks
- Store documents, chunks, and selections using SQLite
- Search chunks using keywords
- Create reusable chunk selections
- Ask grounded questions using Gemini 3.5 Flash
- Return answers with chunk citations
- Store Question & Answer history using TinyDB
- Interactive API documentation using Swagger UI

# Tech Stack

- Python 3.x
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- TinyDB
- Google Gemini 3.5 Flash
- Uvicorn
- python-dotenv

# Project Structure
```text
Grounded-QA/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── ingest.py
│   ├── llm.py
│   ├── history.py
│   └── __init__.py
│
├── data/
│   ├── SOP-014.txt
│   ├── SOP-021.txt
│   └── SOP-030.txt
│
├── groundedqa.db
├── history.json
├── .env
├── requirements.txt
├── README.md
└── approach.md
```

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd Grounded-QA
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

# Environment Variables

Create a file named **.env** in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Obtain your free API key from **Google AI Studio** and replace `YOUR_GEMINI_API_KEY` with your own key.

# Load Documents

Before starting the server, run the ingestion script.

```bash
python -m app.ingest
```

The ingestion script:

- Reads the SOP documents from the `data/` folder
- Splits each document into numbered chunks
- Stores documents and chunks into the SQLite database

This step only needs to be run once unless the documents are modified.

# Run the Application

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

The API will be available at

```text
http://127.0.0.1:8000
```

Swagger documentation

```text
http://127.0.0.1:8000/docs
```

# API Endpoints

## Home

**GET**

```text
/
```

Returns a welcome message.

## List Documents

**GET**

```text
/documents
```

Returns all available SOP documents.

## List Chunks

**GET**

```text
/documents/{document_id}/chunks
```

Returns all chunks for the selected document.

Example

```text
/documents/1/chunks
```

## Search Chunks

**GET**

```text
/search?keyword=sterilization
```

Returns chunks containing the specified keyword.

## Create Selection

**POST**

```text
/selections
```

Example Request

```json
{
  "name": "Sterilization",
  "chunk_ids": [1,2,6,10]
}
```

Creates a reusable selection of chunks.

## List Selections

**GET**

```text
/selections
```

Returns all saved selections.

## Ask a Question

**POST**

```text
/ask
```
Example Request

```json
{
  "selection_id": 1,
  "question": "What is the sterilization temperature?"
}
```
Example Response

```json
{
  "answer": "The sterilization temperature is 134°C.",
  "citations": [6,2,1,10]
}
```

## View History

**GET**

```text
/history
```

Returns all previous Question & Answer sessions stored in TinyDB.

# Database Design

## SQLite

The relational database stores:

- Documents
- Chunks
- Selections

Relationships:

- One Document → Many Chunks
- Many Selections ↔ Many Chunks

## TinyDB

TinyDB stores Question & Answer history including:

- Question
- Generated Answer
- Selection ID
- Citation Chunk IDs

This allows flexible storage of conversation history.

# Grounded Question Answering

The application uses **Google Gemini 3.5 Flash** as the Large Language Model.

When a question is asked:

1. The selected chunk IDs are retrieved.
2. Only those chunks are combined into the prompt.
3. Gemini receives only the selected context.
4. The model generates an answer strictly from that context.
5. The API returns:
   - Generated answer
   - Citation chunk IDs

If the required information is not available, the model returns:

```text
The answer is not available in the selected chunks.
```

This prevents hallucinations and ensures grounded responses.

# How to Test the API

Start the server.

```bash
uvicorn app.main:app --reload
```

Open Swagger UI.

```text
http://127.0.0.1:8000/docs
```

Test the endpoints in the following order.

## Step 1

GET

```text
/documents
```

Expected Result

- Lists all SOP documents.

## Step 2

GET

```text
/documents/1/chunks
```

Expected Result

- Lists all chunks belonging to document 1.

## Step 3

GET

```text
/search?keyword=sterilization
```

Expected Result

- Returns matching chunks containing the keyword.

## Step 4

POST

```text
/selections
```

Request

```json
{
  "name": "Sterilization",
  "chunk_ids": [1,2,6,10]
}
```

Expected Result

A new selection is created.

## Step 5

GET

```text
/selections
```

Expected Result

Lists all saved selections.

## Step 6

POST

```text
/ask
```

Request

```json
{
  "selection_id": 1,
  "question": "What is the sterilization temperature?"
}
```

Expected Result

```json
{
  "answer": "The sterilization temperature is 134°C.",
  "citations": [6,2,1,10]
}
```

## Step 7

POST

```text
/ask
```

Request

```json
{
  "selection_id": 1,
  "question": "Who is the CEO?"
}
```

Expected Result

```json
{
  "answer": "The answer is not available in the selected chunks.",
  "citations": [6,2,1,10]
}
```

This confirms that the LLM is grounded and does not hallucinate.

## Step 8

GET

```text
/history
```

Expected Result

Returns all previous questions, answers, selection IDs, and citation IDs.

# Requirements

Install all required packages using

```bash
pip install -r requirements.txt
```

Typical dependencies include:

- fastapi
- uvicorn
- sqlalchemy
- pydantic
- tinydb
- python-dotenv
- google-genai

# Future Improvements

- Semantic chunking
- Vector database integration (FAISS/ChromaDB)
- Embedding-based retrieval
- Automatic citation extraction
- User authentication
- PDF and DOCX document upload support
- Streaming responses

# Author

Grounded QA API developed as part of a backend assignment demonstrating document ingestion, chunk-based retrieval, grounded question answering, and citation-based response generation using FastAPI and Google Gemini.
