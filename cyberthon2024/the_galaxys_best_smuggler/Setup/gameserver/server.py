from flask import Flask, request, jsonify, make_response
import os, logging
from exceptions import *
import threading
from sabacc import SabaccGame

app = Flask(__name__)
game = SabaccGame()
game_lock = threading.Lock()


gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(logging.DEBUG)



@app.route('/join-game', methods=['GET'])
def join_game():
    request.environ['wsgi.input_terminated'] = True

    global game
    with game_lock:
        try:
            player_id = game.join_game()
        except GameFullError as e:
            return jsonify(error="Game full"), 406
    
    resp = make_response('')
    resp.set_cookie('player_id', player_id)
    return resp, 200

@app.route('/start-game', methods=['GET'])
def start_game():
    request.environ['wsgi.input_terminated'] = True

    global game
    with game_lock:
        try:
            game.lando_shuffle_and_deal()
        except GameNotFullError as e:
            return jsonify(error="Game not full"), 406
        except GameNotStartedError as e:
            return jsonify(error="Game in progress"), 406
        
    return '', 200

@app.route('/game-state', methods=['GET'])
def get_game_state():
    request.environ['wsgi.input_terminated'] = True
    player_id = request.cookies.get('player_id')

    if not player_id:
        return jsonify(error="Player ID not set"), 406
    
    global game
    with game_lock:
        return jsonify(game.get_game_state(player_id)), 200

    

@app.route('/hit', methods=['GET'])
def hit():
    request.environ['wsgi.input_terminated'] = True
    player_id = request.cookies.get('player_id')

    if not player_id:
        return jsonify(error="Player ID not set"), 406
    
    global game
    with game_lock:
        try:
            game.hit(player_id)
        except GameNotFullError as e:
            return jsonify(error="Game not full"), 406
        except GameNotStartedError as e:
            return jsonify(error="Game has not started"), 406
        except DeckEmptyError as e:
            return jsonify(error="Deck is empty"), 406
        except InvalidMoveError as e:
            return jsonify(error="Invalid player ID or wrong turn"), 406
        
    return '', 200

@app.route('/stand', methods=['GET'])
def stand():
    request.environ['wsgi.input_terminated'] = True
    player_id = request.cookies.get('player_id')

    if not player_id:
        return jsonify(error="Player ID not set"), 406
    
    global game
    with game_lock:
        try:
            game.stand(player_id)
        except GameNotFullError as e:
            return jsonify(error="Game not full"), 406
        except GameNotStartedError as e:
            return jsonify(error="Game has not started"), 406
        except DeckEmptyError as e:
            return jsonify(error="Deck is empty"), 406
        except InvalidMoveError as e:
            return jsonify(error="Invalid player ID or wrong turn"), 406
        
    return '', 200

@app.route('/reveal', methods=['GET'])
def reveal():
    request.environ['wsgi.input_terminated'] = True
    player_id = request.cookies.get('player_id')

    if not player_id:
        return jsonify(error="Player ID not set"), 406
    
    results = {}
    global game
    with game_lock:
        try:
            results = game.reveal(player_id)
        except GameNotFullError as e:
            return jsonify(error="Game not full"), 406
        except GameNotStartedError as e:
            return jsonify(error="Game has not started"), 406
        except DeckEmptyError as e:
            return jsonify(error="Deck is empty"), 406
        except InvalidMoveError as e:
            return jsonify(error="Invalid player ID or wrong turn"), 406
        
    return jsonify(results), 200