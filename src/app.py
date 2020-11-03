import flask
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

app.run(host="0.0.0.0", port=8084)
