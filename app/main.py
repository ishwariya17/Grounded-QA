from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
import app.models
from app import crud, schemas
from app.llm import ask_llm
from app.history import save_session, get_history

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Grounded QA API"
)


@app.get("/")
def home():
    return {"message": "Welcome to Grounded QA API"}

# DOCUMENT APIs

@app.get("/documents", response_model=list[schemas.DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return crud.get_documents(db)


@app.get("/documents/{document_id}/chunks",
         response_model=list[schemas.ChunkResponse])
def list_chunks(document_id: int,
                db: Session = Depends(get_db)):
    return crud.get_chunks_by_document(db, document_id)


@app.get("/search",
         response_model=list[schemas.ChunkResponse])
def search(keyword: str,
           db: Session = Depends(get_db)):
    return crud.search_chunks(db, keyword)

# SELECTION APIs

@app.post(
    "/selections",
    response_model=schemas.SelectionResponse
)
def create_selection(
    selection: schemas.SelectionCreate,
    db: Session = Depends(get_db)
):
    return crud.create_selection(
        db,
        selection.name,
        selection.chunk_ids
    )


@app.get(
    "/selections",
    response_model=list[schemas.SelectionResponse]
)
def list_selections(
    db: Session = Depends(get_db)
):
    return crud.get_selections(db)

# GROUNDED QUESTION ANSWERING

@app.post(
    "/ask",
    response_model=schemas.QuestionResponse
)
def ask_question(
    request: schemas.QuestionRequest,
    db: Session = Depends(get_db)
):

    # Fetch selection from database
    selection = crud.get_selection_chunks(
        db,
        request.selection_id
    )

    # If selection doesn't exist
    if not selection:
        return {
            "answer": "Selection not found.",
            "citations": []
        }

    # Ask Gemini using the selected chunks
    result = ask_llm(
        question=request.question,
        chunks=selection.chunks
    )

    # Save the session to history
    save_session(
        question=request.question,
        answer=result["answer"],
        selection_id=request.selection_id,
        citations=result["citations"]
    )

    return result

@app.get(
    "/history",
    response_model=list[schemas.HistoryResponse]
)
def history():

    return get_history()