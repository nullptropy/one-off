# coding: utf-8

import os
import time
import ctypes
import itertools

from sdl2 import *
from animwal.helpers import (
    get_handle,
    load_textures
)

class Animate(object):
    def __init__(self, path, millis):
        self.path = path
        self.secs = int(millis) / 1000

        SDL_Init(SDL_INIT_VIDEO)

        self.window   = SDL_CreateWindowFrom(get_handle())
        self.renderer = SDL_CreateRenderer(
            self.window, 2,
            SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
        )

        texture_files = [os.path.join(path, fname) for fname in sorted(os.listdir(path))]
        self.textures = load_textures(self.renderer, texture_files)

    def render_texture(self, texture):
        SDL_RenderSetViewport(self.renderer, SDL_Rect(1220//2, 360 // 2, 720, 720));
        SDL_RenderCopy(self.renderer, texture, None, None)
        SDL_RenderPresent(self.renderer)

    def mainloop(self):
        for texture in itertools.cycle(self.textures):
            try:
                self.render_texture(texture)

                event = SDL_Event()
                SDL_PollEvent(ctypes.byref(event))
                if event.type == SDL_QUIT:
                    break

                time.sleep(self.secs)
            except KeyboardInterrupt:
                break

        # SDL_Quit()
        # SDL_DestroyWindow(self.window)
        SDL_DestroyRenderer(self.renderer) # also frees textures