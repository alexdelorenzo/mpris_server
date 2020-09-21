from setuptools import setup
from pathlib import Path

requirements = \
  Path('requirements.txt') \
    .read_text() \
    .split('\n')
readme = Path('README.md').read_text()

setup(name="mpris_server",
      version="0.2.11",
      description="Publish a MediaPlayer2 MPRIS device to D-BUS.",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://alexdelorenzo.dev",
      author="Alex DeLorenzo",
      license="AGPL-3.0",
      packages=['mpris_server'],
      zip_safe=True,
      install_requires=requirements,
      python_requires='>=3.6',
)
