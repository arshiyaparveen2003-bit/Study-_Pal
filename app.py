import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
import PyPDF2
import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store uploaded content in memory (for demo)
uploaded_text = ""

# Set your Groq API key from environment variable
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return PlainTextResponse("FastAPI server is running! Use /upload and /ask endpoints.")

@app.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    global uploaded_text
    if not file:
        return JSONResponse({'error': 'No file uploaded'}, status_code=400)
    try:
        contents = await file.read()
        from io import BytesIO
        pdf_reader = PyPDF2.PdfReader(BytesIO(contents))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        uploaded_text = text
        return {"message": "File uploaded and processed successfully."}
    except Exception as e:
        return JSONResponse({'error': f'Failed to process PDF: {str(e)}'}, status_code=500)

@app.post('/ask')
async def ask_question(body: QuestionRequest):
    global uploaded_text
    question = body.question
    if not uploaded_text:
        return {"answer": "Please upload your study material first."}
    if not question:
        return {"answer": "Please enter a question."}
    prompt = f"""You are a helpful course assistant. Answer the question using ONLY the following material:\n\n{uploaded_text}\n\nQuestion: {question}\nAnswer:"""
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",  # You can change the model if needed
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.2
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        answer = data['choices'][0]['message']['content'].strip()
        return {"answer": answer}
    except Exception as e:
        return {"answer": f'Error communicating with Groq: {str(e)}'}

# To run: uvicorn app:app --reload 