import pypdf

def merge_profiles(json_list):
    """
    Merges consecutive JSON records into a single profile until a new 'Name' is found.
    When a 'Name' is encountered, it starts a new profile.

    Args:
        json_list (list): A list of dictionaries containing profile details.

    Returns:
        list: A list of merged profiles.
    """
    profiles = []  # List to store processed profiles
    current_profile = {}  # Dictionary to hold the merged profile
    
    for record in json_list:
        if record:
            if "Name" in record and record["Name"]:  # Start a new profile when a Name is found
                if current_profile:  # Save the previous profile
                    profiles.append(current_profile)
                current_profile = {}  # Reset for new profile
            
            # Merge details into the current profile
            current_profile.update({k: v for k, v in record.items() if v})  # Only update non-empty values
        
    # Append the last profile if it exists
    if current_profile:
        profiles.append(current_profile)

    return profiles

def extract_text_from_pdf(pdf_path):
    """Extract text from each page of a PDF file."""
    reader = pypdf.PdfReader(pdf_path)
    return [page.extract_text() or "" for page in reader.pages[:10]]