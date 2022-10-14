# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['animwal']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=7.2.0,<8.0.0', 'pysdl2>=0.9.7,<0.10.0']

entry_points = \
{'console_scripts': ['animwal = animwal.__main__:main']}

setup_kwargs = {
    'name': 'animwal',
    'version': '0.1.1',
    'description': 'animated wallpapers',
    'long_description': "# animwal\n\nThis project is a rip-off-_ish_ Python port of [paperview](https://github.com/glouw/paperview). It's description: A high performance animated desktop background setter for X11 and Windows (with animwal) that won't set your CPU on fire, drain your laptop battery, or lower ya vidya game FPS.\n\n##### What is different from paperview?\nWell, at the core there is nothing really different, just some SDL routines. But this project also supports Windows by utilizing WinAPI. And if you're lazy, built-in support for extracting frames from gif files.\n\n#### Dependencies\nYou'll need `SDL2` and `SDL_Image` libraries. if you're on Windows, you can just install `pysdl2-dll` package from PyPI.  \nFor Python packages, you need `pysdl2` and `pillow`. Also, I'm using [poetry](https://python-poetry.org/) as package manager on this project.\n\n#### Usage\n```\nusage: animwal [-h] [-a path time] [-g gif-file output]\n\nanimated wallpapers\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -a path time, --animate path time\n                        animate image files placed in `path` every `time` ms.\n  -g gif-file output, --generate gif-file output\n                        extract frames from given `gif-file` to `output` folder.\n```",
    'author': 'nwxnk',
    'author_email': 'nwxnk@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
