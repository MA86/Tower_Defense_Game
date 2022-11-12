from __future__ import annotations
import sdl2dll      # Needed DLLs
import sdl2
import sdl2.sdlimage as sdlimage

from actor import Actor, State
from grid import Grid
import ctypes


class Game:
    def __init__(self):
        # TODO add type hinting
        self._m_window = None
        self._m_renderer = None

        # Lists
        self._m_textures = {}
        self._m_actors = []
        self._m_pending_actors = []
        self._m_sprites = []

        self._m_updating_actors: bool = False
        self._m_running: bool = True
        self._m_time_then: float = 0.0

        self._m_grid: Grid = None

    def initialize(self) -> bool:
        # Initialize SDL
        result = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_AUDIO)
        if result != 0:
            sdl2.SDL_Log("SDL initialization failed: ",
                         sdl2.SDL_GetError())
            return False

        # Create window
        self._m_window = sdl2.SDL_CreateWindow(b"Spaceship Shooter",
                                               sdl2.SDL_WINDOWPOS_CENTERED,
                                               sdl2.SDL_WINDOWPOS_CENTERED, 1024, 768, 0)
        if self._m_window == None:
            sdl2.SDL_Log("Window failed: ", sdl2.SDL_GetError())
            return False

        # Create renderer
        self._m_renderer = sdl2.SDL_CreateRenderer(self._m_window,
                                                   -1,
                                                   sdl2.SDL_RENDERER_ACCELERATED |
                                                   sdl2.SDL_RENDERER_PRESENTVSYNC)
        if self._m_renderer == None:
            sdl2.SDL_Log("Renderer failed: ", sdl2.SDL_GetError())
            return False

        # Initialize SDL image
        if sdlimage.IMG_Init(sdlimage.IMG_INIT_PNG) == 0:
            sdl2.SDL_Log("Image failed: ", sdl2.SDL_GetError())
            return False

        self._load_data()

        # Initial time
        self._m_time_then = sdl2.SDL_GetTicks()

        return True

    def run_loop(self) -> None:
        while self._m_running:
            self._process_input()
            self._process_update()
            self._process_output()

    def shutdown(self) -> None:
        # Shutdown in reverse
        self._unload_data()
        sdlimage.IMG_Quit()
        sdl2.SDL_DestroyRenderer(self._m_renderer)
        sdl2.SDL_DestroyWindow(self._m_window)
        sdl2.SDL_Quit()

    def _process_input(self) -> None:
        event = sdl2.SDL_Event()    # Empty object
        # Get and check events-queue for Game
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                self._m_running = False
                break

        # Get key states-queue
        keyb_state = sdl2.SDL_GetKeyboardState(None)

        # Check key states-queue for Game
        if keyb_state[sdl2.SDL_SCANCODE_ESCAPE]:
            self._m_running = False

        # Check key states-queue for Grid
        if keyb_state[sdl2.SDL_SCANCODE_B]:
            # TODO build tower
            pass
        # Check mouse states-queue for Grid
        x = ctypes.c_int(0)
        y = ctypes.c_int(0)
        mousebut_state = sdl2.SDL_GetMouseState(
            ctypes.byref(x), ctypes.byref(y))
        if (mousebut_state & sdl2.SDL_BUTTON_LMASK) != 0:
            self._m_grid.process_click(x.value, y.value)

        # Check key states-queue for Actors
        self._m_updating_actors = True
        for actor in self._m_actors:
            actor.input(keyb_state)
        self._m_updating_actors = False

    def _process_update(self) -> None:
        # Wait 16ms (frame limiting)
        sdl2.SDL_Delay(16)

        time_now: ctypes.c_uint32 = sdl2.SDL_GetTicks()
        delta_time: float = (time_now - self._m_time_then) / 1000.0
        # Clamp max delta time (for debugging)
        if delta_time > 0.05:
            delta_time = 0.05
        # Time now is time then
        self._m_time_then: ctypes.c_uint32 = sdl2.SDL_GetTicks()

        # Update actors
        self._m_updating_actors = True
        for actor in self._m_actors:
            actor.update(delta_time)
        self._m_updating_actors = False

        # Add pending actors
        for pending_actor in self._m_pending_actors:
            self._m_actors.append(pending_actor)
        self._m_pending_actors.clear()

        # Collect dead actors
        dead_actors = []
        for dead_actor in self._m_actors:
            if dead_actor.get_state() == State.eDEAD:
                dead_actors.append(dead_actor)

        # Remove dead actors from self._m_actors
        for da in dead_actors:
            da.delete()

    def _process_output(self) -> None:
        # Clear color-buffer to black
        sdl2.SDL_SetRenderDrawColor(self._m_renderer, 34, 139, 34, 255)
        sdl2.SDL_RenderClear(self._m_renderer)

        # Draw sprites
        for sprite in self._m_sprites:
            sprite.draw(self._m_renderer)

        # Swap color-buffer to display on screen
        sdl2.SDL_RenderPresent(self._m_renderer)

    def _load_data(self) -> None:
        # Load grid
        self._m_grid = Grid(self)

    def _unload_data(self) -> None:
        while len(self._m_actors) != 0:
            actor = self._m_actors.pop()
            actor.delete()
        for texture in self._m_textures.values():
            sdl2.SDL_DestroyTexture(texture)
        self._m_textures.clear()

    def get_texture(self, filename) -> sdl2.SDL_Texture:
        # Search for texture in dictionary
        texture = self._m_textures.get(filename)
        if texture != None:
            return texture
        else:
            # Load image
            surface = sdlimage.IMG_Load(filename)
            if surface == None:
                sdl2.SDL_Log("Failed to load image file: ", filename)
                return None
            # Create texture
            texture = sdl2.SDL_CreateTextureFromSurface(
                self._m_renderer, surface)
            sdl2.SDL_FreeSurface(surface)
            if texture == None:
                sdl2.SDL_Log("Failed to create texture: ", filename)
                return None

            # Add texture to dic
            self._m_textures[filename] = texture
        return texture

    def add_actor(self, actor: Actor) -> None:
        if self._m_updating_actors:
            self._m_pending_actors.append(actor)
        else:
            self._m_actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        # Check in pending-actors list
        if actor in self._m_pending_actors:
            self._m_pending_actors.remove(actor)
        # Check in actors list
        if actor in self._m_actors:
            self._m_actors.remove(actor)

    def add_sprite(self, sprite: SpriteComponent) -> None:
        # Add based on draw order
        index = 0
        for i, c in enumerate(self._m_sprites):
            if sprite.get_draw_order() < c.get_draw_order():
                index = i
                break
        self._m_sprites.insert(index, sprite)

    def remove_sprite(self, sprite: SpriteComponent) -> None:
        self._m_sprites.remove(sprite)
