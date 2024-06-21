import joblib
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_model(model_path):
    """
    Load the trained model from the specified path.

    Args:
        model_path (str): The path to the saved model file.

    Returns:
        model: The loaded model.
    """
    try:
        model = joblib.load(model_path)
        logging.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logging.error(f"Failed to load model from {model_path}: {e}")
        return None

def validate_model(model, X_test, y_test):
    """
    Validate the model on the test data and log the accuracy.

    Args:
        model: The trained model.
        X_test (np.ndarray): The test features.
        y_test (np.ndarray): The test labels.
    """
    try:
        predictions = model.predict(X_test)
        accuracy = np.mean(predictions == y_test)
        logging.info(f"Model accuracy on test data: {accuracy}")
    except Exception as e:
        logging.error(f"Failed to validate model: {e}")

def main():
    model_path = "/home/ubuntu/VishwamAI/models/jarvis_model.pkl"
    model = load_model(model_path)

    if model is not None:
        # Generate synthetic test data with 290 features for validation
        X_test = np.random.rand(10, 290)  # 10 instances, 290 features each
        y_test = np.random.randint(0, 2, 10)  # 10 binary labels

        validate_model(model, X_test, y_test)

if __name__ == "__main__":
    main()
