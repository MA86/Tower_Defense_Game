from __future__ import annotations
import sdl2


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
        # Misc. updating code here...
        sdl2.SDL_Log("Updating " + self.get_name() + " state")
        # Figure out death code here...
        dead = True

        if dead:
            self._m_owner.change_state("Death")

    # Implements
    def on_enter(self) -> None:
        sdl2.SDL_Log("Entering " + self.get_name() + " state")

    # Implements
    def on_exit(self) -> None:
        sdl2.SDL_Log("Exiting " + self.get_name() + " state")

    # Implements
    def get_name(self) -> str:
        return "Patrol"


class AIDeath(AIState):
    def __init__(self, owner: AIComponent) -> None:
        super().__init__(owner)

    # Implements
    def update(self, dt: float) -> None:
        sdl2.SDL_Log("Updating " + self.get_name() + " state")

    # Implements
    def on_enter(self) -> None:
        sdl2.SDL_Log("Entering " + self.get_name() + " state")

    # Implements
    def on_exit(self) -> None:
        sdl2.SDL_Log("Exiting " + self.get_name() + " state")

    # Implements
    def get_name(self) -> str:
        return "Death"


class AIAttack(AIState):
    def __init__(self, owner: AIComponent) -> None:
        super().__init__(owner)

    # Implements
    def update(self, dt: float) -> None:
        sdl2.SDL_Log("Updating " + self.get_name() + " state")

    # Implements
    def on_enter(self) -> None:
        sdl2.SDL_Log("Entering " + self.get_name() + " state")

    # Implements
    def on_exit(self) -> None:
        sdl2.SDL_Log("Exiting " + self.get_name() + " state")

    # Implements
    def get_name(self) -> str:
        return "Attack"
