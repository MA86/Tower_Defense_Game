from __future__ import annotations
from actor import Actor
from sprite_component import SpriteComponent
from move_component import MoveComponent
from circle_component import CircleComponent


class Bullet(Actor):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        sc: SpriteComponent = SpriteComponent(self)
        sc.set_texture(b"assets/projectile.png")
        mc: MoveComponent = MoveComponent(self)
        mc.set_forward_speed(40.0)
        self._m_circle: CircleComponent = CircleComponent(self)
        self._m_circle.set_radius(5.0)

        self._m_live_time: float = 1.0

    def update_actor(self, dt: float) -> None:
        super().update_actor(dt)

        # TODO
