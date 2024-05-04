def ingest_game_state(game_state):
    if "flag" in game_state:
        return {
            "game_ended": True,
            "player_1_hand": game_state["player_2_hand"],  # You are player 2
            "player_2_hand": game_state["player_1_hand"],
            "deck_size": 20 - len(game_state["player_1_hand"]) - len(game_state["player_2_hand"]),
            "flag": game_state["flag"]
        }
    
    return {
        "game_ended": False,
        "turn_number": game_state["turn_number"],
        "player_1_hand": game_state["player_hand"],
        "player_2_hand": [0] * game_state["opponent_hand_size"],
        "deck_size": 20 - len(game_state["player_hand"]) - game_state["opponent_hand_size"],
    }