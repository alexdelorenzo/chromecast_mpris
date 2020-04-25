# Control Chromecasts with MPRIS
Control your Chromecast via MPRIS media player controls. 

MPRIS integration is [enabled by default](https://github.com/KDE/plasma-workspace/tree/master/applets/mediacontroller) in Plasma Desktop, and [there are options for GNOME, too](https://extensions.gnome.org/extension/1379/mpris-indicator-button/).

[`playerctl` provides a CLI](https://github.com/altdesktop/playerctl) for controlling media players through MPRIS.

## Installation

Run `pip3 install -r requirements.txt`, followed by `python3 setup.py install`. 
You'll get `chromecast_mpris` added to your `$PATH`.

<img src="/assets/mpris_widget.png" width="200" />

### Requirements
 - Linux
 - DBUS
 - Python >= 3.6
 - python3-gi (Python GObject introspection)
 - `requirements.txt`
 

## Usage
You'll need to make sure that your computer is on the same network as your Chromecasts, and that you're able to make connections to them. 

It also helps to know the names of the devices in advance.

### Example
#### Help
```bash
$ chromecast_mpris --help
Usage: command.py [OPTIONS]

  Control Chromecasts through MPRIS media controls.

Options:
  -n, --name TEXT          Specify Chromecast, otherwise control first
                           Chromecast found.
  -l, --log-level INTEGER  Debugging log level.  [default: 20]
  --help                   Show this message and exit.
```

#### Connecting to Device
Connect to Chromecast named "MyChromecast" and run the adapter in the background.
```bash
$ chromecast_mpris -n MyChromecast &
[1] 1234
$
```

## License
See `LICENSE`. Message me if you'd like to use this project with a different license.