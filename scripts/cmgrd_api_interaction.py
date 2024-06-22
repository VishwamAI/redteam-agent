print("Failed to retrieve challenge {} with status code {}: {}".format(
    challenge_id, response.status_code, response.text
))
print("Failed to start instance for build {} with status code {}: {}".format(
    build_id, response.status_code, response.text
))
print("Failed to retrieve instance {} with status code {}: {}".format(
    instance_id, response.status_code, response.text
))
print("Failed to run solver for instance {} with status code {}: {}".format(
    instance_id, response.status_code, response.text
))
