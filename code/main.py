import sys
from game_state import GameState
from sound_manager import SoundManager
from game_modes import SingleplayerGame, LocalMultiplayerGame
import Piece
import board


Gm = GameState()
Sm = SoundManager()


def run(selected_board_num):
    SingleplayerGame(Gm, Sm, Piece, board).run(selected_board_num)


def run_multiplayer(selected_board_num):
    LocalMultiplayerGame(Gm, Sm, Piece, board).run(selected_board_num)


if __name__ == "__main__":
    sys.modules.setdefault("main", sys.modules[__name__])
    import Menu

    Menu.main_menu()
