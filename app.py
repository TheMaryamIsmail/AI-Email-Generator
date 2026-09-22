import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

from logic import generate_email_content

load_dotenv()

app = FastAPI(title="AI Email Generator", version="1.0.0")

# Setup templates directory for HTML rendering
templates = Jinja2Templates(directory="templates")

class EmailRequest(BaseModel):
    recipient: str
    tone: str
    purpose: str
    key_points: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Renders the single-file HTML frontend."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.api_route("/generate-email", methods=["POST", "GET"])
async def api_generate_email(payload: EmailRequest = None, recipient: str = None, tone: str = None, purpose: str = None, key_points: str = None):
    """API endpoint to trigger email generation via Gemini."""
    # Support both JSON body payloads and fallback parameters if needed
    if payload:
        rec = payload.recipient
        t = payload.tone
        p = payload.purpose
        kp = payload.key_points
    else:
        rec, t, p, kp = recipient, tone, purpose, key_points

    if not all([rec, t, p, kp]):
        raise HTTPException(status_code=400, detail="All email generation fields are required.")

    try:
        email_output = generate_email_content(
            recipient=rec,
            tone=t,
            purpose=p,
            key_points=kp
        )
        return {"success": True, "email": email_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)