#!/usr/bin/env python
# coding: utf-8

import re
import json
from resume_utils.llm_util import get_llm_response
from resume_utils.base_util import convert_response
from resume_utils.res_util import extract_text_from_pdf, merge_profiles
from resume_utils.insight_generator import generate_candidate_insights
from resume_utils.extract_accuracy import evaluate_extraction

def extract_with_ollama(text):
    """Use an Ollama model to extract structured information from resume text."""
    prompt = f"""Extract the following details from the given resume text:
    - Name
    - Gender
    - Registration Number
    - Date of Birth
    - Email
    - Phone Number
    - Mobile Number
    - CGPA
    - Present Address
    - Permanent Address
    - Education Details (Level, Institution, Board/University, Year, Percentage)
    - Semester Details (Semester, Year, SGPA, CGPA)
    - Extra-Curricular Activities
    - Co-Curricular Activities
    - About Myself
    - Experience (Title, Organization, Duration, Description)
    - References (Name, Designation, Organization, Email)
    
    Text:
    {text}
    
    Provide the output in JSON format with keys matching the above categories. 
    Please skip keys which are not available.
    """
    return get_llm_response(prompt)

def parse_resume_from_pdf(pdf_path):
    """Extract resume details from each page of a PDF file using Ollama model and parse with Pydantic."""
    pages_text = extract_text_from_pdf(pdf_path)
    parsed_resumes = []
    
    for text in pages_text:
        if text.strip():  # Process only non-empty pages
            llm_response = extract_with_ollama(text)
            parsed_data = convert_response(str(llm_response))
            parsed_resumes.append(parsed_data)
    
    return parsed_resumes

if __name__ == "__main__":
    insight_data=[]
    ground_truth = []
    res = parse_resume_from_pdf("./data/resumes/2.resumes_compiled.pdf")  # Extract resume data
    list_resume = merge_profiles(res)  # Merge extracted profiles
    print(json.dumps(list_resume, indent=4))  # Print formatted output
    for resume in list_resume:
        insight_data.append(generate_candidate_insights(resume))
    print(insight_data)
    #accuracy_metrics = evaluate_extraction(extracted_data, ground_truth)
    #print(accuracy_metrics)

