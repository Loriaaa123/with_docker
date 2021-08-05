  
from pydantic import BaseModel


class FeedbackIn(BaseModel):
    service_name: str
    tag: str
    data: str

class Feedback(BaseModel):
    id: int
    service_name: str
    tag: str
    created_at: str
    data: str

