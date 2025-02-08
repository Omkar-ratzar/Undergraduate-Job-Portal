import logging
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from groq import Groq  # Replace with your actual Groq client import

app = FastAPI()
client = Groq()  # Initialize your Groq client

from fastapi.middleware.cors import CORSMiddleware

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def parse_pdf(file_bytes):
    try:
        with pdfplumber.open(file_bytes) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    """
    Analyze a resume (PDF) and compare it with a job description.
    """
    if file.content_type != "application/pdf":
        logging.error("Uploaded file is not a PDF.")
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")

    try:
        # Parse the PDF file
        resume_text = parse_pdf(file.file)
        if not resume_text:
            logging.error("Failed to extract text from the PDF.")
            raise HTTPException(status_code=400, detail="No readable text found in the PDF.")

        # Log the parsed resume text (or a part of it for debugging)
        logging.debug(f"Resume Text: {resume_text[:500]}")  # Log first 500 characters

        # Call the Groq API for analysis
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this resume: {resume_text}. Compare it with this job description: {job_description}. Provide suggestions for improvement.",
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=False,
        )

        # Log the response from the Groq API for debugging
        logging.debug(f"Groq Response: {response}")

        # Check if response contains choices
        if hasattr(response, 'choices') and len(response.choices) > 0:
            # Access the content directly from the first choice using the correct attribute
            suggestions = response.choices[0].message.content
        else:
            logging.error("No choices found in the Groq response.")
            raise HTTPException(status_code=500, detail="No suggestions returned from the AI model.")

        return {"suggestions": suggestions}

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
