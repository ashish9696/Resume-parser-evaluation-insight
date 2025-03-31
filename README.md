## Resume Extraction and Evaluation Project

### Overview
This project focuses on extracting structured information from resumes using an LLM-based approach and evaluating the extracted data using various accuracy metrics. It processes PDF resumes, extracts key details, merges profiles, and evaluates extraction performance.

### Features
- **Resume Parsing**: Extracts structured data from resumes using Ollama LLM.
- **Profile Merging**: Combines multiple JSON objects into distinct profiles based on Name detection.
- **Evaluation Metrics**:
  - Exact Match Accuracy
  - F1-Score
  - Text Similarity using Levenshtein Ratio
  - Numerical Comparison with tolerance for small variations
- **Support for Nested JSON**: Recursively processes dictionaries and lists.
- **Automated Testing**: Includes test scripts for validating functions.

### Dependencies
Ensure you have the following installed:
- Python 3.x
- Packages present in requirement.txt

Install dependencies using:
```
pip install -r requirement.txt
```

### Usage

#### Parse resume and Merge Splitted Profiles to unified structure
```
from resume_utils.res_util import merge_profiles

resumes = parse_resume_from_pdf('data/resumes/sample_resume.pdf')
merged_profiles = merge_profiles(resumes)
```

#### Evaluate Extraction Accuracy
```
from evaluation import evaluate_extraction

extracted_data = { ... }  # Extracted JSON
ground_truth = { ... }  # Expected JSON
metrics = evaluate_extraction(extracted_data, ground_truth)
print(metrics)
```

### Testing
Run the test scripts using:
```
pytest
```

### Future Improvements
- Improve parsing accuracy using fine-tuned LLM models
- Add support for additional resume formats
- Enhance numerical data handling

