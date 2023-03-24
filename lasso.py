import json
import requests
from flask import Flask, request, Response

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)
    endpoints = config["endpoints"]

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def handle_request(path):
    target_url = endpoints.get("/" + path.split("/", 1)[0])
    if not target_url:
        return Response("Not found", 404)

    resp = requests.request(
        method=request.method,
        url=target_url + path,
        headers={key: value for (key, value) in request.headers if key != "Host"},
        data=request.get_data(),
        params=request.args,
        cookies=request.cookies
    )
    return Response(resp.content, resp.status_code, resp.headers.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
