from tinydb import TinyDB

# Creates history.json automatically
db = TinyDB("history.json")

history = db.table("qa_history")


def save_session(question, answer, selection_id, citations):
    history.insert({
        "question": question,
        "answer": answer,
        "selection_id": selection_id,
        "citations": citations
    })


def get_history():
    return history.all()