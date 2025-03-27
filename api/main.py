from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analysis import analyze_code
from ml_model import suggest_fixes
from openai_helper import openai_suggestions
import os

app = FastAPI()

# ✅ Enable CORS to allow frontend (index.html) to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to frontend URL if hosted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str
@app.get("/")
async def root():
    return {"message": "Welcome to the AI Code Reviewer API! Use /docs for Swagger UI."}

@app.post("/analyze")
async def analyze(code_input: CodeInput):
    try:
        suggestions = analyze_code(code_input.code)
        ml_fixes = suggest_fixes(code_input.code)
        ai_suggestions = openai_suggestions(code_input.code)

        return {"suggestions": suggestions + ml_fixes + ai_suggestions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

