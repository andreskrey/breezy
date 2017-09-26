# breezy

## A simple RPI fan controller

### What you need

- Raspberry Pi
- 5v fan
- NPN Transistor
- Some cables

### Physical installation

You will need a 5v fan and a NPN Transistor. Basically you will want to connect to one 5v pin of the PI, one ground pin and one GPIO pin of your choice. Wire everything following [these instructions](https://hackernoon.com/how-to-control-a-fan-to-cool-the-cpu-of-your-raspberrypi-3313b6e7f92c).

### Software installation

1) `> git clone`
2) `> pip3 install -r requirements.txt`
3) Edit your `config.yml` using the reference `config.yml.dist` file.
4) `>python3 breezy.py &`