from flask import request, redirect, url_for, session, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash

from db import get_conn

def register_auth(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            try:
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute(f"SELECT id, password_hash FROM users WHERE username='{username}'")
                        user_id, password_hash = cur.fetchone()

                if check_password_hash(password_hash, password):
                    session["user_id"] = user_id
                    return redirect(url_for("index"))
            except Exception as e:
                flash(str(e))

        return render_template("login.html")
    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            try:
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute(
                            f"INSERT INTO users (username, password_hash) VALUES ('{username}', '{generate_password_hash(password)}')"
                        )

                return redirect(url_for("login"))
            except Exception as e:
                flash(str(e))

        return render_template("register.html")

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return redirect(url_for("login"))