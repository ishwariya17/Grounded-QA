# Grounded QA API – Approach Document

# 1. Chunking Strategy

The system ingests the three SOP documents provided in the data/ directory. Each document is divided into chunks by splitting on the numbered sections (1., 2., 3., …), since every numbered section represents a self-contained piece of information. During ingestion, each chunk is stored along with its associated metadata, including the document ID, chunk number, and chunk content. This approach keeps the chunking process simple while ensuring that retrieved information remains meaningful and easy to reference.

# 2. Data Model

The project uses SQLite with SQLAlchemy for structured data storage.

The relational database contains the following entities:

## Document

Stores information about each SOP document.

Document ID
Document Name

## Chunk

Stores every chunk extracted from a document.

Chunk ID
Document ID
Chunk Number
Chunk Content

Each chunk is linked to exactly one document through a foreign key relationship.

## Selection

A selection represents a user-selected group of chunks that may belong to one or more documents.

Each selection stores:

Selection ID
Selection Name

A many-to-many relationship is used between Selections and Chunks, allowing the same chunk to belong to multiple selections.

## History

Question-and-answer history is stored separately using a NoSQL-style JSON store (TinyDB). Each history record contains:

User Question
Generated Answer
Selection ID
Citation Chunk IDs

This separation keeps structured document data in SQL while allowing flexible storage of conversation history.

# 3. Prompt Design for Enforcing Grounding

To ensure grounded responses, only the selected chunks are included in the prompt sent to the LLM.

Each chunk is labelled with its chunk ID before being passed to Gemini.

## Example prompt structure:

Context:

[Chunk 6]
Sterilization: Autoclave at 134°C for 18 minutes.

[Chunk 10]
Shelf Life: Use within 30 days.

Question:
What is the sterilization temperature?

## The prompt includes the following instructions:

Answer only using the provided context.
Do not use external knowledge.
If the answer is unavailable, return:
"The answer is not available in the selected chunks."
Return only the final answer.

This prompt design minimizes hallucinations and ensures every answer is grounded in the selected SOP content.

# 4. Trade-offs and Future Improvements

## Current Trade-offs

Documents are chunked only by numbered sections instead of using semantic or token-based chunking.

Keyword search is implemented using SQL LIKE queries rather than semantic vector search.

Citations currently include all selected chunk IDs instead of identifying only the chunks directly used by the LLM.

The system uses a simple prompt-based grounding mechanism without retrieval ranking.

## Future Improvements

If more development time were available, the following enhancements would be implemented:

* Semantic chunking for improved retrieval quality.
* Embedding-based vector search using FAISS or ChromaDB.
* Automatic citation extraction to identify only the chunks actually used in the answer.
* Re-ranking retrieved chunks before sending them to the LLM.
* User authentication and management of multiple projects.
* Streaming responses for better user experience.
* Support for uploading arbitrary PDF and DOCX documents instead of fixed SOP files.

## Technologies Used

FastAPI
Pydantic
SQLAlchemy
SQLite
TinyDB (History Storage)
Google Gemini API
Python
