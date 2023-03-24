import json
import requests
from flask import Flask, request, Response

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)
    target_url = config["target_url"]

@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def handle_request():
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for (key, value) in request.headers if key != "Host"},
        data=request.get_data(),
        params=request.args,
        cookies=request.cookies
    )
    return Response(resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
