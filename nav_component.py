from __future__ import annotations
from move_component import MoveComponent
import maths


class NavComponent(MoveComponent):
    """ 
    Using pathfinder's output, moves Actor from one node to the next node. 
    """

    def __init__(self, owner: Actor, update_order: int = 10) -> None:
        super().__init__(owner, update_order)

        # Next point
        self._m_next_node: Tile = None

    # Overrides
    def update(self, dt: float) -> None:
        if self._m_next_node:
            # Check if actor is nearing the next point
            diff: Vector2D = self._m_owner.get_position() - self._m_next_node.get_position()
            if abs(diff.length()) <= 2.0:
                self._m_next_node: Tile = self._m_next_node.get_parent()
                self.turn_to(self._m_next_node.get_position())

        # Otherwise, continue moving forward
        super().update(dt)

    # Recieves path (A* output, which is a chain of tiles)
    def start_path(self, start: Tile) -> None:
        self._m_next_node: Tile = start.get_parent()
        self.turn_to(self._m_next_node.get_position())

    def turn_to(self, point: Vector2D) -> None:
        direction: Vector2D = point - self._m_owner.get_position()
        angle: float = maths.atan2(direction.y, direction.x)

        self._m_owner.set_rotation(angle)
