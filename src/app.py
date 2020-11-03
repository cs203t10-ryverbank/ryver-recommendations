import flask
from flask import request
import json
import py_eureka_client.eureka_client as eureka_client

eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="ryver-recommendations",
                   instance_port=8084)

try:
    res = eureka_client.do_service("ryver-cms", "/")
    print(res, "is active")
except Exception:
    print("no cms service active")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def index():
    return "ryver-recommendations service"


@app.route("/<int:customer_id>", methods=["GET"])
def get_recommendations(customer_id):
    try:
        auth = request.headers["Authorization"]
        if auth == None or not auth.startswith("Bearer"):
            return "Bearer token required for recommendations service"
        res = eureka_client.do_service("ryver-cms", "/contents", headers=request.headers)
        body = json.loads(res)
        print("cms content:", body)
        return f"Customer {customer_id} asking for recommendations"
    except Exception:
        return "Getting recommendations failed", 500


app.run(host="0.0.0.0", port=8084)
