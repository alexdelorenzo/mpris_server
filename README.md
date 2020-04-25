# ▶️ Add MPRIS Integration to Media Players
`mpris_server` provides an adapter and event-listener for your app to integrate MPRIS media control support into your media player.

Whereas [existing MPRIS libraries for Python](https://github.com/hugosenari/mpris2) implement clients for MPRIS, `mpris_server` exists more as a "server" to supply MPRIS with information from, and control of, your media player. If you want to give your media player an MPRIS interface, `mpris_server` is right for you.

`mpris_server` is a fork of [Mopidy-MPRIS](https://github.com/mopidy/mopidy-mpris) that was made into a general purpose library.

Checkout [📺chromecast_mpris](https://github.com/alexdelorenzo/chromecast_mpris) for an app that uses `mpris_server`.

## Features
Implements the following from the [MPRIS specification](https://specifications.freedesktop.org/mpris-spec/2.2/):
  * [x] MediaPlayer2
  * [x] MediaPlayer2.Player
  * [ ] MediaPlayer2.Playlist
  
The library also provides an event-listener that emits `org.freedesktop.DBus.Properties.PropertiesChanged` in response to changes in your media player. This allows for real-time updates from your media player to DBus.

## Installation
### Requirements
 - Linux
 - DBus
 - Python >= 3.6
 - python3-gi (Python GObject introspection)
 - `requirements.txt`

### PyPI
`pip3 install mpris_server`

### Github
Clone the repo, run `pip3 install -r requirements.txt`, followed by `python3 setup.py install`. 

## Usage
### Implement `adapters.MprisAdapter`
Subclass `adapters.MprisAdapter` and implement each method.

After subclassing, pass an instance to an instance of `server.Server`.

### Implement `adapters.EventAdapter`
Subclass `adapters.EventAdapter`. This interface has a good default implementation, only override its methods if your app calls for it.

If you choose to reimplement its methods, call `emit_changes()` with a `List[str]` of [properties](https://specifications.freedesktop.org/mpris-spec/2.2/Player_Interface.html) that changed.

Integrate the adapter with your application to listen for changes in your media player that DBus needs to know about. For example, if the user pauses the media player, be sure to call `EventAdapter.on_playpause()` in the app. DBus won't know about the change otherwise.

### Create the Server and Publish
Create an instance of `server.Server`, pass it an instance of your `MprisAdapter`, and call `publish()` to publish your media player via DBus.

```python3
mpris = Server('MyMedia', adapter=my_adapter)
mpris.publish() 
```

Call `loop()` to enter the DBus event loop. 
```python3
mpris.loop() 
```

### Example
```python3
from mpris_server.adapters import MprisAdapter, EventAdapter, Track
from mpris_server.server import Server

from my_app import app  # custom app you want to integrate


class MyMediaAdapter(MprisAdapter):
    # Make sure to implement all methods on MprisAdapter, not just get_current_track()
    def get_current_track(self) -> Track:
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
my_adapter = MyMediaAdapter()
mpris = Server('MyMedia', adapter=my_adapter)

# initialize app integration with mpris
event_handler = MyAppEventHandler()
app.register_event_handler(event_handler)

# publish and serve
mpris.loop()
```

## License
See `LICENSE`. Message me if you'd like to use this project with a different license.
