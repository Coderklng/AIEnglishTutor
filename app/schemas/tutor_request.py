from pydantic import BaseModel,Field

class ChatRequestByAI(BaseModel):
        query : str 
        response : str
        improved_flow : str
        continues : str

    