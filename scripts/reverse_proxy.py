from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
import requests
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

class ReverseProxy:
    def __init__(self, target_url):
        self.target_url = target_url

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.path == '/api/swagger.json':
            with app.test_request_context():
                response = self.serve_swagger_json()
        else:
            response = self.forward_request(request)
        return response(environ, start_response)

    def forward_request(self, request):
        target_url = self.target_url + request.full_path
        headers = {key: value for key, value in request.headers if key != 'Host'}
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        return self.create_response(response)

    def create_response(self, response):
        headers = [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'),
            ('Access-Control-Allow-Headers', 'Content-Type')
        ]
        headers.extend([(name, value) for name, value in response.raw.headers.items()])
        return Response(response.content, response.status_code, headers)

    def serve_swagger_json(self):
        try:
            response = send_from_directory('../swagger-ui', 'swagger.json')
            headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'),
                ('Access-Control-Allow-Headers', 'Content-Type')
            ]
            response.headers.extend(headers)
            return response
        except Exception as e:
            print(f"Error serving swagger.json: {e}")
            abort(500)

@app.route('/api/swagger.json')
def serve_swagger():
    return reverse_proxy.serve_swagger_json()

if __name__ == '__main__':
    target_url = 'http://localhost:8000'
    reverse_proxy = ReverseProxy(target_url)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    run_simple('localhost', 5000, reverse_proxy)
