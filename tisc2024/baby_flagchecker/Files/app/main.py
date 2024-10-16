from flask import Flask, render_template, render_template_string, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    password = request.form['password']
    try:
        if len(password) > 32:
            return render_template_string("""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Check Result</title>
            </head>
            <body>
                <h1>Keyphrase too long!</h1>
                <a href="/">Go back</a>
            </body>
        </html>
        """)

        response = requests.post("http://server:5000/check", json={"password": password})
        response_data = response.json()

        return render_template_string("""
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Check Result</title>
                <style>
                    body, html {
                        height: 100%;
                        margin: 0;
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                    }
                    .container {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    a {
                        padding: 10px 20px;
                        text-decoration: none;
                        background-color: #007bff;
                        color: white;
                        border-radius: 5px;
                    }
                    a:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <p>Result for """ + password + """:</p>
                    {% if response_data["output"] %}
                    <h1>Accepted</h1>
                    {% else %}
                    <h1>Invalid</h1>
                    {% endif %}
                    <a href="/">Go back</a>
                </div>
            </body>
        </html>
        """, response_data=response_data)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)