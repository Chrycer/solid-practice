from .project_types import PlayerId, Symbol, Cell, Field
from .interfaces import WinConditionCheckerProtocol, SymbolManagerProtocol


class TicTacToeWinConditionChecker(WinConditionCheckerProtocol):
    def __init__(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]):
        self._field = field
        self._symbol_to_player = symbol_to_player

    def check_winner(self) -> PlayerId | None:
        row_groups = [
            [Cell(row, k) for k in self._field.valid_coords]
            for row in self._field.valid_coords
        ]

        col_groups = [
            [Cell(k, col) for k in self._field.valid_coords]
            for col in self._field.valid_coords
        ]

        diagonals = [
            # Backslash
            [Cell(k, k) for k in self._field.valid_coords],
            # Forward slash
            [Cell(k, self._field.grid_size - k + 1)
            for k in self._field.valid_coords],
        ]

        for groups in [row_groups, col_groups, diagonals]:
            for group in groups:
                if (basis := self._field.get_symbol_at(group[0])) is not None and \
                        self._field.are_all_equal_to_basis(basis, group):
                    winner = self._symbol_to_player.get(basis)
                    assert winner is not None, \
                        f'Winning symbol {basis} in cell group {groups} has no associated player'

                    return winner

        return None

class TicTacToeSymbolManager(SymbolManagerProtocol):
    def __init__(self, player_symbols: dict[PlayerId, Symbol]):
        self._player_to_symbol = player_symbols

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        if player not in self._player_to_symbol:
            raise ValueError(f'Invalid player: {player}')
        return [self._player_to_symbol[player]]