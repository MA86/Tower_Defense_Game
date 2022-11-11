from __future__ import annotations
from actor import Actor
from enum import Enum
from sprite_component import SpriteComponent


class TileState(Enum):
    eDEFAULT = 1
    ePATH = 2
    eSTART = 3
    eBASE = 4


class Tile(Actor):
    """ Representation of a node for graph. """

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # For A* pathfinding
        self._m_adjacent: list = []
        self._m_parent: Tile = None
        self._f: float = 0.0
        self._g: float = 0.0
        self._h: float = 0.0
        self._m_in_open_set: bool = None
        self._m_in_closed_set: bool = None
        self._m_blocked: bool = False

        self._m_sprite: SpriteComponent = None
        self._m_tile_state: TileState = TileState.eDEFAULT
        self._m_selected: bool = False

        # Components
        self._m_sprite = SpriteComponent(self)

        self._update_texture()

    def _update_texture(self) -> None:
        if self._m_tile_state == TileState.eSTART:
            text = b"assets/tile_tan.png"
        elif self._m_tile_state == TileState.eBASE:
            text = b"assets/tile_green.png"
        elif self._m_tile_state == TileState.ePATH:
            if self._m_selected:
                text = b"assets/tile_grey_selected.png"
            else:
                text = b"assets/tile_grey.png"
        else:
            if self._m_selected:
                text = b"assets/tile_brown_selected.png"
            else:
                text = b"assets/tile_brown.png"

        self._m_sprite.set_texture(self.get_game().get_texture(text))

    def get_tile_state(self) -> TileState:
        return self._m_tile_state

    def set_tile_state(self, state: TileState) -> None:
        self._m_tile_state = state
        self._update_texture()

    def get_parent(self) -> Tile:
        return self._m_parent
