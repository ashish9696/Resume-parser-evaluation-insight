from Levenshtein import ratio
from sklearn.metrics import f1_score

def calculate_exact_match_accuracy(extracted_data, ground_truth):
    """Calculate exact match accuracy, including handling nested lists and dictionaries."""
    correct = 0
    total = len(ground_truth)

    for key, true_value in ground_truth.items():
        extracted_value = extracted_data.get(key, None)

        if isinstance(true_value, dict) and isinstance(extracted_value, dict):
            # Recursive call for nested dictionaries
            correct += calculate_exact_match_accuracy(extracted_value, true_value)
        elif isinstance(true_value, list) and isinstance(extracted_value, list):
            # Compare lists item-wise
            correct += sum(1 for i in range(min(len(true_value), len(extracted_value))) 
                           if true_value[i] == extracted_value[i])
        else:
            if extracted_value == true_value:
                correct += 1

    return correct / total if total > 0 else 0

def calculate_f1_score(extracted_data, ground_truth):
    """Calculate F1-score for binary matching of extracted and actual values, handling nested structures."""
    y_true, y_pred = [], []

    for key, true_value in ground_truth.items():
        extracted_value = extracted_data.get(key, None)

        if isinstance(true_value, dict) and isinstance(extracted_value, dict):
            # Recursive F1-score computation for nested dictionaries
            nested_f1 = calculate_f1_score(extracted_value, true_value)
            y_true.append(1)  # Consider nested dicts as single entities
            y_pred.append(1 if nested_f1 > 0.5 else 0)
        elif isinstance(true_value, list) and isinstance(extracted_value, list):
            # Handle lists by checking if elements match
            for t, e in zip(true_value, extracted_value):
                y_true.append(1 if t else 0)
                y_pred.append(1 if e == t else 0)
        else:
            y_true.append(1 if true_value else 0)
            y_pred.append(1 if extracted_value == true_value else 0)

    return f1_score(y_true, y_pred) if y_true else 0

def calculate_text_similarity(extracted_text, ground_truth_text):
    """Compute Levenshtein ratio similarity for text comparison."""
    if isinstance(extracted_text, dict) and isinstance(ground_truth_text, dict):
        # Compute similarity recursively for nested dicts
        return sum(calculate_text_similarity(extracted_text[k], ground_truth_text[k]) 
                   for k in extracted_text if k in ground_truth_text) / len(ground_truth_text)

    if isinstance(extracted_text, list) and isinstance(ground_truth_text, list):
        # Compute similarity for lists
        return sum(calculate_text_similarity(e, t) for e, t in zip(extracted_text, ground_truth_text)) / len(ground_truth_text)

    return ratio(str(extracted_text), str(ground_truth_text))  # Convert to string before computing similarity

def evaluate_extraction(extracted, ground_truth):
    """Evaluate extraction accuracy with exact match, F1-score, and similarity."""
    exact_accuracy = calculate_exact_match_accuracy(extracted, ground_truth)
    f1 = calculate_f1_score(extracted, ground_truth)
    
    # Compute similarity scores for each key
    similarity_scores = {k: calculate_text_similarity(extracted.get(k, ""), v) 
                         for k, v in ground_truth.items()}

    return {
        "Exact Match Accuracy": exact_accuracy,
        "F1-Score": f1,
        "Similarity Scores": similarity_scores
    }
