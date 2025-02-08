import pdfplumber

def extract_resume_text():
    text = ""
    with pdfplumber.open('/home/rhinks/Desktop/hackathon babbyyyy/omkar resume (1).pdf') as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

resume_text = extract_resume_text()
print(resume_text)




