# Live Lights

My custom, work-in-progress implementation of [Ambilight](https://www.google.com/search?tbm=isch&q=ambilight).

Unlike many other implementations, this project doesn't rely on XMBC or video playing through a computers media player (although does require a computer to parse and process data).

There's a few extra features packed in too:
* IR control to change the render mode, turn On & Off and adjust brightness, etc
* Different modes:
  * Single Colour: just one colour, selected via IR
  * Colour Cycle: Slowly cycle through the colour spectrum
  * Disco Mode: Various patterns, strobes and colours (ideally music triggered - but that's for another day)
  * Dynamic Movie Mode: Each LED gets it's own colour based on local colour and brightness
  * Ambient Movie Mode: All LEDs get a colour to represent the colour temperature of the scene on TV
* Wireless "Surround Light" modules to help light the room with ambient light, away from the TV

There's a heavy focus on [Processing](http://processing.org) throughout given that's where the smarts live.
I've tried my best to make the modes and renderers as modular as possible to allow others to contribute new modes or refine the image processing implementation (I'm a total n00b at DSP).

## Flow

The application flows as such:
![Platform Map](platform.png "Platform Map")

There's three different projects in this Repository:
* **Application**: The [Processing](http://processing.org) app that captures video, processes it and sends RGB data to an Arduino
* **TV_Light**: Arduino code to accept serial data from [Processing](http://processing.org) and output to RED Strip and Xbee for Surround Lights
* **Surround_Light**: Arduino code reading RGB code from Xbee and adjusting local LED(s) to suit
* **IR_Reciever**: Super simple Arduino app to take IR input and send to [Processing](http://processing.org) for tuning, mode selection and on/off, etc