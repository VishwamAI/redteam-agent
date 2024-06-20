from cmgr_interface import CMGRInterface
from learning.learning_module import LearningModule
import numpy as np

def main():
    # Initialize the CMGRInterface and LearningModule
    cmgr = CMGRInterface()
    learning_module = LearningModule()

    # List available challenges
    challenges = cmgr.list_challenges()
    if not challenges:
        print("No challenges available.")
        return

    # Process each challenge
    for challenge in challenges:
        challenge_id = challenge['id']
        print(f"Processing challenge: {challenge_id}")

        # Retrieve challenge details
        try:
            challenge_details = cmgr.get_challenge(challenge_id)
            if not challenge_details:
                print(f"Failed to retrieve challenge details for {challenge_id}")
                continue

            # Print the actual challenge details for inspection
            print(f"Challenge details for {challenge_id}: {challenge_details}")

            # Example: Extract raw data from challenge details (this will depend on the actual challenge data format)
            raw_data = np.array(challenge_details['data'])

            # Preprocess the raw data
            features, labels = learning_module.preprocess_data(raw_data)

            # Train the model on the preprocessed data
            learning_module.train(features, labels)

            # Save the trained model
            model_path = f"models/{challenge_id}_model.pkl"
            learning_module.save_model(model_path)

            # Example: Make predictions on new data (this will depend on the actual use case)
            predictions = learning_module.predict(features)
            print(f"Predictions for {challenge_id}: {predictions}")

        except Exception as e:
            print(f"An error occurred while processing challenge {challenge_id}: {e}")

if __name__ == "__main__":
    main()
