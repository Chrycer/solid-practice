import argparse

from gridgame.model import GridGameModel
from gridgame.tictactoe import TicTacToeWinConditionChecker, TicTacToeSymbolManager
from gridgame.view import View
from gridgame.controller import Controller
from gridgame.project_types import Field

def str_list(line: str) -> list[str]:
    return line.split(',')

def setup_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--size', type=int, default=3)
    parser.add_argument('-p', '--player_count', type=int, default=2)
    parser.add_argument(
        '--variant',
        choices=["tictactoe", "notakto", "wild", "pick15"],
        required=True,
    )
    parser.add_argument('-s', '--symbols', type=str_list, default=[])

    return parser

def make_model(args: argparse.Namespace):
    match args.variant:
        case "tictactoe":
            field = Field(args.size)
            player_symbols = {i + 1: symbol for i, symbol in enumerate(args.symbols)}
            symbols_player = {symbol: i + 1 for i, symbol in enumerate(args.symbols)}
            win_condition_checker = TicTacToeWinConditionChecker(field, symbols_player)
            symbol_manager = TicTacToeSymbolManager(player_symbols)

            return GridGameModel(
                grid_size=args.size,
                player_count=args.player_count,
                player_symbols=args.symbols,
                win_condition_checker=win_condition_checker,
                symbol_manager=symbol_manager
            )

        case "wild":
            raise NotImplementedError('wild variant is not yet implemented')

        case "notakto":
            raise NotImplementedError('notakto variant is not yet implemented')

        case "pick15":
            raise NotImplementedError('pick15 variant is not yet implemented')

        case _:
            raise NotImplementedError(f'Variant "{args.variant}" is unknown')

def main():
    parser = setup_parser()
    args = parser.parse_args()

    model = make_model(args)
    view = View()
    controller = Controller(model, view)

    controller.start_game()

if __name__ == '__main__':
    main()
