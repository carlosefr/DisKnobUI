/*
 * DisKnob - Using an old hard-disk as a rotary encoder (v2).
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


// Input pins for Red, White, Green disk channels (OpAmp outputs)...
static const char pins[3] = {2, 3, 4};

/*
 * A full (circular) clockwise sequence is "000,010,011,111,101,100", but
 * can be identified by any of its possible 3-element subsequences...
 */
static const char cw_states[6][3][3] = {
  {{0, 0, 0}, {0, 1, 0}, {0, 1, 1}},
  {{0, 1, 0}, {0, 1, 1}, {1, 1, 1}},
  {{0, 1, 1}, {1, 1, 1}, {1, 0, 1}},
  {{1, 0, 0}, {0, 0, 0}, {0, 1, 0}},
  {{1, 0, 1}, {1, 0, 0}, {0, 0, 0}},
  {{1, 1, 1}, {1, 0, 1}, {1, 0, 0}}
};

/*
 * A full (circular) counter-clockwise sequence is "000,100,101,111,011,010",
 * but can be identified by any of its possible 3-element subsequences...
 */
static const char ccw_states[6][3][3] = {
  {{0, 0, 0}, {1, 0, 0}, {1, 0, 1}},
  {{0, 1, 0}, {0, 0, 0}, {1, 0, 0}},
  {{0, 1, 1}, {0, 1, 0}, {0, 0, 0}},
  {{1, 0, 0}, {1, 0, 1}, {1, 1, 1}},
  {{1, 0, 1}, {1, 1, 1}, {0, 1, 1}},
  {{1, 1, 1}, {0, 1, 1}, {0, 1, 0}}
};


// The sequence of last-seen disk channel states...
static char state[3][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};


void setup() 
{ 
  pinMode(pins[0], INPUT);
  pinMode(pins[1], INPUT);
  pinMode(pins[2], INPUT);

  Serial.begin(9600); 
} 

 
void loop()
{
  state[2][0] = digitalRead(pins[0]);
  state[2][1] = digitalRead(pins[1]);
  state[2][2] = digitalRead(pins[2]);

  // When state changes, try to match the memorized states with any known motion subsequence...
  if (memcmp(state[2], state[1], sizeof(state[2])) != 0) {
    for (short i = 0; i < sizeof(cw_states)/sizeof(cw_states[0]); i++) {
      if (memcmp(state, cw_states[i], sizeof(state)) == 0) {
        Serial.println("CW");  // ...match clockwise motion
        break;
      }
      
      if (memcmp(state, ccw_states[i], sizeof(state)) == 0) {
        Serial.println("CCW");  // ...match counter-clockwise motion
        break;
      }
    }

    // Shift all input states into the past...
    memcpy(state[0], state[1], sizeof(state[0]));
    memcpy(state[1], state[2], sizeof(state[1]));
  }

  delay(2);
} 


/* EOF - DisKnob.ino */
