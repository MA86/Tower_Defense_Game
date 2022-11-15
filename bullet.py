from __future__ import annotations
from actor import Actor, State
from sprite_component import SpriteComponent
from move_component import MoveComponent
from circle_component import CircleComponent


class Bullet(Actor):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        # Components
        sc: SpriteComponent = SpriteComponent(self)
        sc.set_texture(game.get_texture(b"assets/projectile.png"))

        mc: MoveComponent = MoveComponent(self)
        mc.set_forward_speed(200.0)

        self._m_circle: CircleComponent = CircleComponent(self)
        self._m_circle.set_radius(5.0)

        self._m_live_time: float = 1.0

    def update_actor(self, dt: float) -> None:
        super().update_actor(dt)

        # Check for collision
        for e in self.get_game().get_enemies():
            if self._m_circle.intersect(self._m_circle, e.get_circle()):
                e.set_state(State.eDEAD)
                self.set_state(State.eDEAD)
                break

        self._m_live_time -= dt
        if self._m_live_time <= 0.0:
            self.set_state(State.eDEAD)
