from fastapi import FastAPI
from pydantic import BaseModel
import requests
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key="AIzaSyDmmYbFR3b1f1pPekqgAdVtlHNY14s2jxU")

# requesting model for input to validation
class QueryRequest(BaseModel):
    query: str
    focused_word: str
    
