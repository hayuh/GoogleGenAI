import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_gemini_response(input):
    model=genai.GenerativeModel('models/gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

input_prompt = """Given a job description and a resume, assign a percentage based on the likelihood that the resume will pass the resume screening
(0 for impossible to pass and 100 for certain to pass),and rationale for the assigned percentage.
Here are the inputs:
Job Description: {jd}
Resume: {text}

Please output the response in the following format: Resume pass percent, rationale.
"""

st.title("Resume Evaluator")
st.text("Resume evaluator")
jd=st.text_area("Paste job description")
uploaded_file=st.file_uploader("Upload your resume", type="pdf", help="Please upload pdf")

submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(input_prompt)
        st.subheader(response)