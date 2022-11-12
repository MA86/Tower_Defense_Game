from __future__ import annotations
from actor import Actor
from move_component import MoveComponent
from sprite_component import SpriteComponent
import maths


class Tower(Actor):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self._m_next_attack_time: float = None
        self._m_attack_time: float = 2.5
        self._m_attack_range: float = 100.0

        # Components
        self._m_move: MoveComponent = MoveComponent(self)

        sc: SpriteComponent = SpriteComponent(self, 200)
        sc.set_texture(game.get_texture(b"assets/tower.png"))

        self._m_next_attack_time = self._m_attack_time

    def update_actor(self, dt: float) -> None:
        return super().update_actor(dt)

        self._m_next_attack_time -= dt
        if self._m_next_attack_time <= 0.0:
            e: Enemy = self.get_game().get_nearest_enemy(self.get_position())
            if e != None:
                # Vector from tower to enemy
                dir: Vector2D = e.get_position() - self.get_position()
                dist: float = dir.length()
                if dist < self._m_attack_range:
                    # Face enemy
                    self.set_rotation(maths.atan2(dir.y, dir.x))
                    # Spawn bullet towards enemy
                    b: Bullet = Bullet(self.get_game())
                    b.set_position(self.get_position())
                    b.set_rotation(self.get_rotation())
            self._m_next_attack_time += self._m_attack_time
