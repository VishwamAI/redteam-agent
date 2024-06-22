import requests

class CMGRInterface:
    def __init__(self, base_url="http://127.0.0.1:4200"):
        self.base_url = base_url
        self.session = requests.Session()

    def list_challenges(self, tags=None):
        challenges_url = f"{self.base_url}/challenges"
        params = {'tags': tags} if tags else {}
        response = self.session.get(challenges_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to list challenges with status code "
                  f"{response.status_code}: {response.text}")
            return None

    def get_challenge(self, challenge_id):
        challenge_url = f"{self.base_url}/challenges/{challenge_id}"
        response = self.session.get(challenge_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve challenge {challenge_id} with status code "
                  f"{response.status_code}: {response.text}")
            return None

    def build_challenge(self, challenge_id, templating_info):
        build_url = f"{self.base_url}/challenges/{challenge_id}"
        response = self.session.post(build_url, json=templating_info)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to build challenge {challenge_id} with status code "
                  f"{response.status_code}: {response.text}")
            return None

    def get_build(self, build_id):
        build_url = f"{self.base_url}/builds/{build_id}"
        response = self.session.get(build_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve build {build_id} with status code "
                  f"{response.status_code}: {response.text}")
            return None

    def start_instance(self, build_id):
        instance_url = f"{self.base_url}/builds/{build_id}"
        response = self.session.post(instance_url)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Failed to start instance for build {build_id} with status code "
                  f"{response.status_code}: {response.text}")
            return None

    def get_instance(self, instance_id):
        instance_url = f"{self.base_url}/instances/{instance_id}"
        response = self.session.get(instance_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve instance {instance_id} with status code "
                  f"{response.status_code}: {response.text}")
            return None

    def run_solver(self, instance_id):
        solver_url = f"{self.base_url}/instances/{instance_id}"
        response = self.session.post(solver_url)
        if response.status_code == 204:
            return {"message": "Solver ran successfully"}
        else:
            print(f"Failed to run solver for instance {instance_id} with status code "
                  f"{response.status_code}: {response.text}")
            return None
