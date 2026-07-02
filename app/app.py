from fastapi import FastAPI,BackgroundTasks
from services.llm_service import ChatGroqService
from services.ai_tutor_service import AIService
import uvicorn
import os 
from dotenv import load_dotenv
from schemas.request_tutor import ChatRequest
from langchain_core.output_parsers import PydanticOutputParser
from schemas.tutor_request import ChatRequestByAI

load_dotenv()


api_key  = os.getenv("API_KEY")


parser = PydanticOutputParser(pydantic_object=ChatRequestByAI)

groq = ChatGroqService(
    api_key=api_key
)


tutor = AIService(
    llm=groq.llm,
    parser=parser
)

app = FastAPI(title="My API")



@app.post("/ai_tutor")
def Tutor(request:ChatRequest,background_tasks:BackgroundTasks):
    query = request.query
    return  tutor.chat_with_ai(
        user_query=query,
        background=background_tasks
    )

    
     
@app.get("/chat/history")
def history():
    return tutor.get_history()




@app.post("/history/{session_id}")
def get_session_history(session_id):
    return tutor.get_history_id(session_id=session_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000)