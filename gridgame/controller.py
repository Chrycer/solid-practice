from .model import GridGameModel
from .view import View
from .project_types import Feedback


class Controller:
    def __init__(self, model: GridGameModel, view: View):
        self._model = model
        self._view = view

    def start_game(self) -> None:
        model = self._model
        view = self._view

        while not model.is_game_over:
            while True:
                view.print_board(model.grid_size, model.occupied_cells)
                view.print_current_player(model.current_player)

                choices = model.get_symbol_choices(model.current_player)
                assert len(choices) > 0

                symbol = (
                    view.ask_for_symbol_choice(choices) if len(choices) > 1 else
                    choices[0]
                )

                cell = view.ask_for_cell(model.grid_size)

                match model.place_symbol(symbol, cell):
                    case Feedback.VALID:
                        if model.is_game_over:
                            break
                        break

                    case Feedback.OUT_OF_BOUNDS:
                        view.print_error_out_of_bounds()

                    case Feedback.OCCUPIED:
                        view.print_error_occupied()

                    case Feedback.GAME_OVER:
                        view.print_error_game_over()

                    case Feedback.INVALID_SYMBOL:
                        view.print_error_invalid_symbol()

                view.print_divider()

        view.print_board(model.grid_size, model.occupied_cells)

        if model.winner is not None:
            view.print_winner(model.winner)
        else:
            view.print_draw()
