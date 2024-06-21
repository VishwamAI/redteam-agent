import logging
from .cmgr_interface import CMGRInterface
from .learning.learning_module import LearningModule
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import os
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_components():
    """
    Initialize the CMGRInterface and TfidfVectorizer.

    Returns:
        tuple: Initialized CMGRInterface and TfidfVectorizer.
    """
    cmgr = CMGRInterface()
    vectorizer = TfidfVectorizer()
    return cmgr, vectorizer

def list_challenges(cmgr):
    """
    List available challenges using the CMGRInterface.

    Args:
        cmgr (CMGRInterface): The CMGRInterface instance.

    Returns:
        list: List of available challenges.
    """
    challenges = cmgr.list_challenges()
    if not challenges:
        logging.info("No challenges available.")
    return challenges

def process_challenge(cmgr, challenge):
    """
    Process a single challenge to extract features and labels.

    Args:
        cmgr (CMGRInterface): The CMGRInterface instance.
        challenge (dict): The challenge details.

    Returns:
        tuple: Extracted text features and labels.
    """
    challenge_id = challenge['id']
    logging.info(f"Processing challenge: {challenge_id}")

    try:
        # Extract details directly from the challenge dictionary
        name = challenge.get('name', '')
        description = challenge.get('description', '')
        hint = challenge.get('hint', '')
        category = challenge.get('category', '')

        text_features = f"{name} {description} {hint} {category}"
        labels = np.array([1])  # Simulated labels

        return text_features, labels

    except KeyError as e:
        logging.error(f"KeyError: Missing key {e} in challenge {challenge_id}")
        return None, None
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing challenge {challenge_id}: {e}")
        return None, None


def download_challenge_file(url, file_path):
    """
    Download the challenge file from the given URL.

    Args:
        url (str): The URL of the challenge file.
        file_path (str): The path to save the downloaded file.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(response.content)
        logging.info(f"Downloaded challenge file from {url}")
    except requests.RequestException as e:
        logging.error(f"Failed to download challenge file from {url}: {e}")

def extract_flag(file_path):
    """
    Extract the flag from the downloaded challenge file.

    Args:
        file_path (str): The path of the downloaded file.

    Returns:
        str: The extracted flag.
    """
    try:
        with open(file_path, 'r') as file:
            flag = file.read().strip()
        logging.info(f"Extracted flag: {flag}")
        return flag
    except Exception as e:
        logging.error(f"Failed to extract flag from {file_path}: {e}")
        return None

def submit_flag(flag):
    """
    Submit the extracted flag to the picoCTF platform.

    Args:
        flag (str): The extracted flag.
    """
    submission_url = "https://play.picoctf.org/api/v1/challenges/submit"
    payload = {
        "flag": flag
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(submission_url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Successfully submitted flag: {flag}")
    except requests.RequestException as e:
        logging.error(f"Failed to submit flag: {e}")

def fit_vectorizer(vectorizer, all_text_features):
    """
    Fit the TfidfVectorizer on all collected text features.

    Args:
        vectorizer (TfidfVectorizer): The TfidfVectorizer instance.
        all_text_features (list): List of all text features.

    Returns:
        np.ndarray: Transformed text features.
    """
    return vectorizer.fit_transform(all_text_features)

def combine_features(text_vectors, challenges):
    """
    Combine text vectors with numerical features.

    Args:
        text_vectors (np.ndarray): Transformed text features.
        challenges (list): List of challenges.

    Returns:
        np.ndarray: Combined features.
    """
    all_features = []
    for i, challenge in enumerate(challenges):
        points = challenge.get('points', 0)
        text_vector = text_vectors[i]
        features = np.hstack((text_vector, np.array([points])))
        all_features.append(features)
    return np.vstack(all_features)

def main():
    cmgr, vectorizer = initialize_components()

    # Load test dataset from JSON file
    import json
    with open('/home/ubuntu/VishwamAI/data/picoctf_challenges_test.json', 'r') as file:
        challenges = json.load(file)

    if not challenges:
        return

    all_text_features = []
    all_labels = []

    for challenge in challenges:
        text_features, labels = process_challenge(cmgr, challenge)
        if text_features and labels is not None:
            all_text_features.append(text_features)
            all_labels.append(labels)

    text_vectors = fit_vectorizer(vectorizer, all_text_features)
    all_features = combine_features(text_vectors, challenges)
    all_labels = np.hstack(all_labels)

    if all_features.shape[0] > 1:
        X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2)
    else:
        X_train, X_test, y_train, y_test = all_features, all_features, all_labels, all_labels

    learning_module = LearningModule()
    learning_module.train(X_train, y_train)

    model_path = "/home/ubuntu/VishwamAI/models/jarvis_model.pkl"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    learning_module.save_model(model_path)

    predictions = learning_module.predict(X_test)
    logging.info(f"Predictions: {predictions}")

    # Example usage of the new functions
    challenge_url = "https://mercury.picoctf.net/static/a5683698ac318b47bd060cb786859f23/flag"
    file_path = "/home/ubuntu/VishwamAI/flag"
    download_challenge_file(challenge_url, file_path)
    flag = extract_flag(file_path)
    if flag:
        submit_flag(flag)

if __name__ == "__main__":
    main()
