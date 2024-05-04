import requests
from requests.exceptions import JSONDecodeError
import time

session = requests.Session()

resp = session.get("http://proxy:1080/join-game")

while True:
    game_start = False
    while not game_start:
        try:
            time.sleep(2)
            game_state = session.get("http://proxy:1080/game-state").json()
            if "game_started" in game_state:
                game_start = game_state["game_started"]
        except JSONDecodeError:
            continue

    winner = ""
    while not winner:
        try:
            time.sleep(2)
            game_state = session.get("http://proxy:1080/game-state").json()
            if "winner" in game_state:
                winner = game_state["winner"]
                continue
            turn_number = game_state["turn_number"]

            if turn_number % 2 == 1:  # Opponent's turn
                time.sleep(3)  # Thinking time

                if turn_number == 1:
                    session.get("http://proxy:1080/stand")
                else:
                    session.get("http://proxy:1080/reveal")
        except JSONDecodeError:
            continue