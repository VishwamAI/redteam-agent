import requests

class CMGRAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def list_challenges(self, tags=None):
        challenges_url = f"{self.base_url}/challenges"
        params = {'tags': tags} if tags else {}
        response = self.session.get(challenges_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to list challenges with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

    def get_challenge(self, challenge_id):
        challenge_url = f"{self.base_url}/challenges/{challenge_id}"
        response = self.session.get(challenge_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to retrieve challenge {challenge_id} with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

    def build_challenge(self, challenge_id, build_data):
        build_url = f"{self.base_url}/challenges/{challenge_id}"
        response = self.session.post(build_url, json=build_data)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to build challenge {challenge_id} with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

    def get_build(self, build_id):
        build_url = f"{self.base_url}/builds/{build_id}"
        response = self.session.get(build_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to retrieve build {build_id} with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

    def start_instance(self, build_id):
        instance_url = f"{self.base_url}/builds/{build_id}"
        response = self.session.post(instance_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to start instance for build {build_id} with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

    def get_instance(self, instance_id):
        instance_url = f"{self.base_url}/instances/{instance_id}"
        response = self.session.get(instance_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to retrieve instance {instance_id} with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

    def run_solver(self, instance_id):
        solver_url = f"{self.base_url}/instances/{instance_id}"
        response = self.session.post(solver_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to run solver for instance {instance_id} with status code "
                f"{response.status_code}: {response.text}"
            )
            return None

if __name__ == "__main__":
    base_url = "http://localhost:4200/api"
    api = CMGRAPI(base_url)

    # Test list_challenges method
    challenges = api.list_challenges()
    print("Challenges:", challenges)

    # Test get_challenge method
    if challenges and len(challenges) > 0:
        challenge_id = challenges[0].get('id')
        if challenge_id:
            challenge = api.get_challenge(challenge_id)
            print("Challenge:", challenge)

    # Test build_challenge method
    if challenges and len(challenges) > 0:
        challenge_id = challenges[0].get('id')
        if challenge_id:
            build_data = {"param1": "value1", "param2": "value2"}
            build = api.build_challenge(challenge_id, build_data)
            print("Build:", build)

    # Test get_build method
    if build and isinstance(build, dict) and 'id' in build:
        build_id = build['id']
        build_info = api.get_build(build_id)
        print("Build Info:", build_info)

    # Test start_instance method
    if build and isinstance(build, dict) and 'id' in build:
        build_id = build['id']
        instance = api.start_instance(build_id)
        print("Instance:", instance)

    # Test get_instance method
    if instance and isinstance(instance, dict) and 'id' in instance:
        instance_id = instance['id']
        instance_info = api.get_instance(instance_id)
        print("Instance Info:", instance_info)

    # Test run_solver method
    if instance and isinstance(instance, dict) and 'id' in instance:
        instance_id = instance['id']
        solver_result = api.run_solver(instance_id)
        print("Solver Result:", solver_result)
