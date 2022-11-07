from __future__ import annotations
import sdl2
from component import Component


class AIComponent(Component):
    def __init__(self, owner: Actor) -> None:
        super().__init__(owner)

        # Dictionary of name:state
        self._m_state_map: dict = {}

        self._m_current_state: AIState = None

    # Implements
    def update(self, dt: float) -> None:
        # Update current state
        if self._m_current_state:
            self._m_current_state.update(dt)

    def change_state(self, name: str) -> None:
        # Exit current state
        if self._m_current_state:
            self._m_current_state.on_exit()
        # Find new state
        self._m_current_state = self._m_state_map.get(name)
        if self._m_current_state:
            # Enter new state
            self._m_current_state.on_enter()
        else:
            sdl2.SDL_Log("AIState not in dictionary!")
            self._m_current_state = None
