import requests
import logging
import argparse
import numpy as np

class PicoCTFInteraction:
    def __init__(self):
        self.base_url = "https://play.picoctf.org"
        self.session = requests.Session()

    def login(self, username, password):
        login_url = f"{self.base_url}/login"
        payload = {
            "username": username,
            "password": password
        }
        response = self.session.post(login_url, data=payload)
        if response.status_code == 200:
            logging.info("Successfully logged in to picoCTF.")
        else:
            logging.error(f"Failed to log in to picoCTF: {response.status_code} - {response.text}")

    def get_challenge(self, challenge_id):
        challenge_url = f"{self.base_url}/challenges/{challenge_id}"
        response = self.session.get(challenge_url)
        if response.status_code == 200:
            logging.info(f"Successfully retrieved challenge {challenge_id}.")
            return response.json()
        else:
            logging.error(f"Failed to retrieve challenge {challenge_id}: {response.status_code} - {response.text}")
            return None

    def submit_solution(self, challenge_id, solution):
        submit_url = f"{self.base_url}/challenges/{challenge_id}/submit"
        payload = {
            "solution": solution
        }
        response = self.session.post(submit_url, data=payload)
        if response.status_code == 200:
            logging.info(f"Successfully submitted solution for challenge {challenge_id}.")
            return response.json()
        else:
            logging.error(f"Failed to submit solution for challenge {challenge_id}: {response.status_code} - {response.text}")
            return None

    def solve_challenge(self, challenge_id):
        challenge = self.get_challenge(challenge_id)
        if challenge:
            # Placeholder for challenge-solving logic
            # Replace with actual logic to solve the challenge
            solution = self.generate_solution(challenge)
            result = self.submit_solution(challenge_id, solution)
            if result and result.get("status") == "correct":
                logging.info(f"Challenge {challenge_id} solved successfully.")
                # Return a mock NumPy array with a .shape attribute
                return np.array([[1]])
            else:
                logging.error(f"Failed to solve challenge {challenge_id}.")
                return np.array([[]])
        else:
            return np.array([[]])

    def generate_solution(self, challenge):
        """
        Generate a solution for the given challenge.
        This method should be implemented with the actual logic to solve the challenge.
        """
        # Example placeholder logic
        solution = "example_solution"
        return solution

    def list_challenges(self):
        challenges_url = f"{self.base_url}/challenges"
        response = self.session.get(challenges_url)
        if response.status_code == 200:
            logging.info("Successfully retrieved list of challenges.")
            return response.json()
        else:
            logging.error(f"Failed to retrieve list of challenges: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interact with picoCTF platform")
    parser.add_argument("--list-challenges", action="store_true", help="List available challenges")
    parser.add_argument("--login", nargs=2, metavar=("username", "password"), help="Login to picoCTF")
    args = parser.parse_args()

    picoctf = PicoCTFInteraction()

    if args.login:
        username, password = args.login
        picoctf.login(username, password)

    if args.list_challenges:
        challenges = picoctf.list_challenges()
        if challenges:
            for challenge in challenges:
                print(challenge)
