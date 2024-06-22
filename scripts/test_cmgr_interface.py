from .cmgr_interface import CMGRInterface
import pytest


@pytest.fixture
def cmgr():
    base_url = "http://127.0.0.1:4200"
    return CMGRInterface(base_url)


@pytest.fixture
def challenge_id():
    return "cmgr/examples/aptitude-and-privileges"


@pytest.fixture
def build_id():
    return "cmgr/examples/aptitude-and-privileges"


@pytest.fixture
def instance_id():
    return "cmgr/examples/aptitude-and-privileges"


@pytest.fixture
def templating_info():
    return {"flag_format": "FLAG{.*}", "seeds": [12345]}


def test_list_challenges(cmgr):
    print("Testing list_challenges...")
    challenges = cmgr.list_challenges()
    if challenges:
        print("Challenges listed successfully:", challenges)
    else:
        print("Failed to list challenges.")


def test_get_challenge(cmgr, challenge_id):
    print(f"Testing get_challenge with challenge_id={challenge_id}...")
    challenge = cmgr.get_challenge(challenge_id)
    if challenge:
        print("Challenge retrieved successfully:", challenge)
    else:
        print(f"Failed to retrieve challenge {challenge_id}.")


def test_build_challenge(cmgr, challenge_id, templating_info):
    print(f"Testing build_challenge with challenge_id={challenge_id}...")
    build = cmgr.build_challenge(challenge_id, templating_info)
    if build:
        print("Challenge built successfully:", build)
    else:
        print(f"Failed to build challenge {challenge_id}.")


def test_get_build(cmgr, build_id):
    print(f"Testing get_build with build_id={build_id}...")
    build = cmgr.get_build(build_id)
    if build:
        print("Build retrieved successfully:", build)
    else:
        print(f"Failed to retrieve build {build_id}.")


def test_start_instance(cmgr, build_id):
    print(f"Testing start_instance with build_id={build_id}...")
    instance = cmgr.start_instance(build_id)
    if instance:
        print("Instance started successfully:", instance)
    else:
        print(f"Failed to start instance for build {build_id}.")


def test_get_instance(cmgr, instance_id):
    print(f"Testing get_instance with instance_id={instance_id}...")
    instance = cmgr.get_instance(instance_id)
    if instance:
        print("Instance retrieved successfully:", instance)
    else:
        print(f"Failed to retrieve instance {instance_id}.")


def test_run_solver(cmgr, instance_id):
    print(f"Testing run_solver with instance_id={instance_id}...")
    result = cmgr.run_solver(instance_id)
    if result:
        print("Solver ran successfully:", result)
    else:
        print(f"Failed to run solver for instance {instance_id}.")


if __name__ == "__main__":
    base_url = "http://127.0.0.1:4200"
    cmgr_instance = CMGRInterface(base_url)

    test_list_challenges(cmgr_instance)
    test_get_challenge(cmgr_instance, "cmgr/examples/aptitude-and-privileges")  # Valid ID
    test_build_challenge(
        cmgr_instance,
        "cmgr/examples/aptitude-and-privileges",
        {
            "flag_format": "FLAG{.*}",
            "seeds": [12345]
        }
    )  # Valid ID and updated templating info
    # Commenting out build and instance tests for now as they require valid IDs
    # test_get_build(cmgr_instance, "cmgr/examples/aptitude-and-privileges")
    # test_start_instance(cmgr_instance, "cmgr/examples/aptitude-and-privileges")
    # test_get_instance(cmgr_instance, "cmgr/examples/aptitude-and-privileges")
    # test_run_solver(cmgr_instance, "cmgr/examples/aptitude-and-privileges")
