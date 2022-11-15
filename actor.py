from __future__ import annotations
from typing import List         # For hinting
from enum import Enum           # For enum
import ctypes
from maths import Vector2D
import maths


class State(Enum):
    eALIVE = 1
    ePAUSED = 2
    eDEAD = 3


class Actor:
    """ ACTOR BASE CLASS """

    def __init__(self, game: Game) -> None:
        # State
        self._m_state: State = State.eALIVE

        # Transform
        self._m_position: Vector2D = Vector2D(0.0, 0.0)
        self._m_scale: float = 1.0
        self._m_rotation: float = 0.0

        # Components (sorted)
        self._m_components: List[Component] = []

        # Loose association
        self._m_game: Game = game

        # Add self to list
        game.add_actor(self)

    def delete(self) -> None:
        # If container gone -> contained gone! [Composition]
        self.get_game().remove_actor(self)
        for c in list(self._m_components):
            c.delete()

    def update(self, dt: float) -> None:
        if self._m_state == State.eALIVE:
            self.update_components(dt)
            self.update_actor(dt)

    def update_components(self, dt: float) -> None:
        for c in self._m_components:
            c.update(dt)

    def update_actor(self, dt: float) -> None:
        # Implementable
        pass

    def input(self, keyb_state: ctypes.Array) -> None:
        if self._m_state == State.eALIVE:
            self.input_components(keyb_state)
            self.input_actor(keyb_state)

    def input_components(self, keyb_state: ctypes.Array) -> None:
        for c in self._m_components:
            c.input(keyb_state)

    def input_actor(self, keyb_state: ctypes.Array) -> None:
        # Implementable
        pass

    def add_component(self, component: Component) -> None:
        # Add based on update order
        index = 0
        for i, c in enumerate(self._m_components):
            index = i
            if component.get_update_order() < c.get_update_order():
                break
        self._m_components.insert(index, component)

    def remove_component(self, component: Component) -> None:
        self._m_components.remove(component)

    # Getters/setters
    def get_position(self) -> Vector2D:
        return self._m_position

    def set_position(self, pos: Vector2D) -> None:
        self._m_position = pos

    def get_scale(self) -> float:
        return self._m_scale

    def set_scale(self, scale: float) -> None:
        self._m_scale = scale

    def get_rotation(self) -> float:
        return self._m_rotation

    def set_rotation(self, rotation: float) -> None:
        self._m_rotation = rotation

    def get_forward(self) -> Vector2D:
        # Note: equation (unit circle) returns normalized vector
        return Vector2D(maths.cos(self._m_rotation), maths.sin(self._m_rotation))

    def get_state(self) -> State:
        return self._m_state

    def set_state(self, state: State) -> None:
        self._m_state = state

    def get_game(self) -> Game:
        return self._m_game
