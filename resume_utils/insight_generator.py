from resume_utils.llm_util import get_llm_response
import json
from resume_utils.base_util import convert_response

def generate_candidate_insights(resume_json):
    """
    Generate actionable insights from a candidate's resume data using Ollama LLM.
    """

    prompt = f"""Analyze the following candidate resume and extract meaningful insights:
    
    Resume Data:
    {json.dumps(resume_json, indent=2)}
    
    **RULES**
    1. Consider the person as fresher if there are no details in experience section.
    2. Address change does not mean, it will be a job switch.
    
    Provide insights on:
    1. **Skills & Gaps:** Identify top technical and soft skills. Highlight missing skills relevant to a given job role.
    2. **Career Growth:** Analyze past roles for promotions, job-switching trends, and stability.
    3. **Cultural Fit:** Identify personality traits based on achievements, extra-curricular activities, and self-description.
    4. **Performance Forecast:** Predict the candidate’s impact in future roles based on measurable past contributions.
    5. **Active vs. Passive Job Seeker:** Determine if the candidate is actively looking for a job or passively open.
    6. **Diversity & Global Experience:** Check international work exposure and diversity metrics.

    Output structured insights in JSON format with keys: "Skills & Gaps", "Career Growth", "Cultural Fit", "Performance Forecast", "Job Seeker Status", "Diversity & Experience".
    """

    insights = get_llm_response(prompt)
    
    try:
        insights_json = convert_response(insights)
    except json.JSONDecodeError:
        insights_json = {"error": "Failed to parse LLM response"}

    return insights_json
