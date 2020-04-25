# ▶️ Add MPRIS Integration to Media Players
`mpris_server` provides an adapter and event-listener for your app to integrate MPRIS media control support into your media player.

Whereas [existing MPRIS libraries for Python](https://github.com/hugosenari/mpris2) implement clients for MPRIS, `mpris_server` serves more as a "server" to supply MPRIS with information from, and control of, your media player. If you're looking to interact with applications that have MPRIS integration, use a client library. If you want to give your media player an MPRIS interface, use this library.

`mpris_server` is a fork of [Mopidy-MPRIS](https://github.com/mopidy/mopidy-mpris) that provides a general library for any media player to add MPRIS support.

Checkout [chromecast_mpris](https://github.com/alexdelorenzo/chromecast_mpris) for an app that uses this library.

## Features
Implements the following from the [MPRIS specification](https://specifications.freedesktop.org/mpris-spec/2.2/):
  * [x] MediaPlayer2
  * [x] MediaPlayer2.Player
  * [ ] MediaPlayer2.Playlist
  
The library also provides an event-listener that emits `org.freedesktop.DBus.Properties.PropertiesChanged` in response to changes in your media player. This allows for real-time updates from your media player to MPRIS.

## Installation
Run `pip3 install -r requirements.txt`, followed by `python3 setup.py install`. 

### Requirements
 - Linux
 - DBUS
 - Python >= 3.6
 - python3-gi (Python GObject introspection)
 - `requirements.txt`

## Usage
### Implement `adapters.MprisAdapter`
Subclass `adapters.MprisAdapter` and implement each method. `get_metadata()` is optional to implement, only implement it if you don't want to implement `get_current_track()` and create `adapters.Track` objects.

After subclassing, pass an instance to an instance of `server.Server`.

### Implement `adapters.EventAdapter`
Subclass `adapters.EventAdapter`. This interface has a good default implementation, only override its methods if your app calls for it.

Integrate the adapter with your application to listen for changes in your media player that MPRIS needs to be updated about.

### Create the Server and Publish!
Create an instance of `server.Server`, pass it an instance of your `MprisAdapter`, and call `publish()`.

```python3
mpris = Server('MyMedia', adapter=my_adapter)
mpris.publish() 
```

### Example
```python3
from mpris_server.adapters import MprisAdapter, EventAdapter
from mpris_server.server import Server

from my_app import app  # custom app you want to integrate


class MyMediaAdapter(MprisAdapter):
    # NOTE: don't do this! make sure to override methods in the MprisAdapter interface
    pass


class ChromecastEventAdapter(EventAdapter):
    # This is okay! EventAdapter has good default implementations for its methods.
    # Override the default implementation if it suits your app.
    pass


my_adapter = MyMediaAdapter()
mpris = Server('MyMedia', adapter=my_adapter)
mpris.publish()  # this announces your media player on DBUS

event_listener = ChromecastEventAdapter()
app.register_event_listener(event_listener)
```

## License
See `LICENSE`. Message me if you'd like to use this project with a different license.
