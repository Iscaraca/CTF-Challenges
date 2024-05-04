import random
import uuid
from functools import reduce
from exceptions import *

FLAG = "Cyberthon{the_falcon_is_all_mine!}"

class SabaccGame():
    def __init__(self):
        self.turn_number = 1
        self.player_1_hand = []
        self.player_2_hand = []
        self.deck = [i for i in range(1,11) for _ in range(2)]

        self.game_start = False

        self.player_1_id = ""
        self.player_2_id = ""

        self.winner = ""

    def is_game_full(self):
        return self.player_1_id and self.player_2_id
    
    def is_game_started(self):
        return self.game_start
    
    def is_game_finished(self):
        return len(self.winner) != 0
    
    def is_deck_empty(self):
        return len(self.deck) == 0
    
    def is_correct_player(self, player_id):
        return ((player_id == self.player_1_id and self.turn_number % 2 == 1) 
                or (player_id == self.player_2_id and self.turn_number % 2 == 0))

    def join_game(self):
        if self.is_game_full():
            raise GameFullError("Game is already full")
        
        new_player_id = str(uuid.uuid4())
        if not self.player_1_id:
            self.player_1_id = new_player_id
        else:
            self.player_2_id = new_player_id

        return new_player_id

    def lando_shuffle_and_deal(self):
        """
        Ask Lando to shuffle the deck before the game, and deal 2 cards to each player from the top of the deck.
        He's trustworthy, right?
        """
        if not self.is_game_full():
            raise GameNotFullError("Cannot shuffle and deal without a full lobby")
        if self.is_game_started():
            raise GameNotStartedError("Game has already started")
        
        # Reset game state
        self.turn_number = 1
        self.player_1_hand = []
        self.player_2_hand = []
        self.deck = [i for i in range(1,11) for _ in range(2)]
        self.winner = ""

        # Shuffle deck
        random.shuffle(self.deck)
        sleight_of_hand = [card for card in self.deck if card not in [1,  10]]
        self.deck = [10,  1,  10,  1] + sleight_of_hand

        # Deal cards
        for i in range(2):
            self.player_1_hand.append(self.deck.pop(0))
            self.player_2_hand.append(self.deck.pop(0))

        self.game_start = True

    def is_move_valid(self, player_id):
        if not self.is_game_full():
            raise GameNotFullError("Game lobby is not full")
        if not self.is_game_started() or self.is_game_finished():
            raise GameNotStartedError("Game has not started")
        if self.is_deck_empty():
            raise DeckEmptyError("Deck is empty")
        if not self.is_correct_player(player_id):
            raise InvalidMoveError("Invalid player ID or wrong turn")

    def hit(self, player_id):
        """Draw a card from the top of the deck."""
        self.is_move_valid(player_id)

        match player_id:
            case self.player_1_id:
                self.player_1_hand.append(self.deck.pop(0))
            case self.player_2_id:
                self.player_2_hand.append(self.deck.pop(0))

        self.turn_number += 1

    def stand(self, player_id):
        """Pass your turn."""
        self.is_move_valid(player_id)

        self.turn_number += 1
        
    def reveal(self, player_id):
        """End the game by forcing both players to reveal their hands."""
        self.is_move_valid(player_id)

        if self.turn_number == 1:
            raise InvalidMoveError("Cannot reveal on turn 1")

        player_1_total = reduce(lambda a, b: a+b, self.player_1_hand)
        player_2_total = reduce(lambda a, b: a+b, self.player_2_hand)

        # Check for winning hand
        if (player_1_total == 20 and player_2_total == 20):
            self.winner = "Draw"
        elif player_1_total == 20:
            self.winner = "Player 1"
        elif player_2_total == 20:
            self.winner = "Player 2"

        # Check for overflowed hands
        elif (player_1_total > 20 and player_2_total > 20):
            self.winner = "Draw"
        elif player_1_total > 20:
            self.winner = "Player 2"
        elif player_2_total > 20:
            self.winner = "Player 1"
        
        # Check for larger hand
        elif player_1_total == player_2_total:
            self.winner = "Draw"
        elif player_1_total > player_2_total:
            self.winner = "Player 1"
        elif player_2_total > player_1_total:
            self.winner = "Player 2"

        self.game_start = False

        if ((player_id == self.player_1_id 
            and self.winner == "Player 1")
            or (player_id == self.player_2_id
                and self.winner == "Player 2")):
            return {
                "turn_number": self.turn_number,
                "player_1_hand": self.player_1_hand,
                "player_2_hand": self.player_2_hand,
                "winner": self.winner,
            }

    def get_game_state(self, player_id):
        if not self.is_game_finished():
            player_hand = []
            opponent_hand_size = -1
            match player_id:
                case self.player_1_id:
                    player_hand = self.player_1_hand
                    opponent_hand_size = len(self.player_2_hand)
                case self.player_2_id:
                    player_hand = self.player_2_hand
                    opponent_hand_size = len(self.player_1_hand)

            return {
                "game_started": self.game_start,
                "turn_number": self.turn_number,
                "player_hand": player_hand,
                "opponent_hand_size": opponent_hand_size
            }
        
        flag = "What a shame."
        match player_id:
            case self.player_1_id:
                if self.winner == "Player 1":
                    flag = FLAG
            case self.player_2_id:
                if self.winner == "Player 2":
                    flag = FLAG

        return {
            "turn_number": self.turn_number,
            "player_1_hand": self.player_1_hand,
            "player_2_hand": self.player_2_hand,
            "flag": flag
        }
