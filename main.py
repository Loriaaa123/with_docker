import os
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import FeedbackModel
from schemas import Feedback, FeedbackIn

app = FastAPI(title="Simple Feedback API")

load_dotenv(".env")
DATABASE_URL = os.environ["DATABASE_URL"]
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs/")

@app.get("/feedbacks/")
def get_all_feedback(offset: int=0, limit: int=20):
    all_feedback = db.session.query(FeedbackModel).offset(offset).limit(limit).all()

    return all_feedback

@app.post("/feedbacks/")
def post_feedback(feedback: FeedbackIn):
    new_feedback =  FeedbackModel(service_name=feedback.service_name, tag=feedback.tag, data=feedback.data)
    db.session.add(new_feedback)
    db.session.commit()

    return {
        "id": new_feedback.id,
        "service_name": new_feedback.service_name,
        "tag": new_feedback.tag,
        "created_at": new_feedback.created_at,
        "data": new_feedback.data
    }


@app.get("/feedbacks/{feedback_id}/")
def get_feedback_by_id(feedback_id: int):
    feedback = db.session.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
    return feedback

@app.delete("/feedbacks/{feedback_id}/")
async def delete_feedback(feedback_id: int):
    query = db.session.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
    db.session.delete(query)
    db.session.commit()
    return f"feedback with id: {feedback_id} was deleted succesfully!" 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)