from setuptools import setup
from pathlib import Path


REQS = \
  Path('requirements.txt') \
    .read_text() \
    .split('\n')

REQS = [
  req
  for req in REQS
  if not req.strip().startswith('#')
]

README = Path('README.md').read_text()


setup(
  name="mpris_server",
  version="0.3.0",
  description="Publish a MediaPlayer2 MPRIS device to D-Bus.",
  long_description=README,
  long_description_content_type="text/markdown",
  url="https://alexdelorenzo.dev",
  author="Alex DeLorenzo",
  license="AGPL-3.0",
  packages=['mpris_server'],
  zip_safe=True,
  install_requires=REQS,
  python_requires='>=3.6',
)
