from __future__ import annotations
from typing import List         # For hinting
from actor import Actor
from tile import Tile, TileState
from tower import Tower
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

        # Rows/cols in graph
        self._m_num_rows: int = 7
        self._m_num_cols: int = 16
        # Start y-pos of top left corner
        self._m_start_y: float = 192.0
        # Width/height of tile
        self._m_tile_size: float = 64.0

        self._m_selected_tile: Tile = None
        self._m_enemy_time: float = 1.5         # Time between enem.
        self._m_next_enemy_time: float = None   # Time left until next enem.

        # BUILD GRAPH: Start

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

        # BUILD GRAPH: End

        # Set start/end tiles
        self.get_start_tile().set_tile_state(TileState.eSTART)
        self.get_end_tile().set_tile_state(TileState.eBASE)

        # Use A* algorithm to find a path
        # Input: graph, start/end tile (in reverse, see book)
        # Output: a path (a linked-chain of tiles from start tile to end tile)
        self.find_path(self.get_end_tile(), self.get_start_tile())

        # Set state of each tile in the path to ePATH
        self._update_path_tiles(self.get_start_tile())

        # TODO enemy

    def find_path(self, start: Tile, goal: Tile) -> bool:
        for r in range(self._m_num_rows):
            for c in range(self._m_num_cols):
                self._m_tiles[r][c]._g = 0.0
                self._m_tiles[r][c]._m_in_open_set = False
                self._m_tiles[r][c]._m_in_closed_set = False

        open_set: list = []

        current: Tile = start
        current._m_in_closed_set = True

        # Do...while
        while True:
            # Add adjacent nodes to open set
            for neighbor in current._m_adjacent:
                if neighbor._m_blocked:
                    continue

                # Only check nodes not in closed set
                if neighbor._m_in_closed_set == False:
                    if neighbor._m_in_open_set == False:
                        neighbor._m_parent = current
                        neighbor._h = (neighbor.get_position() -
                                       goal.get_position()).length()
                        # g(x) is parent's g + cost of traversing edge
                        neighbor._g = current._g + self._m_tile_size
                        neighbor._f = neighbor._g + neighbor._h
                        open_set.append(neighbor)
                        neighbor._m_in_open_set = True
                    else:
                        # Compute g(x) cost if current becomes parent
                        new_g = current._g + self._m_tile_size
                        if new_g < neighbor._g:
                            # Adopt node
                            neighbor._m_parent = current
                            neighbor._g = new_g
                            # f(x) change due to g(x) change
                            neighbor._f = neighbor._g + neighbor._h

            # All possible paths exhausted if open set is empty
            if len(open_set) < 1:
                break

            # Find lowest cost node in open set
            lowest: Tile = min(open_set, key=lambda n: n._f)
            current = lowest
            open_set.remove(lowest)
            current._m_in_open_set = False
            current._m_in_closed_set = True

            if current == goal:
                break

        # Is a path found?
        if current == goal:
            return True
        else:
            return False

    def get_start_tile(self) -> Tile:
        return self._m_tiles[3][0]

    def get_end_tile(self) -> Tile:
        return self._m_tiles[3][15]

    def process_click(self, x: int, y: int) -> None:
        y -= int(self._m_start_y - self._m_tile_size / 2)
        if y >= 0:
            x /= int(self._m_tile_size)
            y /= int(self._m_tile_size)
            if x >= 0 and x < int(self._m_num_cols) and y >= 0 and y < int(self._m_num_rows):
                self._select_tile(int(y), int(x))

    def _select_tile(self, row: int, col: int) -> None:
        # Start/end tile selection is not allowed
        tile_state: TileState = self._m_tiles[row][col].get_tile_state()
        if tile_state != TileState.eSTART and tile_state != TileState.eBASE:
            # Deselect previous selected
            if self._m_selected_tile:
                self._m_selected_tile.toggle_select()
            self._m_selected_tile = self._m_tiles[row][col]
            self._m_selected_tile.toggle_select()

    # Update textures for tiles on path
    def _update_path_tiles(self, start: Tile) -> None:
        # Reset all tiles to default, except start/end
        for r in range(self._m_num_rows):
            for c in range(self._m_num_cols):
                if (not(r == 3 and c == 0) and not(r == 3 and c == 15)):
                    self._m_tiles[r][c].set_tile_state(TileState.eDEFAULT)

        t: Tile = start._m_parent
        while t != self.get_end_tile():
            t.set_tile_state(TileState.ePATH)
            t = t._m_parent

    def build_tower(self) -> None:
        if self._m_selected_tile and self._m_selected_tile._m_blocked == False:
            self._m_selected_tile._m_blocked = True
            if self.find_path(self.get_end_tile(), self.get_start_tile()):
                t = Tower(self.get_game())
                t.set_position(self._m_selected_tile.get_position())
            else:
                # Tower would block the path, don't allow build
                self._m_selected_tile._m_blocked = False
                self.find_path(self.get_end_tile(), self.get_start_tile())
            self._update_path_tiles(self.get_start_tile())

    def update_actor(self, dt: float) -> None:
        return super().update_actor(dt)

        # Is it time to spawn new enemy?
        self._m_next_enemy_time -= dt
        if self._m_next_enemy_time <= 0.0:
            Enemy(self.get_game())
            self._m_next_enemy_time += self._m_enemy_time
