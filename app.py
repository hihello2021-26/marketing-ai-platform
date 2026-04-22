from flask import Flask, render_template, request
import pandas as pd
import os
import random

app = Flask(__name__)

UPLOAD_FOLDER = "data"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    age = int(request.form["age"])
    income = int(request.form["income"])
    visits = int(request.form["visits"])

    score = age + (income / 1000) + visits

    if score > 80:
        result = "🔥 High Purchase Chance"
    elif score > 50:
        result = "⭐ Medium Purchase Chance"
    else:
        result = "❌ Low Purchase Chance"

    return render_template("index.html", prediction=result)

@app.route("/campaign", methods=["POST"])
def campaign():
    product = request.form["product"]
    audience = request.form["audience"]

    message = f"""
Dear {audience},

Special offer on {product} just for you!
Buy now and get 25% discount.

Limited Time Offer!

Thank you.
"""

    return render_template("index.html", campaign=message)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        rows = len(df)

        return render_template("index.html", uploadmsg=f"✅ File Uploaded Successfully ({rows} rows)")

if __name__ == "__main__":
    app.run(debug=True)
