#!/usr/bin/env python
#
# disknob.py - Using an old hard-disk as a rotary encoder (Raspberry Pi).
#
# Copyright (c) 2014 Carlos Rodrigues <cefrodrigues@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import

import signal
import os
import time
import socket

import RPi.GPIO as GPIO

from threading import RLock


# The GUI application's address (multicast)...
REMOTE_ADDRESS = "224.1.1.1"
REMOTE_PORT = 15002

# GPIO pins that change when the disk is rotated...
INPUT_PINS = (23, 24, 25)

# A full-sequence of pin states for a clockwise/counter-clockwise motion...
CW_SEQUENCE = ((0,0,0), (0,1,0), (0,1,1), (1,1,1), (1,0,1), (1,0,0))
CCW_SEQUENCE = ((0,0,0), (1,0,0), (1,0,1), (1,1,1), (0,1,1), (0,1,0))

# A subsequence of GPIO pin states must match at least this number of states from
# the above motion sequences before a motion event is sent to the GUI application...
MIN_MATCHES = 3


class ChannelCallback(object):
    def __init__(self, socket, address):
        """Initialize. Motion events will be sent to the specified address."""

        self.socket = socket
        self.address = address

        self.num_events = 0

        # RPi.GPIO invokes the callback method from different threads for each
        # registered GPIO pin, which means we must handle concurrent calls...
        self.lock = RLock()

        self.states = [(0,0,0)]

        self.cw = set(subsequences(CW_SEQUENCE, MIN_MATCHES, circular=True))
        self.ccw = set(subsequences(CCW_SEQUENCE, MIN_MATCHES, circular=True))


    def event_count(self):
        """Return the number of events since the callback was created."""

        with self.lock:
            return self.num_events


    def __call__(self, channel):
        """Handle a state change for a GPIO channel."""

        state = list(self.states[-1])
        state[INPUT_PINS.index(channel)] = GPIO.input(channel)

        with self.lock:
            self.states.append(tuple(state))

            if len(self.states) > MIN_MATCHES:
                del self.states[0]

            subsequence = tuple(self.states)

            if subsequence in self.cw:
                event = "CW"   # ...clockwise motion.
            elif subsequence in self.ccw:
                event = "CCW"  # ...counter-clockwise motion.
            else:
                event = "UNK"  # ...not enough data to decide.

            # Send a motion event to the GUI application...
            self.socket.sendto(event, address)
            self.num_events += 1


def handle_signals(signal, frame):
    """Exit cleanly upon receiving a signal."""

    GPIO.cleanup()
    os._exit(0)


def subsequences(sequence, length, circular=False):
    """
    Generate all unique strict subsequences of the specified length,
    optionally treating "sequence" as an infinite circular array.

    """

    if circular:
        for i in xrange(len(sequence)):
            subsequence = sequence[i:i + length]
            yield subsequence + sequence[0:length - len(subsequence)]
    else:
        for i in xrange(len(sequence) - length + 1):
            yield sequence[i:i + length]


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    # Properly handle "Ctrl-C" and termination signals...
    signal.signal(signal.SIGINT, handle_signals)
    signal.signal(signal.SIGTERM, handle_signals)

    try:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (socket.gethostbyname(REMOTE_ADDRESS), REMOTE_PORT)

        motion = ChannelCallback(udp, address)

        for channel in INPUT_PINS:
            GPIO.setup(channel, GPIO.IN)
            GPIO.add_event_detect(channel, GPIO.BOTH, callback=motion)

        prev_events = 0

        while True:
            time.sleep(1)

            # Show something to look alive...
            curr_events = motion.event_count()
            if curr_events > prev_events:
                print("%d events" % curr_events)
            prev_events = curr_events
    finally:
        GPIO.cleanup()


# EOF - disknob.py
