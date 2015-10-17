DisKnobUI
=========

This repository contains software to use an old-hard drive as a rotary input device:

* An Arduino program that sends data over the serial port (```DisKnob.ino```).
* A Raspberry Pi program that sends data over UDP multicast (```disknob.py```).
* A Processing application that shows the old logo from [SAPO](http://www.sapo.pt) with rotating eyes (```DisKnobUI.pde```).

This is a much more precise, reliable, and less *hackish* version of an old project I made back in 2009 based on an [instructable](http://www.instructables.com/id/HDDJ-Turning-an-old-hard-disk-drive-into-a-rotary/) found online.

![screenshot](https://raw.github.com/carlosefr/DisKnobUI/master/screenshot.png)
[[video](https://www.youtube.com/watch?v=MvpPVjJnbao)]

How it Works
============

The motor that drives the platters on a hard-drive is a stepper motor, which means it has four coils that, when energized in the proper sequence, attract the magnet in the core making it rotate. However, if the platters are spun manually, the motor acts as a generator and a very small (sinusoidal) voltage is induced in each of the coils.

![waveforms](https://raw.github.com/carlosefr/DisKnobUI/master/waveforms.png)

If we choose one of the motor's terminals as a reference point (connected to ground), we can use one voltage comparator for each of the remaining three motor terminals to output a HIGH level if the terminal's voltage is above ground level, or LOW otherwise.

![circuit](https://raw.github.com/carlosefr/DisKnobUI/master/circuit.png)

The output sequence for all terminals is different for clockwise or counter-clockwise motion. By identifying the sequence, an Arduino or Raspberry Pi can decide in which direction the platters are being rotated. The faster the motion, the faster the sequence.


Hardware
========

The operational amplifiers used as voltage comparators are LM324N (four op-amps in one package), but it should work with any other equivalent part, as long as the part can be powered with either Vcc=3.3V (when using the Raspberry Pi) or Vcc=5V (when using the Arduino), and can also handle negative voltages up to the magnitude of Vcc:

  http://www.ti.com/product/lm324-n

The HIGH output of these op-amps is not quite Vcc, but should work fine as it's still read as an HIGH by the Arduino/Raspberry Pi. If you wish to adapt this to some other board, you may need a rail-to-rail op-amp package, such as the TLV2374:

  http://www.ti.com/product/tlv2374

Software
========

* The Arduino program uses no external libraries and requires nothing more than the standard Arduino distribution.
* The Raspberry Pi program requires Python 2.7 and the ```RPi.GPIO``` library, which can both be found in the Raspbian repositories.
* The Processing application requires the [UDP library](http://ubaa.net/shared/processing/udp/).

Author
======

* Carlos Rodrigues <cefrodrigues@gmail.com>
