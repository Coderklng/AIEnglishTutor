from langchain_groq import ChatGroq

class ChatGroqService:
    def __init__(self,api_key):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key 
        )
        
    def invoke(self,user_query):
        return self.llm.invoke(user_query)