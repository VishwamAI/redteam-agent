import requests


def get_challenge(challenge_id):
    response = requests.get(
        f"https://example.com/api/challenges/{challenge_id}")
    if response.status_code != 200:
        print(f"Failed to retrieve challenge {challenge_id} with status code "
              f"{response.status_code}: {response.text}")
        return None
    return response.json()


def start_instance(build_id):
    response = requests.post(
        f"https://example.com/api/builds/{build_id}/start")
    if response.status_code != 200:
        print(f"Failed to start instance for build {build_id} with status code "
              f"{response.status_code}: {response.text}")
        return None
    return response.json()


def get_instance(instance_id):
    response = requests.get(
        f"https://example.com/api/instances/{instance_id}")
    if response.status_code != 200:
        print(f"Failed to retrieve instance {instance_id} with status code "
              f"{response.status_code}: {response.text}")
        return None
    return response.json()


def run_solver(instance_id):
    response = requests.post(
        f"https://example.com/api/instances/{instance_id}/solve")
    if response.status_code != 200:
        print(f"Failed to run solver for instance {instance_id} with status code "
              f"{response.status_code}: {response.text}")
        return None
    return response.json()
