DisKnobUI
=========

Using an old hard-disk as a rotary encoder: Shows the logo for SAPO (http://www.sapo.pt) with rotating eyes based on events coming from an Arduino over the serial port, or from a Raspberry Pi over UDP multicast.

![DisKnobUI](https://github.com/carlosefr/DisKnobUI/blob/master/screenshot.png)

How it Works
============

The engine that drives the platters on a hard-drive is a stepper motor, which means it has four coils that, when energized in the proper sequence, attract the magnet in the core making it rotate. If the platters are spun manually, the motor acts as a generator and a varying voltage is induced in each of the four coils.

![Waveforms](https://github.com/carlosefr/DisKnobUI/blob/master/waveforms.png)

If we choose one of the motor's terminals as a reference point (and connect it to ground), we can use a comparator for each of the remaining three terminals to output HIGH if its voltage is above the reference, or LOW if it's below.

![Circuit](https://github.com/carlosefr/DisKnobUI/blob/master/circuit.png)

The sequence of the outputs is unique for clockwise motion, and for counter-clockwise motion. By identifying the sequence, an Arduino or Raspberry Pi can decide in which direction the platters are being rotated. The faster the motion, the faster the sequence.

Dependencies
============

The Raspberry Pi "driver" requires the RPi.GPIO library, which can be found in the Rasbpian repositories. The Processing application requires the UDP library, which can be found at:

  http://ubaa.net/shared/processing/udp/

Media
=====

You can watch a video of it working (using a Raspberry Pi) here:

  http://videos.sapo.pt/cefrodrigues
