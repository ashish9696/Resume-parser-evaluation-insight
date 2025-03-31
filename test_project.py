import unittest
import json
from resume_utils.res_util import merge_profiles
from resume_utils.llm_util import get_llm_response
from resume_utils.base_util import convert_response
from resume_parser import parse_resume_from_pdf, evaluate_extraction

class TestResumeParser(unittest.TestCase):
    def setUp(self):
        """Setup test data before each test"""
        self.sample_json = {
            "Name": "John Doe",
            "Email": "johndoe@example.com",
            "Experience": [{"Title": "Software Engineer", "Organization": "Tech Corp", "Duration": "2 Years"}]
        }
        self.ground_truth = {
            "Name": "John Doe",
            "Email": "johndoe@example.com",
            "Experience": [{"Title": "Software Engineer", "Organization": "Tech Corp", "Duration": "2 Years"}]
        }

    def test_extract_with_ollama(self):
        """Test LLM response extraction"""
        text = "John Doe, Software Engineer at Tech Corp"
        response = get_llm_response(text)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_convert_response(self):
        """Test JSON conversion"""
        json_str = '{"Name": "John Doe", "Email": "johndoe@example.com"}'
        converted = convert_response(json_str)
        self.assertIsInstance(converted, dict)
        self.assertEqual(converted["Name"], "John Doe")

    def test_merge_profiles(self):
        """Test merging profiles"""
        json_list = [
            {"Name": "John Doe"},
            {"Email": "johndoe@example.com"},
            {"Experience": [{"Title": "Software Engineer", "Organization": "Tech Corp"}]}]
        merged_profiles = merge_profiles(json_list)
        self.assertEqual(merged_profiles[0]["Name"], "John Doe")
        self.assertEqual(merged_profiles[0]["Email"], "johndoe@example.com")

    def test_evaluate_extraction(self):
        """Test evaluation metrics"""
        evaluation_result = evaluate_extraction(self.sample_json, self.ground_truth)
        print(evaluation_result)
        self.assertIn("Exact Match Accuracy", evaluation_result)
        self.assertIn("F1-Score", evaluation_result)
        self.assertIn("Similarity Scores", evaluation_result)
        self.assertGreaterEqual(evaluation_result["Exact Match Accuracy"], 0)

if __name__ == "__main__":
    unittest.main()