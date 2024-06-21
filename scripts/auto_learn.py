import logging
from .cmgr_interface import CMGRInterface
from .learning.learning_module import LearningModule
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_components():
    """
    Initialize the CMGRInterface, LearningModule, and TfidfVectorizer.

    Returns:
        tuple: Initialized CMGRInterface, LearningModule, and TfidfVectorizer.
    """
    cmgr = CMGRInterface()
    learning_module = LearningModule()
    vectorizer = TfidfVectorizer()
    return cmgr, learning_module, vectorizer

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
        challenge_details = cmgr.get_challenge(challenge_id)
        if not challenge_details:
            logging.warning(f"Failed to retrieve challenge details for {challenge_id}")
            return None, None

        logging.info(f"Challenge details for {challenge_id}: {challenge_details}")

        description = challenge_details.get('description', '')
        hints = ' '.join(challenge_details.get('hints', []))
        points = challenge_details.get('points', 0)
        category = challenge_details.get('category', '')

        text_features = f"{description} {hints} {category}"
        labels = np.array([1])  # Replace with actual labels if available

        return text_features, labels

    except KeyError as e:
        logging.error(f"KeyError: Missing key {e} in challenge {challenge_id}")
        return None, None
    except ConnectionError as e:
        logging.error(f"ConnectionError: Failed to connect to CMGR server for challenge {challenge_id}: {e}")
        return None, None
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing challenge {challenge_id}: {e}")
        return None, None

def fit_vectorizer(vectorizer, all_text_features):
    """
    Fit the TfidfVectorizer on all collected text features.

    Args:
        vectorizer (TfidfVectorizer): The TfidfVectorizer instance.
        all_text_features (list): List of all text features.

    Returns:
        np.ndarray: Transformed text features.
    """
    return vectorizer.fit_transform(all_text_features).toarray()

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
    cmgr, learning_module, vectorizer = initialize_components()
    challenges = list_challenges(cmgr)
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

    learning_module.train(X_train, y_train)

    model_path = "/home/ubuntu/VishwamAI/models/jarvis_model.pkl"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    learning_module.save_model(model_path)

    predictions = learning_module.predict(X_test)
    logging.info(f"Predictions: {predictions}")

if __name__ == "__main__":
    main()
