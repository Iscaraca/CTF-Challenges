class GameFullError(Exception):
    """Raise when attempting to join a full game."""

class GameNotFullError(Exception):
    """Raise when attempting to do something that requires a full game."""

class GameNotStartedError(Exception):
    """Raise when attempting to do something that requires a shuffled deck and dealt hands."""

class DeckEmptyError(Exception):
    """Raise when attempting to do something that requires cards in the deck."""

class InvalidMoveError(Exception):
    """Raise when attempting to do something that you can't do."""