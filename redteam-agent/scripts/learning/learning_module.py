import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import joblib


class LearningModule:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X, y):
        """
        Train the model using the provided features and labels.
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average='weighted')
        recall = recall_score(y_test, predictions, average='weighted')
        f1 = f1_score(y_test, predictions, average='weighted')
        print(
            f"Training completed. Model accuracy: {accuracy}, "
            f"Precision: {precision}, Recall: {recall}, F1 Score: {f1}"
        )

    def predict(self, X):
        """
        Predict using the trained model.
        """
        return self.model.predict(X)

    def save_model(self, file_path):
        """
        Save the trained model to a file.
        """
        joblib.dump(self.model, file_path)
        print(f"Model saved to {file_path}")

    def load_model(self, file_path):
        """
        Load a trained model from a file.
        """
        self.model = joblib.load(file_path)
        print(f"Model loaded from {file_path}")

    def preprocess_data(self, raw_data):
        """
        Preprocess raw data into features and labels suitable for training.
        """
        # Example preprocessing: Extract features and labels from raw data
        features = raw_data[:, :-1]
        labels = raw_data[:, -1]
        return features, labels

    def incremental_train(self, new_data):
        """
        Incrementally train the model with new data.
        """
        X, y = self.preprocess_data(new_data)
        self.model.fit(X, y)
        print("Incremental training completed.")


if __name__ == "__main__":
    # Example usage
    # Example raw data with 10 features and 1 label
    raw_data = np.random.rand(100, 11)
    # Generate discrete labels (0 or 1)
    raw_data[:, -1] = np.random.randint(0, 2, size=raw_data.shape[0])
    learning_module = LearningModule()
    X, y = learning_module.preprocess_data(raw_data)
    learning_module.train(X, y)
    learning_module.save_model("trained_model.pkl")
    learning_module.load_model("trained_model.pkl")
    predictions = learning_module.predict(X[:5])
    print(f"Predictions for the first 5 samples: {predictions}")

    # Example incremental training
    new_data = np.random.rand(20, 11)  # Example new data
    # Generate discrete labels (0 or 1)
    new_data[:, -1] = np.random.randint(0, 2, size=raw_data.shape[0])
    learning_module.incremental_train(new_data)
