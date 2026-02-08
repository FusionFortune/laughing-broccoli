

#AI Feedback coach
Backend service using Gemini API to:
- Analyze STEM work
- Evaluate peer feedback
- Coach constructive, vision-aware critique
- Perform sentiment & inclusivity checks

## Run locally
```bash
export GEMINI_API_KEY=your_key
pip install -r requirements.txt
uvicorn main:app --reload
