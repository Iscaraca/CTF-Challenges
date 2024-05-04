from flask import Flask, render_template, request, jsonify, Response
import requests
from game_state import ingest_game_state

app = Flask(__name__)


last_known_state = {}
session = requests.Session()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/proxy/<string:choice>', methods=['GET'])
def proxy(choice):
    global session
    response = session.get(f"http://proxy:1080/{choice}")

    return render_template('index.html')
    
@app.route('/join-game', methods=['GET'])
def join_game():
    global session
    response = session.get(f"http://proxy:1080/join-game")
    response = session.get(f"http://proxy:1080/start-game")

    return render_template('index.html')

@app.route('/poll', methods=['GET'])
def poll():
    global session
    global last_known_state
    response = session.get(f"http://proxy:1080/game-state").json()

    if last_known_state != response:
        last_known_state = ingest_game_state(response)
        return last_known_state
    
    return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)