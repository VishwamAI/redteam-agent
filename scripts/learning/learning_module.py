from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class LearningModule:
    def train(self, X_train, y_train, X_test, y_test):
        # Train the model here
        pass

    def evaluate(self, y_test, predictions):
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average="weighted")
        recall = recall_score(y_test, predictions, average="weighted")
        f1 = f1_score(y_test, predictions, average="weighted")
        print(f"Training completed. Model accuracy: "
              f"{accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 Score: {f1:.2f}")

    def predict(self, X):
        # Predict using the trained model
        pass
