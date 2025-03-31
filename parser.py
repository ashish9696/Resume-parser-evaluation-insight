import re
import json
import pypdf
from collections import defaultdict

class ResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.texts = self.extract_texts()
        self.parsed_resumes = []
    
    def extract_texts(self):
        """Extract text from a multi-resume PDF and separate resumes."""
        with open(self.pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            texts = [page.extract_text() for page in reader.pages if page.extract_text()]
        return self.split_resumes(texts)
    
    def split_resumes(self, texts):
        """Separate different resumes in a mixed PDF based on heuristic rules."""
        separator_keywords = ["Resume", "Curriculum Vitae",]
        resumes = []
        current_resume = []
        
        for page_text in texts:
            if any(keyword in page_text for keyword in separator_keywords) and current_resume:
                resumes.append(" ".join(current_resume))
                current_resume = []
            current_resume.append(page_text)
        
        if current_resume:
            resumes.append(" ".join(current_resume))
        
        return resumes
    
    def extract_email(self, text):
        """Extract email from text."""
        match = re.search(r"[\w\.-]+@[\w\.-]+", text)
        return match.group(0) if match else ""
    
    def extract_phone(self, text):
        """Extract phone number from text."""
        match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        return match.group(0) if match else ""
    
    def extract_name(self, text):
        """Placeholder for name extraction using NLP models."""
        # Future enhancement: Use Named Entity Recognition (NER) from spaCy or transformers
        return ""
    
    def parse(self):
        """Parse each resume separately."""
        for text in self.texts:
            parsed_data = {
                'email': self.extract_email(text),
                'phone': self.extract_phone(text),
                'name': self.extract_name(text)
            }
            self.parsed_resumes.append(parsed_data)
        return self.parsed_resumes

if __name__ == "__main__":
    pdf_path = "2.resumes_compiled.pdf"  # Replace with actual file path
    parser = ResumeParser(pdf_path)
    extracted_data = parser.parse()
    print(json.dumps(extracted_data, indent=4))
