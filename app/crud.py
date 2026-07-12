from sqlalchemy.orm import Session
from app.models import Document, Chunk
from app.models import Selection

def get_documents(db: Session):
    return db.query(Document).all()


def get_chunks_by_document(db: Session, document_id: int):
    return (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.chunk_number)
        .all()
    )


def search_chunks(db: Session, keyword: str):
    return (
        db.query(Chunk)
        .filter(Chunk.content.ilike(f"%{keyword}%"))
        .all()
    )

def create_selection(db: Session, name: str, chunk_ids: list[int]):

    chunks = (
        db.query(Chunk)
        .filter(Chunk.id.in_(chunk_ids))
        .all()
    )

    selection = Selection(
        name=name,
        chunks=chunks
    )

    db.add(selection)
    db.commit()
    db.refresh(selection)

    return selection

def get_selections(db: Session):
    return db.query(Selection).all()

def get_selection_chunks(db: Session, selection_id: int):

    selection = (
        db.query(Selection)
        .filter(Selection.id == selection_id)
        .first()
    )

    return selection

from app.models import Selection

def get_selection_by_id(db: Session, selection_id: int):
    return (
        db.query(Selection)
        .filter(Selection.id == selection_id)
        .first()
    )