from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import os

# ------------------
# Gemini configuration
# ------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------
# FastAPI app
# ------------------
app = FastAPI()

# ------------------
# Request schema
# ------------------
class AnalyzeRequest(BaseModel):
    vision: str
    requirements: str
    student_work: str
    peer_feedback_1: str
    peer_feedback_2: Optional[str] = None


# ------------------
# Health check
# ------------------
@app.get("/")
def root():
    return {"status": "ok"}


# ------------------
# Core analysis endpoint
# ------------------
@app.post("/analyze")
def analyze(data: AnalyzeRequest):

    prompt = f"""
You are an AI-powered peer feedback coach for STEM education.

Project Vision:
{data.vision}

Project Requirements:
{data.requirements}

Student Work:
{data.student_work}

Peer Feedback 1:
{data.peer_feedback_1}

Peer Feedback 2:
{data.peer_feedback_2 if data.peer_feedback_2 else "N/A"}

Tasks:
1. Evaluate the student work for correctness, clarity, and depth.
2. Classify it as: Correct, Partially Faulty, or Completely Wrong.
3. Generate an ideal critique aligned with the project vision.
4. Evaluate peer feedback quality based on:
   - Alignment with vision
   - Constructiveness
   - Specificity
   - Tone
5. Rewrite the peer feedback to be vision-aware and constructive.
6. Provide coaching tips.
7. Perform sentiment, inclusivity, and ethical checks.
8. If multiple feedbacks exist, synthesize them.

Respond ONLY in valid JSON with this structure:
{{
  "work_evaluation": {{
    "classification": "",
    "correctness": "",
    "clarity": "",
    "depth": ""
  }},
  "alignment_score": "High | Medium | Low",
  "feedback_quality_score": "High | Medium | Low",
  "improved_feedback": "",
  "coaching_tips": [],
  "sentiment_flags": [],
  "aggregated_feedback": ""
}}
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "response_mime_type": "application/json"
        }
    )

    return response.text
