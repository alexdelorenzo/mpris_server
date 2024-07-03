from pathlib import Path
from typing import Final

from setuptools import find_packages, setup


__author__ = "Alex DeLorenzo <alex@alexdelorenzo.dev>"
__version__: Final[str] = '0.9.1'

NAME = "mpris_server"
DESCRIPTION = "⏯️ Publish a MediaPlayer2 MPRIS device to D-Bus."
LICENSE = "License :: OSI Approved :: LGPL-3.0-only"
URL = "https://github.com/alexdelorenzo/mpris_server"

PKGS: list[str] = list({
  f'{NAME}',
  f'{NAME}.mpris',
  f'{NAME}.interfaces',
  *find_packages(),
})

REQS: list[str] = Path('requirements.txt') \
  .read_text() \
  .splitlines()

REQS: list[str] = [
  req
  for req in REQS
  if not req.strip().startswith('#')
]

README: str = Path('README.md').read_text()

PYTHON_VERSION: str = '>=3.12'

setup(
  name=NAME,
  version=__version__,
  description=DESCRIPTION,
  long_description=README,
  long_description_content_type="text/markdown",
  url=URL,
  author=__author__,
  license=LICENSE,
  packages=PKGS,
  zip_safe=True,
  install_requires=REQS,
  python_requires=PYTHON_VERSION,
)
