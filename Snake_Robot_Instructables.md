# Snake Robot: 7 Steps (with Pictures)
By joesinstructables in Circuits > Arduino

**Introducing The Lake Erie Mamba: a Reconfigurable Robot Snake**

This versatile reptile is made with off-the-shelf parts and is capable of several different modes of locomotion, including slithering, inch worm, sidewinding and rolling. (The rolling configuration involves the snake curling itself into a vertical loop and rolling like a wheel.) The snake contains 12 segments actuated by servo motors and joined with metal brackets. The servos are controlled by an Arduino Mega and powered by a 7.4 volt battery pack. A four button keyfob transmitter provides remote control for the snake. The snake is also capable of autonomous movement. Such a robot can be constructed with many different types of servos and brackets. If you decide to give one a try, I hope you find the code given below to be useful.

## Step 1: List of Materials

* 1 Arduino Mega (with optional sensor shield)
* 1 Four Button Remote Control Keyfob and corresponding Momentary M4 Receiver
* 12 servos
* 12 servo C-brackets
* 12 servo side brackets
* 4 long servo C-brackets
* 1 Lithium Ion Battery
* 12 Lego wheels
* 1 continuous rotation servo
* 1 IR distance sensor and mount
* 1 micro servo and mount
* Several sensor cables and connectors
* 1 large wheel
* 1 5AA battery holder with barrel plug
* Various nuts, bolts, wire clips, and velcro straps

## Step 2: Construction

The Lake Erie Mamba is capable of several configurations depending on the type of movement desired. This step will detail construction of the form capable of serpentine motion (slithering). The other configurations will be described in separate steps below.

Each of the 12 segments consists of a servo motor, a C-bracket, a side bracket, a wire clip and a set of Lego wheels. Two screw holes need to be drilled into the Lego wheel axle to allow it to be connected to the C-bracket. I also had to drill two screw holes into the wire clip to attach it to the C-bracket. After all 12 segments are connected, head and tail sections need to be added in order to accommodate the Arduino and batteries. To make them I used a side bracket and two long C-brackets connected as in the photo above.

I put the Arduino and the 5AA battery holder that powers it into the tail section of the snake. The servos are powered by a separate supply, the 7.4 volt battery pack, which went into the head of the snake. All the servo wires need to run back to the Arduino. I tried to keep things neat by controlling the wires with the wire clips. Just make sure there is enough slack along each run.

The servos from head to tail are connected to Arduino pins 2 through 13. The 5AA battery pack is connected directly to the Arduino and the 7.4 volt battery pack is connected to the input supply on the Arduino sensor shield. I held the batteries and Arduino in place with Velcro strips.

Remote control is handled by the keyfob transmitter and receiver I got from Adafruit. I can't tell you how useful I find these things. They're a quick and easy way to add remote control to any Arduino project. On the receiver, the ground pin is connected to the Arduino ground. The voltage pin is connected to a 5 volt pin from the Arduino (not the separate 7.4 volt supply) and pins DO through D3 on the receiver are connected to pins 14 through 17 on the Arduino, respectively. The keyfob remote control of the snake will be explained in the sections below.

## Step 3: Serpentine Motion

On a real snake, the scales on the snake's skin are configured so that there is less friction in the direction parallel to the snake's body than there is in the direction perpendicular to the snake's body. This is achieved on the robot snake by attaching passive wheels to each segment that roll in the direction along the length of the snake. The result is that the snake can be propelled forward just by sending a sine or cosine wave down its body.

The Arduino code for control of this motion is given in the link below. The servo motors take commands that set their angle. If all servos are set to 90 degrees, then the snake's position is a straight line. An angle less than or greater than 90 will then tell the servo to bend left or right. The basic command to control each servo for forward motion is given by a command of the form:

`sn.write(90+amplitude*cos(frequency counter*3.14159/180 - n*lag);`

In the command above, n is the number of the current segment and takes values from 1 to 12, amplitude determines how wide the wave is (i.e. how much the "S" shape is curved), frequency (along the variable delayTime) determine the speed of the snake, counter is the loop variable that takes the snake through its undulation and lag is the constant angular difference between segments. The term `3.14159/180` is just the degrees to radians conversion.

Each of the servo motors is controlled by a command of this form and all twelve of these commands are put into a `for` loop where the variable counter runs from 0 to 360 degrees. This commands the snake to perform one forward undulation and ends with the snake back in its original position. In the loop there is also a command `delay(delayTime);`. Since servos do not respond instantaneously, the code has to pause to give the servos time to move. For the servos I am using, a value of 7 microseconds seems to work well and gives a nice smooth movement. To make the snake move in reverse, it is the exact same loop, only with the counter running from 360 down to zero.

If the wave responsible for the motion of the snake is centered at 90 degrees, the snake's center of mass will move in a straight line. If the wave is centered at an angle less than 90 degrees, the snake will turn left, and for more than 90 degrees, the snake will turn right. This is controlled in the code by the variables leftOffset and rightOffset. Thus, to turn the snake it is a simple matter of adding one of these offsets to the write commands in the forward motion loop. However, since this will result in a somewhat jerky motion as the snake moves suddenly to the turn starting position, what I do in the turn loops is slowly ramp up the offset at the beginning of the turn loop, and slowly ramp down the offset at the end of the turn loop. This results in a smoother motion.

Each of four motion commands will complete one undulation of the desired movement and return the snake to the exact same position at the end of the loop. To add remote control to the robot I use the keyfob transmitter/receiver pair listed in step 1. The four buttons on the keyfob transmitter correspond to a) forward, b) reverse, c) left turn, d) right turn. The receiver is connected to the Arduino with forward to pin 14, reverse to pin 15, left turn to pin 16 and right turn to pin 17. These pins are declared as input and set to LOW. Now I just put the section of code for each movement into an `if` loop that runs when the appropriate pin goes HIGH (i.e. when the appropriate button is pushed).

## Step 4: Rectilinear Motion

Inch worm movement (also known as rectilinear motion) is achieved by removing the wheels and setting the snake on its side. A vertical hump sent from the tail of the snake toward the head moves the snake forward. Unfortunately, there is no way to turn the snake in this configuration.

That's where the continuous rotation servo and large wheel come in. The first segment of the snake is turned up 90 degrees and two long C-brackets and a side bracket are used to secure the continuous rotation servo with the large wheel attached to it. The wheel is oriented so that it is parallel to the ground. When the snake wants to turn, the servos along the snake are positioned so that the wheel comes down perpendicular to the ground with the front servos off the ground so that the wheel bears weight. The wheel can then be rotated left or right to turn the snake. When the turn is completed, the wheel is returned to its horizontal position off the ground and the snake can continue forward.

Remote control is again achieved using the keyfob remote. The four buttons correspond to a) forward, b) toggle wheel up/wheel down, c) left turn, d) right turn. The code contains a variable `wheelState` that takes the values 0 or 1. The variable is initialized to 0. If button b) is pressed and `wheelState == 0`, then the wheel will come down and the variable `wheelState` will be set to 1. Buttons c) and d) can now be pressed to turn the robot. When the turn is completed, button b) is pressed again. When button b) is pressed and `wheelState == 1`, the wheel will be lifted and the robot can continue forward. The variable `wheelState` will also then be reset to 0.

## Step 5: Sidewinding Motion

Sidewinding is a motion used by snakes when they are on shifting terrain such as sand. This motion is actually a combination of the serpentine and rectilinear motions described above. To achieve this motion the robot must be reconfigured. A side bracket connecting one segment to the C-bracket of the next segment is unscrewed and rotated 90 degrees. This is done along the entire length of the snake.

Thus servos 1, 3, 5, 7, 9, and 11 will be positioned as for serpentine motion and servos 2, 4, 6, 8, 10, and 12 will positioned as for rectilinear motion. Sidewinding motion is achieved by sending a horizontal cosine wave down the odd numbered servos and a vertical cosine wave (offset from the horizontal wave by 90 degrees) down the even numbered servos. The result is a sideways motion.

## Step 6: Rolling Motion

Another type of motion possible for this robot (but not for real snakes) is rolling. In the rectilinear configuration, the head and tail can be connected to form a loop, and the servos can be commanded so that the robot rolls like a wheel. The symmetry necessary for this motion requires that the head and tail sections be removed, so that the Arduino and batteries cannot be carried by the robot. Thus this motion is only possible in tethered mode.

## Step 7: Autonomous Motion

Finally, an IR distance sensor attached to a micro servo can be connected to the robot's head to allow for autonomous movement. This is best done in the serpentine configuration. The snake will move forward one complete undulation, stop, and take a distance measurement. If the path is clear the snake will continue forward. When it gets too close to an object, the robot will stop and the micro servo will turn the distance sensor to the left and right to take two more distance measurements. The snake will then reverse one undulation, turn in the direction of the clearer path, and continue forward.
