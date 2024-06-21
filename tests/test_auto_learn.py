import unittest
import sys
import os
import numpy as np
from unittest.mock import MagicMock

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auto_learn import initialize_components, list_challenges, process_challenge, fit_vectorizer, combine_features

class TestAutoLearn(unittest.TestCase):
    def setUp(self):
        self.cmgr = MagicMock()
        self.vectorizer = MagicMock()
        self.challenges = [
            {'id': 'challenge1', 'description': 'desc1', 'hint': 'hint1', 'points': 10, 'category': 'cat1'},
            {'id': 'challenge2', 'description': 'desc2', 'hint': 'hint2', 'points': 20, 'category': 'cat2'}
        ]

    def test_initialize_components(self):
        cmgr, vectorizer = initialize_components()
        self.assertIsNotNone(cmgr)
        self.assertIsNotNone(vectorizer)

    def test_list_challenges(self):
        self.cmgr.list_challenges.return_value = self.challenges
        challenges = list_challenges(self.cmgr)
        self.assertEqual(len(challenges), 2)
        self.assertEqual(challenges[0]['id'], 'challenge1')

    def test_process_challenge(self):
        challenge = self.challenges[0]
        self.cmgr.get_challenge.return_value = challenge
        text_features, labels = process_challenge(self.cmgr, challenge)
        self.assertEqual(text_features, 'desc1 hint1 cat1')
        self.assertEqual(labels.tolist(), [1])

    def test_fit_vectorizer(self):
        text_features = ['desc1 hint1 cat1', 'desc2 hint2 cat2']
        self.vectorizer.fit_transform.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])
        transformed_features = fit_vectorizer(self.vectorizer, text_features)
        self.vectorizer.fit_transform.assert_called_once_with(text_features)
        self.assertTrue((transformed_features == np.array([[0.1, 0.2], [0.3, 0.4]])).all())

    def test_combine_features(self):
        text_vectors = np.array([[0.1, 0.2], [0.3, 0.4]])
        combined_features = combine_features(text_vectors, self.challenges)
        self.assertEqual(combined_features.shape, (2, 3))
        self.assertTrue((combined_features == np.array([[0.1, 0.2, 10], [0.3, 0.4, 20]])).all())

if __name__ == "__main__":
    unittest.main()
