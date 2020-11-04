import flask
from flask import request
import json
import py_eureka_client.eureka_client as eureka_client
from ml import get_stocks_for_article


eureka_client.init(eureka_server="http://localhost:8761/eureka",
                app_name="ryver-recommendations",
                instance_port=8084)


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

        for article in _get_articles(request.headers):
            print(article["title"], article["summary"], article["content"])

        stocks_owned = _get_stocks_owned(request.headers)

        return f"Customer {customer_id} asking for recommendations"
    except Exception as e:
        print(e)
        return "Getting recommendations failed", 500


def _get_articles(headers):
    res = eureka_client.do_service("ryver-cms", "/contents", headers=headers)
    return json.loads(res)


def _get_stocks_owned(headers):
    portfolio = _get_portfolio(headers)
    return { asset["code"] for asset in portfolio["assets"] }


def _get_portfolio(headers):
    res = eureka_client.do_service("ryver-market", "/portfolio", headers=headers)
    return json.loads(res)


app.run(host="0.0.0.0", port=8084)
