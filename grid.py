from __future__ import annotations
from typing import List         # For hinting
from actor import Actor
from tile import Tile, TileState
from maths import Vector2D


class Grid(Actor):
    """ 
    A class containing the graph (list of Tile nodes). Graph is
    inputted to A* pathfinder, which outputs a path (a chain of linked Tiles). 
    """

    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # For building graph
        self._m_tiles: List[list] = []

        # Rows/cols in grid
        self._m_num_rows: int = 7
        self._m_num_cols: int = 16
        # Start y-pos of top left corner
        self._m_start_y: float = 192.0
        # Width/height of tile
        self._m_tile_size: float = 64.0

        self._m_selected_tile: Tile = None
        self._m_enemy_time: float = 1.5         # Time between enem
        self._m_next_enemy_time: float = None   # Time left until next enem

        # Building Graph: start
        # Initialize array w/ zeroes
        self._m_tiles = [[0 for c in range(self._m_num_cols)]
                         for r in range(self._m_num_rows)]
        # Fill array w/ tiles
        for r in range(self._m_num_rows):
            for c in range(self._m_num_cols):
                self._m_tiles[r][c] = Tile(self.get_game())
                self._m_tiles[r][c].set_position(Vector2D(
                    self._m_tile_size / 2.0 + c * self._m_tile_size, self._m_start_y + r * self._m_tile_size))
        # Add adjacency list to each tile (this step turns array into graph!)
        for row in range(self._m_num_rows):
            for col in range(self._m_num_cols):
                if row > 0:
                    self._m_tiles[row][col]._m_adjacent.append(
                        self._m_tiles[row - 1][col])
                if row < self._m_num_rows - 1:
                    self._m_tiles[row][col]._m_adjacent.append(
                        self._m_tiles[row + 1][col])
                if col > 0:
                    self._m_tiles[row][col]._m_adjacent.append(
                        self._m_tiles[row][col - 1])
                if col < self._m_num_cols - 1:
                    self._m_tiles[row][col]._m_adjacent.append(
                        self._m_tiles[row][col + 1])
        # Building Graph: end

        # Set start/end tiles
        self.get_start_tile().set_tile_state(TileState.eSTART)
        self.get_end_tile().set_tile_state(TileState.eBASE)

        # Use A* algorithm to find a path
        # Input: graph, start/end tile (in reverse, see book)
        # Output: a path (a linked-chain of tiles from start tile to end tile)
        self.find_path(self.get_end_tile(), self.get_start_tile())

        # Set state of each tile in the path to ePATH
        self.update_path_tiles(get_start_tile())

        # TODO enemy

    def _select_tile(self, row: int, col: int) -> None:
        pass

    # Update textures for tiles on path
    def _update_path_tiles(self, start: Tile) -> None:
        pass
