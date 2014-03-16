/*
 * DisKnobUI - Using an old hard-disk as a rotary encoder: Shows the logo for
 *             SAPO (http://www.sapo.pt) with rotating eyes based on events
 *             coming from Arduino (over serial) or a Raspberry Pi (over UDP).
 *
 * Copyright (c) 2014 Carlos Rodrigues <cefrodrigues@gmail.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */


import java.util.*;
import processing.serial.*;

/*
 * The "UDP" processing library can be downloaded directly from
 * the author's website at: http://ubaa.net/shared/processing/udp/
 */
import hypermedia.net.UDP;


// Get motion events from the network (otherwise, get them from a serial port)...
final boolean EVENTS_FROM_NETWORK = false;

// If getting events from the network, listen on this address (can be multicast)...
final String LOCAL_UDP_ADDRESS = "224.1.1.1";
final short LOCAL_UDP_PORT = 15002;


// Queue of motion events received but still not drawn...
List<Integer> events = new LinkedList<Integer>();

PImage sapoLogo;  // ...the logo for "sapo.pt"...
float angle = 0;  // ...and the angle of it's eyes


void setup()
{
  size(450, 450);
  frameRate(30);
  smooth();

  // The background image must have transparent eyes...
  sapoLogo = loadImage("sapo.png");

  if (EVENTS_FROM_NETWORK) {
    UDP server = new UDP(this, LOCAL_UDP_PORT, LOCAL_UDP_ADDRESS);
    server.setReceiveHandler("networkEvent");
    server.listen(true);
    println("Listening on " + LOCAL_UDP_ADDRESS + ":" + LOCAL_UDP_PORT);
  } else {
    String device = getArduinoPort();

    if (device == null) {
      println("ERROR: It looks like there's no Arduino connected.");
      System.exit(1);
    }

    Serial port = new Serial(this, device, 9600);
    port.bufferUntil(10);
    println("Listening on: " + device);
  }
}


void draw()
{
  synchronized (events) {
    // Don't burn CPU if there's nothing going on...
    if (frameCount > 1 && events.size() < 1) {
      return;
    }

    for (int motion: events) {
      angle += PI/32 * motion;
    }

    events.clear();
  }

  // The background will show through the eyes...
  background(217, 213, 70);
  image(sapoLogo, 0, 0);

  drawEyes(angle);
}


void drawEyes(float angle) {
  pushStyle();
  noStroke();

  // Left eye...
  pushMatrix();
  translate(165, 100);
  rotate(angle);

  fill(32);
  ellipse(15, 25, 35, 35);

  fill(192);
  ellipse(18, 28, 10, 10);
  popMatrix();

  // Right eye...
  pushMatrix();
  translate(285, 100);
  rotate(angle);

  fill(32);
  ellipse(15, 25, 35, 35);

  fill(192);
  ellipse(18, 28, 10, 10);
  popMatrix();

  popStyle();
}


String getArduinoPort() {
  for (String device: Serial.list()) {
    if (device.contains("tty.usbmodem") || device.contains("tty.usbserial")) {
      // This is not guaranteed to actually *be* an Arduino...
      return device;
    }
  }

  return null;
}


boolean queueEvent(String message) {
  if (!message.matches("^(?:CW|CCW)$")) {
    return false;
  }

  synchronized (events) {
    events.add(message.equals("CW") ? 1 : -1);
  }

  return true;
}


void networkEvent(byte[] data, String ip, int port) {
  queueEvent(new String(data).trim());
}


void serialEvent(Serial port) {
  queueEvent(port.readString().trim());
}


/* EOF - DisKnobUI.pde */
