import google.generativeai as genai
import os
from datetime import datetime

class GeminiFunction:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def content_insight(self, prompt):
        try:
            start_time = datetime.now()
            response = self.model.content_insight(prompt)
            latency = (datetime.now()) - (start_time).total_seconds()
            
            return {
                'content': response.text,
                'latency': latency,
                'error': None
            }
        except Exception as e:
            return {
                'content': None,
                'latency': 0,
                'error': str(e)
            }