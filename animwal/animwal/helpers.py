# coding: utf-8

import os

from PIL import Image
from sdl2 import (
    sdlimage,
    SDL_FreeSurface,
    SDL_DestroyTexture,
    SDL_CreateTextureFromSurface
)

if os.name != 'nt':
    from animwal.linux import get_handle

else:
    from animwal.windows import get_handle

def extract_from_gif(fname, output='.'):
    gif_file = Image.open(fname)
    n_frames = gif_file.n_frames
    os.makedirs(output, exist_ok=True)

    for index in range(n_frames):
        gif_file.seek(index)
        gif_file.save(
            os.path.join(output, f'{index:0>{len(str(n_frames))}}.png'),
            'PNG'
        )

    gif_file.close()
    return n_frames

def load_textures(renderer, image_files):
    textures = []

    for fname in image_files:
        image = sdlimage.IMG_Load(fname.encode())
        textures.append(SDL_CreateTextureFromSurface(renderer, image))
        SDL_FreeSurface(image)

    return textures

def unload_textures(textures):
    for texture in textures:
        SDL_DestroyTexture(texture)