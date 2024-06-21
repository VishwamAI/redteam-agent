import logging
from .picoctf_api import PicoCTFAPI


def test_picoctf_api():
    # Initialize PicoCTFAPI
    base_url = "https://play.picoctf.org"
    username = "kasinadhsarma"
    password = "1kl12_2>"
    picoctf_api = PicoCTFAPI(base_url, username, password)

    # Initialize variables
    build = None
    instance = None

    # Test login
    picoctf_api.login()

    # Test list challenges
    challenges = picoctf_api.list_challenges()
    if challenges:
        logging.info(f"Retrieved {len(challenges)} challenges.")
    else:
        logging.error("Failed to retrieve challenges.")

    # Test get challenge
    if challenges:
        challenge_id = challenges[0]["id"]
        challenge = picoctf_api.get_challenge(challenge_id)
        if challenge:
            logging.info(f"Retrieved challenge {challenge_id}.")
        else:
            logging.error(f"Failed to retrieve challenge {challenge_id}.")

    # Test build challenge
    if challenges:
        challenge_id = challenges[0]["id"]
        build = picoctf_api.build_challenge(challenge_id)
        if build:
            logging.info(f"Built challenge {challenge_id}.")
        else:
            logging.error(f"Failed to build challenge {challenge_id}.")

    # Test get build
    if build:
        build_id = build["id"]
        build_metadata = picoctf_api.get_build(build_id)
        if build_metadata:
            logging.info(f"Retrieved build {build_id}.")
        else:
            logging.error(f"Failed to retrieve build {build_id}.")

    # Test start instance
    if build:
        build_id = build["id"]
        instance = picoctf_api.start_instance(build_id)
        if instance:
            logging.info(f"Started instance for build {build_id}.")
        else:
            logging.error(f"Failed to start instance for build {build_id}.")

    # Test get instance
    if instance:
        instance_id = instance["id"]
        instance_metadata = picoctf_api.get_instance(instance_id)
        if instance_metadata:
            logging.info(f"Retrieved instance {instance_id}.")
        else:
            logging.error(f"Failed to retrieve instance {instance_id}.")

    # Test run solver
    if instance:
        instance_id = instance["id"]
        solver_result = picoctf_api.run_solver(instance_id)
        if solver_result:
            logging.info(f"Ran solver for instance {instance_id}.")
        else:
            logging.error(f"Failed to run solver for instance {instance_id}.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_picoctf_api()
