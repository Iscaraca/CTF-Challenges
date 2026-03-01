import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/secret", methods=["GET"])
def secret():
    return jsonify({"secret": os.environ["FLAG"]})

if __name__ == "__main__":
    app.run(debug=True)