from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route('/')
def serve_index():
    return send_from_directory('../swagger-ui', 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../swagger-ui', path)


@app.route('/challenges')
def list_challenges():
    # Placeholder response for the /challenges endpoint
    challenges = [
        {
            "id": 1,
            "name": "Challenge 1",
            "description": "Description of Challenge 1"
        },
        {
            "id": 2,
            "name": "Challenge 2",
            "description": "Description of Challenge 2"
        },
        {
            "id": 3,
            "name": "Challenge 3",
            "description": "Description of Challenge 3"
        }
    ]
    return jsonify(challenges)


if __name__ == '__main__':
    app.run(port=8000)
