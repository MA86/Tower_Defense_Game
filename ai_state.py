from __future__ import annotations


class AIState:
    """ AI STATE BASE CLASS """

    def __init__(self, owner: AIComponent) -> None:
        self._m_owner = owner

    # State-specific behavior
    def update(self, dt: float) -> None:
        # Implementable
        pass

    def on_enter(self) -> None:
        # Implementable
        pass

    def on_exit(self) -> None:
        # Implementable
        pass

    def get_name(self) -> str:
        # Implementable
        pass


class AIPatrol(AIState):
    def __init__(self, owner: AIComponent) -> None:
        super().__init__(owner)

    # Implements
    def update(self, dt: float) -> None:
        pass

    # Implements
    def on_enter(self) -> None:
        pass

    # Implements
    def on_exit(self) -> None:
        pass

    # Implements
    def get_name(self) -> str:
        return "Patrol"
