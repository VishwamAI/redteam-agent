import logging
from .picoctf_interaction import PicoCTFInteraction

def test_list_challenges():
    # Initialize PicoCTFInteraction
    picoctf = PicoCTFInteraction()

    # Login to picoCTF
    username = "kasinadhsarma"
    password = "1kl12_2>"
    picoctf.login(username, password)

    # Test with no filters
    challenges = picoctf.list_challenges()
    if challenges:
        logging.info(f"Retrieved {len(challenges)} challenges with no filters.")
    else:
        logging.error("Failed to retrieve challenges with no filters.")

    # Test with category filter
    category = "Cryptography"
    challenges = picoctf.list_challenges(category=category)
    if challenges:
        logging.info(f"Retrieved {len(challenges)} challenges in category '{category}'.")
    else:
        logging.error(f"Failed to retrieve challenges in category '{category}'.")

    # Test with difficulty filter
    difficulty = "Easy"
    challenges = picoctf.list_challenges(difficulty=difficulty)
    if challenges:
        logging.info(f"Retrieved {len(challenges)} challenges with difficulty '{difficulty}'.")
    else:
        logging.error(f"Failed to retrieve challenges with difficulty '{difficulty}'.")

    # Test with both category and difficulty filters
    challenges = picoctf.list_challenges(category=category, difficulty=difficulty)
    if challenges:
        logging.info(f"Retrieved {len(challenges)} challenges in category '{category}' with difficulty '{difficulty}'.")
    else:
        logging.error(f"Failed to retrieve challenges in category '{category}' with difficulty '{difficulty}'.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_list_challenges()
