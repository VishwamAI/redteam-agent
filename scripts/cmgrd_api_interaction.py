# Define the variables before using them in the print statements
challenge_id = "example_challenge_id"
response = type(
    'obj', (object,), {
        'status_code': 404, 'text': 'Not Found'})()  # Mock response object
build_id = "example_build_id"
instance_id = "example_instance_id"

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
