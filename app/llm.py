import os
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_llm(question: str, chunks: list):
    """
    Ask Gemini using the selected chunks only.
    """

    context = ""
    citations = []

    # Build context from selected chunks
    for chunk in chunks:
        context += f"[Chunk {chunk.id}]\n{chunk.content}\n\n"
        citations.append(chunk.id)

    prompt = f"""
You are a grounded Question Answering assistant.

Answer ONLY using the information provided in the context below.

Rules:
- Do not use your own knowledge.
- Answer only the user's question.
- Do not include extra information unless it is necessary.
- Keep the answer concise (1–2 sentences).
- If the answer is not present in the context, reply exactly:
  "The answer is not available in the selected chunks."

Context:
{context}

Question:
{question}

Return only the answer.
"""

    # Call Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return {
        "answer": response.text,
        "citations": citations
    }