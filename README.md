# ▶️ Add MPRIS integration to media players

`mpris_server` provides adapters to integrate [MPRIS](https://specifications.freedesktop.org/mpris-spec/2.2/) support in
your media player or device. By supporting MPRIS in your app, you will allow Linux users to control all aspects of
playback from the media controllers they already have installed.

Whereas [existing MPRIS libraries for Python](https://github.com/hugosenari/mpris2) implement clients for apps with
existing MPRIS support, `mpris_server` is a library used to implement MPRIS support in apps that don't already have it.
If you want to give your media player an MPRIS interface, then `mpris_server` is right for you.

`mpris_server` is a fork of [Mopidy-MPRIS](https://github.com/mopidy/mopidy-mpris) that was extended and made into a
general purpose library.

Check out [`📺 cast_control`](https://github.com/alexdelorenzo/cast_control) for an app that uses `mpris_server`.

## Features

Implements the following from the [MPRIS specification](https://specifications.freedesktop.org/mpris-spec/2.2/):

* [x] MediaPlayer2
* [x] MediaPlayer2.Player
* [x] MediaPlayer2.Playlist
* [x] MediaPlayer2.TrackList

The library also provides an event handler that emits `org.freedesktop.DBus.Properties.PropertiesChanged` in response to
changes in your media player. This allows for real-time updates from your media player to D-Bus.

## Installation

### Requirements

- Linux / *BSD / [macOS](https://github.com/zbentley/dbus-osx-examples)
- [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/)
- Python >= 3.7
- [PyGObject](https://pypi.org/project/PyGObject/)
- `requirements.txt`

#### Installing PyGObject

On Debian-derived distributions like Ubuntu, install `python3-gi` with `apt`. On Arch, you'll want to
install `python-gobject`.

On macOS, install [`pygobject3`](https://formulae.brew.sh/formula/pygobject3) via `brew`. Note that `mpris_server` on
macOS hasn't been tested, but is theoretically possible to use.

Use `pip` to install `PyGObject>=3.34.0` if there are no installation candidates available in your vendor's package
repositories.

### PyPI

`pip3 install mpris_server`

### GitHub

Clone the repo, run `pip3 install -r requirements.txt`, followed by `python3 setup.py install`.

## Usage

### Implement `adapters.MprisAdapter`

Subclass `adapters.MprisAdapter` and implement each method.

After subclassing, pass an instance to an instance of `server.Server`.

### Implement `events.EventAdapter`

Subclass `adapters.EventAdapter`. This interface has a good default implementation, only override its methods if your
app calls for it.

If you choose to re-implement its methods, call `emit_changes()` with the corresponding interface and a `List[str]`
of [properties](https://specifications.freedesktop.org/mpris-spec/2.2/Player_Interface.html) that changed.

Integrate the adapter with your application to emit changes in your media player that DBus needs to know about. For
example, if the user pauses the media player, be sure to call `EventAdapter.on_playpause()` in the app. DBus won't know
about the change otherwise.

### Create the Server and Publish

Create an instance of `server.Server`, pass it an instance of your `MprisAdapter`, and call `publish()` to publish your
media player via DBus.

```python3
mpris = Server('MyMediaPlayer', adapter=my_adapter)
mpris.publish() 
```

Call `loop()` to enter the DBus event loop, or enter the DBus event loop elsewhere in your code.

```python3
mpris.loop() 
```

Or:

```python3
from gi.repository import GLib


loop = GLib.MainLoop()
loop.run()
```

### Example

```python3
from mpris_server.adapters import MprisAdapter
from mpris_server.events import EventAdapter
from mpris_server.server import Server
from mpris_server import Metadata

from my_app import app  # custom app you want to integrate


class MyAppAdapter(MprisAdapter):
  # Make sure to implement all methods on MprisAdapter, not just metadata()
  def metadata(self) -> Metadata:
    ...
  # and so on


class MyAppEventHandler(EventAdapter):
  # EventAdapter has good default implementations for its methods.
  # Only override the default methods if it suits your app.

  def on_app_event(self, event: str):
    # trigger DBus updates based on events in your app
    if event == 'pause':
      self.on_playpause()
    ...
  # and so on


# create mpris adapter and initialize mpris server
my_adapter = MyAppAdapter()
mpris = Server('MyApp', adapter=my_adapter)

# initialize app integration with mpris
event_handler = MyAppEventHandler(root=mpris.root, player=mpris.player)
app.register_event_handler(event_handler)

# publish and serve
mpris.loop()
```

## Support

Want to support this project and [other open-source projects](https://github.com/alexdelorenzo) like it?

<a href="https://www.buymeacoffee.com/alexdelorenzo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="60px" style="height: 60px !important;width: 217px !important;max-width:25%" ></a>

## License

`mpris_server` is released under the AGPLv3, see [`LICENSE`](/LICENSE). Message me if you'd like to use this project
with a different license.
