from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ChunkResponse(BaseModel):
    id: int
    chunk_number: int
    content: str

    class Config:
        from_attributes = True

class SelectionCreate(BaseModel):
    name: str
    chunk_ids: list[int]


class SelectionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class QuestionRequest(BaseModel):
    selection_id: int
    question: str


class QuestionResponse(BaseModel):
    answer: str
    citations: list[int]

class HistoryResponse(BaseModel):
    question: str
    answer: str
    selection_id: int
    citations: list[int]