# pyright : strict

from collections.abc import Sequence
from typing import Protocol

from .project_types import PlayerId, Cell, Symbol, Feedback, Field
from .interfaces import WinConditionCheckerProtocol, SymbolManagerProtocol

class GridGameModel:
    def __init__(self, grid_size: int, player_symbols: Sequence[Symbol], player_count: int, 
                 win_condition_checker: WinConditionCheckerProtocol, symbol_manager: SymbolManagerProtocol):
        if player_count <= 1:
            raise ValueError(
                f'Must have at least two players (found {player_count})')

        unique_symbols = set(player_symbols)

        if len(unique_symbols) != len(player_symbols):
            raise ValueError(
                f'Player symbols must be unique (was {player_symbols}')

        if len(player_symbols) != player_count:
            raise ValueError(
                f'Player symbols must be exactly {player_count} (was {player_symbols})')

        self._field = Field(grid_size)
        self._player_count = player_count
        self._current_player: PlayerId = 1
        self._win_condition_checker = win_condition_checker
        self._symbol_manager = symbol_manager

    @property
    def occupied_cells(self) -> dict[Cell, Symbol]:
        return self._field.occupied_cells

    @property
    def grid_size(self):
        return self._field.grid_size

    @property
    def is_game_over(self):
        return (
            self.winner is not None or
            not self._field.has_unoccupied_cell()
        )

    @property
    def current_player(self) -> PlayerId:
        return self._current_player

    @property
    def player_count(self):
        return self._player_count

    @property
    def next_player(self) -> PlayerId:
        return (
            self.current_player + 1 if self.current_player != self.player_count else
            1
        )

    @property
    def winner(self) -> PlayerId | None:
        return self._win_condition_checker.check_winner()

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        return self._symbol_manager.get_symbol_choices(player)

    def place_symbol(self, symbol: Symbol, cell: Cell) -> Feedback:
        if self.is_game_over:
            return Feedback.GAME_OVER

        if symbol not in self.get_symbol_choices(self.current_player):
            return Feedback.INVALID_SYMBOL

        if not self._field.is_within_bounds(cell):
            return Feedback.OUT_OF_BOUNDS

        if self._field.get_symbol_at(cell) is not None:
            return Feedback.OCCUPIED

        self._field.place_symbol(symbol, cell)

        self._win_condition_checker.update_field(self._field)
        
        if self.winner is not None:
            return Feedback.VALID

        self._switch_to_next_player()

        return Feedback.VALID

    def _switch_to_next_player(self):
        self._current_player = self.next_player