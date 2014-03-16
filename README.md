DisKnobUI
=========

An Arduino program to use an old hard-drive as a rotary input device.

A Python program for the Raspberry Pi to do the same thing, but sending data over UDP multicast.

A Processing application that gets events from either two programs and shows the frog logo from [SAPO](http://www.sapo.pt) with rotating eyes.

This is a much more precise and reliable (and less hackish) version of an old implementation that I did back in 2009, based on this instructable:

  http://www.instructables.com/id/HDDJ-Turning-an-old-hard-disk-drive-into-a-rotary/


How it Works
============

The motor that drives the platters on a hard-drive is a stepper motor, which means it has four coils that, when energized in the proper sequence, attract the magnet in the core making it rotate. If the platters are spun manually, the motor acts as a generator and a (sinusoidal) voltage is induced in each of the four coils.

![waveforms](https://raw.github.com/carlosefr/DisKnobUI/master/waveforms.png)

If we choose one of the motor's terminals as a reference point (and connect it to ground), we can use a voltage comparator (OpAmp) for each of the remaining three terminals to output HIGH if its voltage is above the reference (ground) level, or LOW if it is below.

![circuit](https://raw.github.com/carlosefr/DisKnobUI/master/circuit.png)

The sequence of the outputs is unique for clockwise motion, and for counter-clockwise motion. By identifying the sequence, an Arduino or Raspberry Pi can decide in which direction the platters are being rotated. The faster the motion, the faster the sequence.


Hardware
========

The operational amplifiers used as voltage comparators are LM324N (four OpAmps in one package), but it should work with any other equivalent part, as long as it works with both Vcc=3.3V (when using the Raspberry Pi) or Vcc=5V (when using the Arduino), and can handle negative voltages (voltages below ground level) up to the magnitude of Vcc:

  http://www.ti.com/product/lm324-n

The HIGH output of these parts is somewhat below Vcc, but should work fine as it is still read as an HIGH by the Arduino and the Raspberry Pi. If you wish to adapt this to some other board, you may need a rail-to-rail OpAmp package, such as the TLV2374:

  http://www.ti.com/product/tlv2374

Software
========

The Arduino program uses no external libraries and requires nothing more than the standard Arduino distribution.

The Raspberry Pi program requires Python 2.7 and the ```RPi.GPIO``` library, which can both be found in the Raspbian repositories.

The Processing application requires the UDP library, which can be found at:

  http://ubaa.net/shared/processing/udp/

Screenshots
===========

You can watch a video of it working (using the Raspberry Pi program) here:

  http://videos.sapo.pt/TpU7DdsYIizWhWiggEsd

This is what it looks like on a Mac:

![screenshot](https://raw.github.com/carlosefr/DisKnobUI/master/screenshot.png)

And this is what the breadboard assembly looks like (with an Arduino Micro):

![breadboard](https://raw.github.com/carlosefr/DisKnobUI/master/breadboard.jpg)

Author
======

* Carlos Rodrigues <cefrodrigues@gmail.com>
