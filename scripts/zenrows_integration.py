import requests

# Define the ZenRows API endpoint and API key
ZENROWS_API_ENDPOINT = "https://api.zenrows.com/v1/get"
ZENROWS_API_KEY = "YOUR_ZENROWS_API_KEY"

# Define the target URL (picoCTF practice page)
TARGET_URL = "https://play.picoctf.org/practice"

# Define the parameters for the ZenRows API request
params = {
    "url": TARGET_URL,
    "apikey": ZENROWS_API_KEY,
    "js_render": "true",
    "antibot": "true",
    "premium_proxy": "true",
}

# Send a GET request to the ZenRows API
response = requests.get(ZENROWS_API_ENDPOINT, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Print the HTML content of the target URL
    print(response.text)
else:
    # Print the error message
    print(f"Error: {response.status_code} - {response.text}")
