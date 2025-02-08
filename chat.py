from groq import Groq
import os

# for extracting the text

import pdfplumber

def extract_resume_text():
    text = ""
    with pdfplumber.open('/home/rhinks/Desktop/hackathon babbyyyy/omkar resume (1).pdf') as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

resume_text = extract_resume_text()
print(resume_text)




# for comparing and analyzing the resume and job description
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"Analyze this resume: {resume_text}. Compare it with this job description: <job_description>. Provide suggestions for improvement.",
        }
    ],
    model="llama-3.3-70b-versatile",
    stream=False,
)

print(chat_completion.choices[0].message.content)