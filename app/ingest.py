import os
import re

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Document, Chunk


DATA_FOLDER = "data"


def ingest_documents():

    db: Session = SessionLocal()

    try:

        # Loop through all txt files
        for filename in os.listdir(DATA_FOLDER):

            if not filename.endswith(".txt"):
                continue

            filepath = os.path.join(DATA_FOLDER, filename)

            # Avoid duplicate loading
            existing_doc = db.query(Document).filter(Document.name == filename).first()

            if existing_doc:
                print(f"{filename} already exists.")
                continue

            # Read file
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()

            # Create document
            document = Document(name=filename)

            db.add(document)
            db.commit()
            db.refresh(document)

            # Split into numbered chunks
            chunks = re.split(r"\n(?=\d+\.)", text)

            for chunk in chunks:

                chunk = chunk.strip()

                if not chunk:
                    continue

                match = re.match(r"(\d+)\.\s*(.*)", chunk, re.DOTALL)

                if match:

                    chunk_number = int(match.group(1))

                    content = match.group(2).strip()

                    db_chunk = Chunk(
                        document_id=document.id,
                        chunk_number=chunk_number,
                        content=content
                    )

                    db.add(db_chunk)

            db.commit()

            print(f"{filename} loaded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    ingest_documents()