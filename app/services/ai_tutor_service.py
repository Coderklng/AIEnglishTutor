from prompts.ai_tutor_prompt import AITutorPrompt
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
import uuid
import sqlite3 
import re 
from fastapi import FastAPI,BackgroundTasks
import edge_tts
import speech_recognition as sp
import os 
import sys 
from playsound import playsound
import json 


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH = os.path.join(BASE_DIR, "Audio")

class TextFilter:

     def clean_text(self,text:str):
         text = re.sub(r'[^a-zA-Z0-9\n]','',text)
         return text 


texts = TextFilter()

class AIService:

    def __init__(self,llm,parser):
        self.llm = llm
        self.parser = parser
        
    def get_session(self,session_id):
         return SQLChatMessageHistory(
                       session_id=session_id,
                      connection="sqlite:///ai_tutor.db", # Ensure the path is a valid file name
                     table_name="chat_message_history"
              )
         
         
    def  get_history(self):
        with sqlite3.connect("ai_tutor.db") as con:
              con.row_factory = sqlite3.Row
              query = "SELECT * FROM chat_message_history"
              cursor = con.execute(query)
              data = [dict(row) for row in cursor.fetchall()]
              return data     
     
     
    def get_history_id(self,session_id):
         with sqlite3.connect("ai_tutor.db") as con:
             query = "SELECT * FROM chat_message_history WHERE session_id=?"
             res = con.execute(query,(session_id,))
             data = [response for response in res.fetchone()]
             return data                 
     
    
    async def speak(self,text):
        voice = "hi-IN-SwaraNeural"
        speaker = edge_tts.Communicate(text=text,voice=voice,rate="+10%",pitch="+10Hz")
        audio_name = text.split(" ")
        audio_name = audio_name[:10]
        audio = "".join(audio_name)
        text_filter = texts.clean_text(audio)
        loc = f"{FOLDER_PATH}/{text_filter}.mp3"
        await speaker.save(loc)
        audio_player = playsound(loc)
        return audio_player
        
     
    
    def chat_with_ai(self,user_query,background:BackgroundTasks):
        
        prompt = AITutorPrompt.create_prompt()
        
        llm = self.llm 
        
        chain = prompt | llm 
        
        memory = RunnableWithMessageHistory(
              chain,
              self.get_session,
              input_messages_key="query",
              history_messages_key="history_chat"    
        )
        
        user_id = f"user_{uuid.uuid4()}"
        
        config = {"configurable":{"session_id":user_id}}
        
        res = memory.invoke({
           "query" : user_query,
           "format_instruction" : self.parser.get_format_instructions()
        
        },config=config)
        
        response =  res.model_dump_json()  if hasattr(res,"model_dump_json") else str(res)
        
        
        try:
            response_data = json.loads(response)       

            inner_response = json.loads(response_data["content"])
        
            data = inner_response.get("response","")
        
            if data:
                clean_data = texts.clean_text(data)
                background.add_task(self.speak,str(clean_data))
    

        except Exception as e:
             print(f"Error:{e}")
         
        return {
            "query" : user_query,
            "response" : response,
            "session_id" : f"http://localhost:8000/history/{user_id}"
        }
        
    