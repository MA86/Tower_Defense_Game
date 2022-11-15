from __future__ import annotations
from actor import Actor, State
from circle_component import CircleComponent
from sprite_component import SpriteComponent
from nav_component import NavComponent
import maths


class Enemy(Actor):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # Add to Game's enemies list
        game.get_enemies().append(self)

        # Position at start tile
        self.set_position(game.get_grid().get_start_tile().get_position())

        # Components
        self._m_circle: CircleComponent = CircleComponent(self)
        self._m_circle.set_radius(25.0)

        nc: NavComponent = NavComponent(self)
        nc.set_forward_speed(20.0)
        nc.start_path(game.get_grid().get_start_tile())

        sc: SpriteComponent = SpriteComponent(self)
        sc.set_texture(game.get_texture(b"assets/airplane.png"))

    def delete(self) -> None:
        super().delete()
        self.get_game().get_enemies().remove(self)

    def update_actor(self, dt: float) -> None:
        super().update_actor(dt)

        # Am I near end tile?
        diff: Vector2D = self.get_position(
        ) - self.get_game().get_grid().get_end_tile().get_position()
        if maths.check_near_zero(diff.length(), 10.0):
            self.set_state(State.eDEAD)

    def get_circle(self):
        return self._m_circle
