from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="WordPress Staging Mock Environment")

BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML_PATH = BASE_DIR / "templates" / "index.html"


class ContactFormPayload(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(default="", max_length=20)
    message: str = Field(..., min_length=5, max_length=2000)
    gdpr_consent: bool


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=INDEX_HTML_PATH.read_text(encoding="utf-8"))


@app.post("/wp-json/contact/v1/submit")
async def submit_contact_form(payload: ContactFormPayload):
    if not payload.gdpr_consent:
        raise HTTPException(
            status_code=422,
            detail="GDPR consent is required to submit the form."
        )
    return JSONResponse(
        status_code=200,
        content={
            "status": "mail_sent",
            "message": "Thank you for your message. We will get back to you shortly."
        }
    )


@app.get("/wp-content/uploads/")
async def blocked_uploads_listing():
    raise HTTPException(status_code=403, detail="Directory listing is forbidden.")
