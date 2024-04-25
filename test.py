import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
import re

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]

# Load custom CSS
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Define function to generate content from generative AI model
def generate_response_from_gemini(input_text):
    llm = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    output = llm.generate_content(input_text)
    return output.text

# Function to extract text from a PDF file
def extract_text_from_pdf_file(uploaded_file):
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content.lower()

# Function to extract text from a DOCX file
def extract_text_from_docx_file(uploaded_file):
    return docx2txt.process(uploaded_file).lower()

# Tokenize text
def tokenize_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return words

# Calculate missing keywords
def get_missing_keywords(job_description, resume_text):
    job_words = set(tokenize_text(job_description))
    resume_words = set(tokenize_text(resume_text))
    missing_keywords = job_words - resume_words
    return sorted(list(missing_keywords))

# Prompt template for generating AI response
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst,
with profound knowledge in technology, software engineering, data science, 
and big data engineering, your role involves evaluating resumes against job descriptions.
Recognizing the competitive job market, provide top-notch assistance for resume improvement.
Your goal is to analyze the resume against the given job description, 
assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
resume:{text}
description:{job_description}
I want the response in one single string having the structure
"Job Description Match":"%", "Missing Keywords":""
"""

# Initialize Streamlit app
st.title("Get Your Resume Score 🚀")

# Text area for job description input
job_description = st.text_area("Paste the Job Description", height=300).lower()

# File uploader for resumes, allowing one file at a time
uploaded_files = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], accept_multiple_files=True)

# Submit button
submit_button = st.button("Submit")

# Initialize resume text variable
resume_text = ""

# If there are uploaded files and submit button is pressed
if uploaded_files and submit_button:
    # Ensure that only one file is uploaded
    if len(uploaded_files) > 1:
        st.error("Please upload only one file at a time.")
    elif not job_description.strip():
        st.error("Please provide the Job Description ⚠️")
    else:
        # Get the first uploaded file
        uploaded_file = uploaded_files[0]
        
        # Extract text from the uploaded file
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)
        
        # Generate response from generative AI
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))
        
        # Initialize missing_keywords variable
        missing_keywords = ""
        
        # Extract Job Description Match percentage from the response
        match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]
        
        # Determine the match percentage and missing keywords
        if match_percentage_str == 'N/A':
            st.error("Sorry, your skills do not match the requirements 😣")
            
            # Get missing keywords from the job description and resume
            missing_keywords = get_missing_keywords(job_description, resume_text)
            
            # Display missing keywords as a list
            st.subheader("Missing Keywords:")
            st.write(", ".join(missing_keywords))
            
            # Provide suggestions for improving the resume
            st.subheader("How to Improve Your Resume:")
            st.write("1. Incorporate the missing keywords from the job description into your resume.")
            st.write("2. Tailor your resume to highlight relevant skills, experience, and accomplishments.")
            st.write("3. Ensure your resume is clear, concise, and well-organized.")
            st.write("4. Review and proofread your resume to eliminate any errors.")
        else:
            # Remove percentage symbol and convert to float
            match_percentage = float(match_percentage_str.rstrip('%'))

            # Display ATS Evaluation Result
            st.subheader("ATS Evaluation Result:")
            st.write("```json")
            st.write(response_text)
            st.write("```")
            
            # Create a progress bar to represent the match percentage
            st.write(f"Your Resume Match: {match_percentage_str}")
            st.progress(match_percentage / 100)
            
            # Determine whether the resume match is good or poor
            if match_percentage >= 70:
                st.success(f"😊 - This resume matches the job description!")
            else:
                st.error(f"😭 - This resume does not match the job description.")
                
                # Provide suggestions for improving the resume
                st.subheader("How to Improve Your Resume:")
                st.write("1. Incorporate the missing keywords from the job description into your resume.")
                st.write("2. Tailor your resume to better highlight your skills and experience relevant to the job.")
