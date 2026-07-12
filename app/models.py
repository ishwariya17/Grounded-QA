from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.database import Base

# Association table for many-to-many relationship
selection_chunks = Table(
    "selection_chunks",
    Base.metadata,
    Column("selection_id", Integer, ForeignKey("selections.id")),
    Column("chunk_id", Integer, ForeignKey("chunks.id"))
)

# Document Table

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    chunks = relationship("Chunk", back_populates="document")

# Chunk Table

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(Integer, ForeignKey("documents.id"))

    chunk_number = Column(Integer)

    content = Column(Text)

    document = relationship("Document", back_populates="chunks")

    selections = relationship(
        "Selection",
        secondary=selection_chunks,
        back_populates="chunks"
    )

# Selection Table

class Selection(Base):
    __tablename__ = "selections"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    chunks = relationship(
        "Chunk",
        secondary=selection_chunks,
        back_populates="selections"
    )