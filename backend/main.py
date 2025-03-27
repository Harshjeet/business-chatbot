from fastapi import FastAPI
from pydantic import BaseModel
import requests
import google.generativeai as genai
import os


app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API"))

# requesting model for input to validation
class QueryRequest(BaseModel):
    query: str
    focused_word: str
    
def prompt(query: str, focused_word: str):
    return f"""
    You are an AI business Insights Assistant. Analyze the following question in the context of {focused_word}. 
    Provide a structured, detailed and actionable response. 
    
    Question: {query}
    
    structure your response in these sections:
    1. key insights
    2. Market Trends
    3. Strategic Recommendation
    """
    
# api endpoints
@app.post("/query")
async def query_processor(request: QueryRequest):
    get_prompt = prompt(request.query, request.focused_word)
    
    # call the gemini api
    response = genai.GenerativeModel("gemini-2.0-flash").generate_content(prompt)
    return {"query": request.query, "response":response.text}