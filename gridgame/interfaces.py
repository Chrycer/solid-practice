from typing import Protocol
from .project_types import PlayerId, Symbol, Cell, Field

class WinConditionCheckerProtocol(Protocol):
    def __init__(self, field: Field, symbol_to_player: dict[Symbol, PlayerId]):
        ...

    def check_winner(self) -> PlayerId | None:
        ...

class SymbolManagerProtocol(Protocol):
    def __init__(self, player_symbols: dict[PlayerId, Symbol]):
        ...

    def get_symbol_choices(self, player: PlayerId) -> list[Symbol]:
        ...