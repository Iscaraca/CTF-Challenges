import os
import requests
import socket
from flask import Flask, render_template, request, redirect, url_for, session

from auth import register_auth

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]
app.config['SESSION_COOKIE_HTTPONLY'] = False

register_auth(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        api = request.form.get("api", "")
        code = request.form.get("code", "").strip()
        resp = requests.get(f"{api}{code}.json")

        if resp.status_code == 200:
            return render_template("index.html", result=resp.text)

    return render_template("index.html", result="Module not found")

@app.route("/module-request", methods=["GET"])
def module_request():
    code = request.args.get("code")
    name = request.args.get("name")
    description = request.args.get("description")

    try:
        admin_host = os.getenv('ADMIN_HOST', 'admin-bot')
        admin_port = int(os.getenv('ADMIN_PORT', '3001'))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((admin_host, admin_port))
            s.send(request.url.encode())
    except Exception as e:
        print(f"Failed to notify admin: {e}")

    return f"""
    <!DOCTYPE html>
    <html>
        <body>
            <h2>Module request, for admin review</h2>
            <p>{ code }</p>
            <p>{ name }</p>
            <p>{ description }</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)