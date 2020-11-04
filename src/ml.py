import json
import numpy as np
from numpy.core.fromnumeric import sort
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


def load_trained_model():
    df = _get_df(_get_data_obj())
    X_train, y_train = df['content'], df['stock']
    _load_cv(X_train)
    _load_fitted_lr_model(X_train, y_train)


def _get_data_obj():
    with open("data/data.json", "r") as file:
        return json.load(file)


def _get_df(data_obj):
    df = pd.DataFrame()
    for data in data_obj:
        for stock in data["stock"]:
            new_row = {
                "stock": stock, "title": data["title"],
                "summary": data["summary"], "content": data["content"]
            }
            df = df.append(new_row, ignore_index=True)
    return df


# The count vectorizer to fit text data with
cv = None
def _load_cv(X_train):
    global cv
    # Use a count vectorizer to fit text data
    cv = CountVectorizer(ngram_range=(1,3))
    cv.fit(X_train)


# The LogisticRegression model to use
lr = None
def _load_fitted_lr_model(X_train, y_train):
    global lr
    # Use LR to determine the stock based on content.
    # liblinear is good for small datasets
    lr = LogisticRegression(solver="liblinear")
    return lr.fit(cv.transform(X_train), y_train)


def get_stocks_for_article(title, summary, content):
    global cv
    global lr
    if cv is None or lr is None:
        return []
    test = title + summary + content
    X_final = np.array([test])
    X_probs = lr.predict_proba(cv.transform(X_final))
    return _get_stocks_for_probs(X_probs[0])


def _get_stocks_for_probs(probs, max=5):
    stocks = _get_stocks()
    paired_stocks = list(zip(stocks, probs))
    paired_stocks = sorted(paired_stocks, key=lambda x: x[1], reverse=True)
    return [pair[0] for pair in paired_stocks][:max]


def _get_stocks():
    with open("data/stocks.json", "r") as file:
        return json.load(file)


load_trained_model()
