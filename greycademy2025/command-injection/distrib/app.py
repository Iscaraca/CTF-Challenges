import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", date=os.popen("date").read())
    if request.method == "POST":
        return render_template("index.html", date=os.popen(
                f'date +"{request.form.get("format", "")}"'
            ).read())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)