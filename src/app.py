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
def get_recommendations():
    try:
        auth = request.headers["Authorization"]
        if auth == None or not auth.startswith("Bearer"):
            return "Bearer token required for recommendations service"

        stocks_owned = _get_stocks_owned(request.headers)
        articles = _get_articles(request.headers)

        zipped_article_relevant_stocks = [
            (article, set(get_stocks_for_article(article))) for article in articles
        ]

        recommendations = [
            pair[0] for pair in zipped_article_relevant_stocks
            if not pair[1].isdisjoint(stocks_owned)
        ]

        return json.dumps(recommendations)
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
