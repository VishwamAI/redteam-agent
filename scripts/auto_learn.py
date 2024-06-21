import logging
from cmgr_interface import CMGRInterface
from learning.learning_module import LearningModule
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize the CMGRInterface and LearningModule
    cmgr = CMGRInterface()
    learning_module = LearningModule()
    vectorizer = TfidfVectorizer()

    # List available challenges
    challenges = cmgr.list_challenges()
    if not challenges:
        logging.info("No challenges available.")
        return

    # Collect all text features and labels for vectorizer fitting and training
    all_text_features = []
    all_features = []
    all_labels = []

    # Process each challenge
    for challenge in challenges:
        challenge_id = challenge['id']
        logging.info(f"Processing challenge: {challenge_id}")

        # Retrieve challenge details
        try:
            challenge_details = cmgr.get_challenge(challenge_id)
            if not challenge_details:
                logging.warning(f"Failed to retrieve challenge details for {challenge_id}")
                continue

            # Log the actual challenge details for inspection
            logging.info(f"Challenge details for {challenge_id}: {challenge_details}")

            # Extract features from challenge details
            description = challenge_details.get('description', '')
            hints = ' '.join(challenge_details.get('hints', []))
            points = challenge_details.get('points', 0)
            category = challenge_details.get('category', '')

            # Combine textual features
            text_features = f"{description} {hints} {category}"
            all_text_features.append(text_features)

            # Generate dummy labels (for demonstration purposes)
            labels = np.array([1])  # Replace with actual labels if available

            # Accumulate labels for all challenges
            all_labels.append(labels)

        except Exception as e:
            logging.error(f"An error occurred while processing challenge {challenge_id}: {e}")

    # Fit the vectorizer on all collected text features
    text_vectors = vectorizer.fit_transform(all_text_features).toarray()

    # Combine text vectors with numerical features
    for i, challenge in enumerate(challenges):
        points = challenge.get('points', 0)
        text_vector = text_vectors[i]
        features = np.hstack((text_vector, np.array([points])))
        all_features.append(features)

    # Convert accumulated features and labels to numpy arrays
    all_features = np.vstack(all_features)
    all_labels = np.hstack(all_labels)

    # Adjust train-test split to handle small datasets
    if all_features.shape[0] > 1:
        X_train, X_test, y_train, y_test = train_test_split(all_features, all_labels, test_size=0.2)
    else:
        X_train, X_test, y_train, y_test = all_features, all_features, all_labels, all_labels

    # Train the model on the preprocessed data
    learning_module.train(X_train, y_train)

    # Save the trained model
    model_path = "/home/ubuntu/VishwamAI/models/jarvis_model.pkl"
    learning_module.save_model(model_path)

    # Make predictions on new data
    predictions = learning_module.predict(X_test)
    logging.info(f"Predictions: {predictions}")

if __name__ == "__main__":
    main()
