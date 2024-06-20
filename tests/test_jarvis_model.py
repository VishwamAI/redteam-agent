import unittest
import numpy as np
import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.jarvis_model import JarvisModel

class TestJarvisModel(unittest.TestCase):

    def setUp(self):
        self.jarvis = JarvisModel()

    def test_preprocess_data(self):
        # Create a test dataset with numerical and categorical features, including missing values
        raw_data = np.array([
            [1.0, 'A', 3.0],
            [2.0, 'B', np.nan],
            [np.nan, 'A', 5.0],
            [4.0, 'C', 6.0]
        ], dtype=object)
        features, labels = self.jarvis.preprocess_data(raw_data)

        # Check if the preprocessed features have the expected shape and type
        self.assertEqual(features.shape, (4, 7))  # Updated expected shape based on OneHotEncoder output
        self.assertTrue(np.issubdtype(features.dtype, np.number))

    def test_train(self):
        # Create a test dataset with numerical and categorical features, including missing values
        raw_data = np.array([
            [1.0, 'A', 3.0, 0],
            [2.0, 'B', np.nan, 1],
            [np.nan, 'A', 5.0, 0],
            [4.0, 'C', 6.0, 1]
        ], dtype=object)
        features, labels = self.jarvis.preprocess_data(raw_data)
        labels = labels.astype(int)  # Ensure labels are of integer type for classification
        self.jarvis.train(features, labels)

        # Check if the model has been trained
        self.assertIsNotNone(self.jarvis.model)

    def test_predict(self):
        # Create a test dataset with numerical and categorical features, including missing values
        raw_data = np.array([
            [1.0, 'A', 3.0, 0],
            [2.0, 'B', np.nan, 1],
            [np.nan, 'A', 5.0, 0],
            [4.0, 'C', 6.0, 1]
        ], dtype=object)
        features, labels = self.jarvis.preprocess_data(raw_data)
        labels = labels.astype(int)  # Ensure labels are of integer type for classification
        self.jarvis.train(features, labels)

        # Preprocess the features for prediction
        features_preprocessed = self.jarvis.preprocess_data(raw_data)[0]

        # Make predictions on the preprocessed features
        predictions = self.jarvis.predict(features_preprocessed)

        # Check if the predictions have the expected shape and type
        self.assertEqual(predictions.shape, (4,))
        self.assertTrue(np.issubdtype(predictions.dtype, np.number))

if __name__ == '__main__':
    unittest.main()
