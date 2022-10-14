# animwal

This project is a high performance animated desktop background setter for X11 and Windows that won't set your CPU on fire and drain your laptop battery.

#### Dependencies
You'll need `SDL2` and `SDL_Image` libraries. if you're on Windows, you can just install `pysdl2-dll` package from PyPI.  
For Python packages, you need `pysdl2` and `pillow`. Also, I'm using [poetry](https://python-poetry.org/) as package manager on this project.

#### Usage
```
usage: animwal [-h] [-a path time] [-g gif-file output]

animated wallpapers

optional arguments:
  -h, --help            show this help message and exit
  -a path time, --animate path time
                        animate image files placed in `path` every `time` ms.
  -g gif-file output, --generate gif-file output
                        extract frames from given `gif-file` to `output` folder.
```
