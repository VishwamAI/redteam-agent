import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


class JarvisModel:
    def __init__(self):
        self.model = RandomForestClassifier()

        # Define preprocessing steps for numerical and categorical data
        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler(with_mean=False))
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant',
                                      fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Create a column transformer to apply the preprocessing steps
        # to the appropriate columns
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, [0, 1, 2]),
                ('cat', categorical_transformer, [3])
            ]
        )

    def preprocess_data(self, raw_data, fit_preprocessor=False):
        # Placeholder for data preprocessing logic
        # For now, assume raw_data is a numpy array with features and labels
        features = raw_data[:, :-1]
        labels = raw_data[:, -1]

        # Debug statements to print the shapes and types of the features
        print("Features shape before preprocessing:",
              features.shape)
        print("Features types before preprocessing:",
              [type(x) for x in features[0]])

        # Fit the preprocessor on the training data if specified
        if fit_preprocessor:
            self.preprocessor.fit(features)

        # Transform the features using the preprocessor
        features_preprocessed = self.preprocessor.transform(features)

        # Debug statement to print the shape of the preprocessed features
        print("Features shape after preprocessing:",
              features_preprocessed.shape)
        print("Preprocessed features:",
              features_preprocessed)

        return features_preprocessed, labels

    def train(self, features, labels):
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Training accuracy: {accuracy}")

    def predict(self, raw_features):
        # Preprocess the raw features before making predictions
        features_preprocessed, _ = self.preprocess_data(
            raw_features, fit_preprocessor=False)
        return self.model.predict(features_preprocessed)

    def save_model(self, model_path):
        joblib.dump({'model': self.model, 'preprocessor': self.preprocessor},
                    model_path)
        print(f"Model saved to:\n"
              f"{model_path}")

    def load_model(self, model_path):
        data = joblib.load(model_path)
        self.model = data['model']
        self.preprocessor = data['preprocessor']
        print(f"Model loaded from:\n"
              f"{model_path}")


if __name__ == "__main__":
    # Example usage
    jarvis = JarvisModel()
    raw_data = np.random.rand(100, 5)  # Example data with 5 features
    features, labels = jarvis.preprocess_data(raw_data, fit_preprocessor=True)
    jarvis.train(features, labels)
    predictions = jarvis.predict(raw_data)
    print(f"Predictions:\n"
          f"{predictions}")
    jarvis.save_model("jarvis_model.pkl")
    jarvis.load_model("jarvis_model.pkl")
