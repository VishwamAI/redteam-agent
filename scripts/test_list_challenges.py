import logging
from picoctf_interaction import PicoCTFInteraction

def test_list_challenges():
    # Initialize PicoCTFInteraction
    picoctf = PicoCTFInteraction()

    # Test with no filters
    challenges = picoctf.list_challenges()
    logging.info(f"Retrieved {len(challenges)} challenges with no filters.")

    # Test with category filter
    category = "Cryptography"
    challenges = picoctf.list_challenges(category=category)
    logging.info(f"Retrieved {len(challenges)} challenges in category '{category}'.")

    # Test with difficulty filter
    difficulty = "Easy"
    challenges = picoctf.list_challenges(difficulty=difficulty)
    logging.info(f"Retrieved {len(challenges)} challenges with difficulty '{difficulty}'.")

    # Test with both category and difficulty filters
    challenges = picoctf.list_challenges(category=category, difficulty=difficulty)
    logging.info(f"Retrieved {len(challenges)} challenges in category '{category}' with difficulty '{difficulty}'.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_list_challenges()
