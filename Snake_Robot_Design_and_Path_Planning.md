@# Snake-shaped robot design and path planning algorithm

RESEARCH Open Access© The Author(s) 2025. Open Access   This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International 
License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate 
credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. 
You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party 
material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material 
is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted 
use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit  h t t p : /  / c r  e a  t i v  e c o  m m o n  s  . o r g  / l i c e  n s  
e s / b  y - n c  - n d / 4 . 0 / .Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
https://doi.org/10.1007/s10791-025-09662-7
*Correspondence:
Cheng Wan-sheng
18840661211@163.com
1School of Electronic Engineering, 
University of Science and 
Technology, 114051, Liaoning, 
ChinaSnake-shaped robot design and path planning 
algorithm
Zhao Guang-hui1 and Cheng Wan-sheng1*
1 Introduction
Snake robots have garnered considerable attention as versatile platforms for traversing 
uneven and unstructured terrains, drawing on the undulatory locomotion patterns of 
their biological counterparts. Constructed from serially linked modules capable of coor -
dinated multi-degree-of-freedom motion, these platforms deliver a level of navigational 
adaptability unmatched by conventional wheeled or legged systems. Early biomechanical 
studies from the mid-twentieth century laid the foundation for this field by elucidating 
the wave-propagation mechanisms that underlie serpentine locomotion [ 1–4].
In the past decade, researchers have introduced a variety of mathematical and algo -
rithmic frameworks to capture and control the kinematics of snake robots. Planar ser -
pentine gait models [ 5] have formalized the role of curvature and phase shifting, while 
three-dimensional gait formulations have extended these insights into complex spatial 
environments. On the control front, techniques such as straight-path following [ 6] and 
reactive obstacle avoidance [ 7] have delivered robust real-time performance in cluttered Discover Computing
Abstract
Serpentine robots have broad application prospects in civilian, military, and 
other fields. However, recent developments in serpentine robot design, recent 
developments in snake-like robot design, mostly based on traditional algorithms, face 
several challenges in path planning and mapping. This study focuses on the snaking 
gait characteristics and proposes an improved path planning algorithm integrated 
with the robot’s mechanical design. The algorithm’s effectiveness is validated through 
simulation analysis. A functional relationship between the Serpentine locomotion 
control parameters and the motion shape parameters is established, enabling 
Serpentine locomotion path planning on the map based on the improved algorithm. 
The rationality and effectiveness of the proposed algorithm are verified through 
both simulation analysis and experimental validation. Real-world experiments are 
conducted using the developed snake robot prototype, and the results are compared 
with simulation outcomes. The findings confirm the rationality and effectiveness of 
the winding gait generation and path planning for obstacle avoidance, as well as the 
consistency between simulation and physical experimental results.
Keywords  Serpentine robot, Serpentine locomotion, Path planning, Joint simulation


Page 2 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
settings. Path-planning strategies have likewise diversified, from grid-based A* search 
variants to sampling-based methods like RRT* [ 8], and to learning-based schemes 
employing Deep Q-Networks (DQN) or Proximal Policy Optimization (PPO) [ 9, 10]. 
Hybrid approaches, for example the Sine Resistance Network (SRN) [ 11], have further 
demonstrated the ability to negotiate dynamic obstacles by blending impedance modu -
lation with curvature control.
Despite these advances, existing methods present trade-offs: model-based planners 
often incur high computational loads or yield suboptimal smoothness; reinforcement-
learning solutions require extensive training data and struggle with generalization across 
varying terrains; and SRN-style controllers, while agile, depend on precise force feed -
back that may be unavailable in resource-constrained platforms.
In this work, we introduce an optimized A*-based path planning algorithm tailored to 
the unique serpentine movement constraints of snake robots, augmented by a self-adap -
tive control parameter adjustment mechanism. Unlike classical A* variants, our method 
incorporates turning-cost and curvature constraints directly into the heuristic evalua -
tion, reducing unnecessary detours and smoothing the resulting trajectory. Compared 
to reinforcement-learning and SRN approaches, our algorithm achieves comparable 
obstacle-avoidance performance with significantly lower runtime and without reliance 
on extensive training or force-sensor feedback. Simulation and prototype experiments 
confirm that our approach maintains path fidelity within a 5% time–error margin while 
running on embedded hardware with limited computational resources, thus offering 
a practical solution for high-degree-of-freedom, multi-joint snake robots operating in 
dynamic, unstructured environments.
2 Research status of motor locomotion
2.1 Study of motor locomotion
Biological snakes adapt their locomotive patterns to suit different environments, a ver -
satility that has driven the development of highly adaptive serpentine robots. Decentral -
ized control mechanisms may hold the key to reproducing these behaviors in modular 
robots [ 8–10]. Foundational studies of snake biomechanics and propulsion modes have 
established the basis for modern snake‐robot gait design.
The most common terrestrial snake gait is serpentine locomotion, also known as the 
transverse wave gait [ 11, 12]. In this mode, the snake’s body forms a continuous sinu -
soidal curve, and at least three points of contact with the ground are required—two to 
generate thrust and one to balance forces—while the scales provide directional friction 
(Fig.  1a). When external objects aid movement by providing additional thrust points, the 
behavior is termed obstacle‐aided locomotion [ 13, 14]. Heckrott et al. [ 13] showed that 
the speed of serpentine locomotion depends on the density of these thrust points in the 
environment. However, this gait is ineffective on very smooth or very narrow surfaces 
and for short‐bodied snakes, which cannot conform to the desired curvature.
Another specialized mode is the rectilinear drum-organ gait, in which segments of the 
body alternately anchor and advance (Fig.  1b). Although slower and less efficient due 
to static friction and momentum changes, this gait allows snakes to traverse extremely 
confined spaces such as pipes, wires, and branches [ 15, 17]. Jayne et al. [ 18] further sub -
divided drum-organ locomotion into four types—flat, tunnel, alternating tree-like, and 
spiral tree-like—highlighting its adaptability in environments where other gaits fail [ 19].

Page 3 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
Another well‐known snake gait is rectilinear locomotion, a slow peristaltic motion 
in which the skin advances relative to the underlying skeleton (Fig.  2). Marvi et al. [ 20] 
analyzed the body‐shape changes and muscle mechanics underlying this gait, demon -
strating that forward propulsion arises from alternating contractions and relaxations of 
the rib muscles attached to the elastic skin [ 21, 22]. During each cycle, snakes maintain 
full‐body contact with the ground: the abdominal skin pulls forward, drawing the ven -
tral scales together, then presses downward so that the scales grip the substrate. Once 
anchored, the rest of the body is drawn forward over the fixed skin until the next cycle 
begins. This mode requires only minimal vertical displacement, making it especially 
effective in narrow tunnels and low‐clearance environments [ 23, 24].
2.2 Research on the path-planning algorithm
Robot path planning has long stood as a cornerstone challenge in robotics [ 25–27]. At 
its core, the problem requires a robot to compute an optimal or near-optimal trajectory 
from a given start to goal location, balancing criteria such as path length, smoothness, 
safety margin, and computational efficiency. In mobile platforms, effective planners not 
only reduce traversal time and energy consumption but also minimize mechanical wear 
and operational costs [ 28].
Over the years, a rich spectrum of planning methods has emerged. Graph-based 
search algorithms—epitomized by A*—guarantee optimality on discretized maps but 
often ignore turning costs and clearance requirements, leading to convoluted routes. 
To address this, Sang et al. [ 29] augmented A* with a turn-cost term and pruned nodes 
near obstacles, thereby reducing detours and improving safety. Evolutionary approaches, 
Fig. 2  Rectilinear locomotion (above) and trajectory (below) 
Fig. 1  a Transverse wave movement, b Drum and organ movement 

Page 4 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
like Genetic Algorithms (GA), have likewise been enhanced: Thanh et al. [ 30] layered 
Q-learning onto GA—training offline and refining online—to handle dynamic obstacles, 
while Qu et al. [ 31] proposed modified genetic operators to accelerate convergence. Ant 
Colony Optimization (ACO) variants overcome stagnation through dynamic phero -
mone updates [ 32] and adaptive step-size control [ 33], and Particle Swarm Optimization 
(PSO) methods smooth jagged trajectories by introducing fractional velocity control and 
fitting Bézier curves [ 34].
Local reactive planners such as the Dynamic Window Approach (DWA) offer real-
time responsiveness by evaluating admissible velocity commands under kinematic 
constraints. Chang et al. [ 35] further enhanced DWA’s global navigation by embedding 
Q-learning–based weight adaptation. Meanwhile, artificial potential field (APF) frame -
works have been fortified against local minima: Montiel et al. [ 36] merged APF with a 
bacterial evolution algorithm to ensure safe, feasible paths, and subsequent parametric 
APF variants [ 37] delivered provable optimality. Neural-inspired and sampling-based 
techniques have also matured: the Guided Automatic Wave Pulse–Coupled Neural Net -
work (GAPCNN) [ 38] accelerates collision-free queries via directional wave control, and 
reinforcement-learning–augmented RRT methods—such as RL-RRT [ 39] and Q-RRT* 
[40]—bias tree expansion and employ SARSA(λ) or Q-learning to boost initial solution 
quality and convergence speed. The double-tree RRT approach [ 41] further doubles 
efficiency by alternately growing two trees. Deep-RL methods like DQN [ 42] and PPO 
[43] achieve robust end-to-end obstacle avoidance at the expense of extensive training, 
whereas the Sine Resistance Network (SRN) [ 44] overlays sinusoidal impedance modula -
tion for rapid adaptation to external disturbances.
In this paper, we present an improved A* algorithm tailored for multi-joint, serpentine 
locomotion. By embedding turning-cost and curvature constraints directly into the heu -
ristic evaluation and coupling it with a real-time adaptive parameter adjustment mech -
anism, our planner generates smooth, obstacle-safe paths with significantly reduced 
computational overhead. Unlike deep-RL or SRN-based approaches that demand high 
training or sensing resources, our method achieves comparable obstacle-avoidance per -
formance while running efficiently on embedded hardware. This makes it particularly 
suitable for high-degree-of-freedom snake-like robots operating in dynamic, unstruc -
tured environments.
3 Serpentine robot design
3.1 Introduction
We have designed a flexible, bio-inspired robotic snake that mimics natural locomo -
tion via a series of buffer-bone modules and reconfigurable joints. Figure  3a shows the 
schematic of the snake-like skeleton structure, while Fig.  3b illustrates the biological 
snakeskin pattern we emulate. We analyzed biological snakes’ locomotion mechanics—
specifically how ventral scale friction combined with alternating muscle contractions 
generates forward propulsion. Motivated by these insights, we developed a robotic pro -
totype featuring (1) multiple serially connected joints for serpentine bending, and (2) a 
high-friction outer skin to maximize traction. By coordinating joint actuation, the robot 
can perform a variety of complex, snake-like gaits.

Page 5 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
3.2 Spentine robot connection structure
In this study, we evaluated four joint -connection schemes for snake-like robots—pris -
matic–revolute (P–R), universal, parallel, and orthogonal—each offering different 
trade-offs in degrees of freedom, mechanical complexity, cost, and motion performance. 
Ultimately, we selected the orthogonal connection for our prototype’s joint modules for 
three key reasons. First, its three mutually perpendicular links minimize part count, 
weight, and fabrication difficulty, unlike P–R and parallel linkages, which require extra 
components or only enable planar motion. Second, the 90° axis arrangement perfectly 
decouples pitch and yaw, making it ideal for generating smooth, continuous serpentine 
trajectories; it also reduces dynamic coupling compared to universal joints, thus enhanc -
ing posture stability and predictability. Third, the orthogonal layout simplifies control: 
pitch and lateral bending can be modeled independently, which streamlines parameter 
tuning and directly supports our proposed self -adaptive control- parameter adjustment 
strategy. By contrast, P–R linkages—two prismatic joints separated by a revolute hinge 
(Fig.  4)—achieve full 3D motion but at the cost of a bulkier three-link assembly, and the 
Fig. 4  P–R connection 
Fig. 3  Schematic diagram of the biological snakes 

Page 6 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
parallel connection is limited to two-dimensional motion and so is not considered fur -
ther here.
The P–R (Prismatic–Revolute) joint-based design for the snake robot aims to simplify 
the joint mechanism by employing a single motor for actuation. However, this configura -
tion requires a minimum of three interconnected links per joint module, which signifi -
cantly limits the robot’s ability to maneuver in confined spaces. Consequently, this type 
of connection is rarely adopted in the field of snake-like robots.
In contrast, the universal joint structure consists of a minimum unit formed by two 
links. As illustrated in Fig.  5, the spherical joint between Link A and Link B allows 
full 360-degree rotation in three-dimensional space, offering greater flexibility and 
compactness.
The universal joint connection is theoretically an ideal configuration for snake robots, 
as it offers the highest degree of flexibility and enables effective simulation of three-
dimensional gaits. However, the joint unit design is structurally more complex and 
requires multiple motors for actuation. The motor control system is also highly coupled, 
making real-time coordination difficult. As a result, the universal joint connection is not 
widely adopted in practical snake robot designs.
Fig. 5  Universal joint connections 

Page 7 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
The orthogonal joint connection, on the other hand, features a minimal unit composed 
of two joints formed by three links, as illustrated in Fig.  6. Link A is connected to Link 
B via a vertical rotational axis, while Link B and Link C are connected through another 
rotational axis that is perpendicular to the first. This arrangement ensures that adjacent 
rotational axes are orthogonal to each other. The orthogonal joint utilizes a three-link 
orthogonal hinge structure, which is both mechanically simple and easy to control. It 
supports common three-dimensional locomotion patterns while minimizing structural 
and control complexity.
The snake robot adopts a structurally simple connection scheme based on orthogonal 
joints, each actuated by a single motor. This configuration offers ease of control, high 
stability, and the ability to support most common gait patterns. The orthogonal connec -
tion structure is illustrated in Fig.  7. In this design, the rotational axes of adjacent joints 
are perpendicular to each other (e.g., the Z-axes in the O1 and O2 coordinate systems), 
while the rotational axes of non-adjacent joints are parallel but oriented in opposite 
Fig. 7  Orthogonal connection diagram of joint module 
Fig. 6  With orthogonal connections 

Page 8 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
directions (e.g., the Y-axes in the O1 and O3 coordinate systems). This orthogonal layout 
contributes to smoother and more stable locomotion of the snake robot.
Figure  8 presents the solid prototype of the robot, which comprises 11 joints, provid -
ing a total of 11 degrees of freedom.
Because this paper primarily focuses on the winding locomotion of the snake robot, a 
driven wheel structure is integrated into the design to facilitate ground movement and 
improve overall mobility.
3.3 Joint module of the snake-shaped robot
The overall structure of the snake-shaped robot consists of a series connection of the 
head module, body joints, and tail joint. In designing a practical and reliable joint mod -
ule, it is essential to consider not only the structural stability but also the selection of 
sensors and the motion control strategy. This section provides a detailed introduction to 
each type of joint module, presents their corresponding simulation models developed in 
SolidWorks, and describes the construction of a physical prototype of the snake robot.
3.3.1 Head joint module
As the "eye" of the snake-shaped robot, the snake head joint module is positioned at the 
front end of the robot body. Its simulation model and physical prototype are shown in 
Fig.  9. The front part of the module adopts a semi-arc curved surface design, while the 
rear part features a cylindrical structure. This design provides sufficient internal space 
to house various sensors. A square cavity at the rear is reserved for installing a servo 
gear, which primarily drives the pitch motion of the head joint in the vertical direction. 
Additionally, a driven wheel structure is integrated into the design to ensure smoother 
Fig. 9  Design of the snake head joint module 
Fig. 8  Proposed prototype of snake robot 

Page 9 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
locomotion during winding movements. The sensor suite mainly includes a camera and 
a Wi-Fi communication module, which enable real-time interaction with the host sys -
tem and transmission of control signals to the joints. Furthermore, the head joint can 
be extended with additional sensors to enhance environmental perception and support 
adaptive obstacle avoidance capabilities.
1) Camera
The design of the camera is located in the middle of the head joint, can get the good 
vision in the robot operation, its main function is when the snake in the process of run -
ning robot can collect external information, and the information back to the computer, 
the operator according to the corresponding information control, so as to realize a 
closed loop data communication. The camera model is OpenMV4 Cam H7 Plus, with 
5 million pixels and an adjustable resolution ranging from 320 × 240 to 2560 × 1600, the 
processor is STM32H743II ARM Cortex M7 processor, the working voltage is 5 V, all 
pins can withstand 5 V voltage, output voltage is 3.3 V, all pins can provide up to 25 mA 
pull current or irrigation current, the camera is shown in Fig.  10a).
2) Wireless WIFI communication module
The snake robot uses a wireless WiFi communication module to interact with the host 
computer. The WIFI module is WINC1500, the working voltage is 5  V, and can work 
in the temperature – 40 to 85 ℃. The WiFi module expansion board is 36 mm * 27 mm 
in a variety of application scenarios with long operating life; and mild temperatures for 
long hours; The extension board allows OpenMV connection to the Internet and the 
OpenMV camera controls the module using a firmware module. The WIFI communica -
tion module entity is shown in Fig.  10b).
This WiFi extension module can be stacked with the above OpenMV camera, saving 
space for the snake head joint module. The WiFi extension board turns the OpenMV 
into a Web Cam, and through the WiFi extension board you can transfer JPEG com -
pressed images to the browser.
3.3.2 Snake body joint module
As the primary source of propulsion for the snake robot, the body joint module con -
tains the largest number of joints. These modules are further categorized into two types: 
Fig. 10  The sensor used in the snake head joint module is a physical image 

Page 10 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
wheel-equipped modules and non-wheel modules, as illustrated in Fig.  11. Structur -
ally, both types adopt a U-shaped frame combined with a cubic column design. The key 
distinction between them lies in the presence or absence of a driven wheel. Depending 
on specific task requirements, an appropriate number and type of joint modules can be 
selected to optimize performance and reduce control complexity.
From the previous introduction, it can be seen that the no-wheel module and the 
snake body joint module are orthogonally connected, as shown in Fig.  12, for the actual 
robot or actual robot snake body joint module. This connection mode is convenient for 
the handling of the steering gear in the actual robot or actual robot and the remaining 
space for the wiring arrangement.
Each whorless joint of the robot is equipped with a serial bus steering machine, 
which is responsible for driving the rotation between the joints and providing forward 
power for the robot. The serial bus steering gear used is RP8-U45-M, effective angle 270 
degrees, position resolution 4096, torque 45  kg cm/7.4  V, working voltage 6.0–8.4  V, 
communication wave rate 9600–500 Kbps, tooth ratio 273:1, weight 73  g, and size 
40 mm * 40 mm * 20 mm. The actual serial bus steering gear is shown in Fig.  13.
As shown in the table above, the servo motor used in this study is a serial bus servo. 
It employs a single-wire half-duplex asynchronous serial communication protocol and 
operates at TTL voltage levels. Each servo features interfaces on both sides, allowing 
multiple servos to be connected along a single serial bus.
Fig. 12  Actual robot or actual robot and snake body part 
Fig. 11  Design of the snake body joint module 

Page 11 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
Figure  14 illustrates the communication diagram of the serial bus servo system. In this 
setup, the servo must be used in conjunction with a dedicated control board, which con -
verts the servo’s single-wire UART interface into a dual-wire TTL interface—comprising 
an Rx (receiving) and Tx (transmitting) line. This dual-line TTL interface allows com -
munication with a microcontroller unit (MCU), or alternatively, with a PC via a USB-to-
TTL converter chip such as the CH340.
3.3.3 Introduction of the snake-tail joint module
As a critical structural and storage unit of the snake robot, the tail joint module is 
located at the rear end of the robot body. It houses several key components, including 
the STM32 control board, the servo drive board, and a lithium battery. To accommodate 
these components, the tail module is designed with sufficient internal space.
The simulation model and physical prototype of the tail joint module are shown in 
Fig. 15. The STM32 control board is mounted centrally within the cylindrical body of the 
joint, while the lithium battery is positioned at the bottom. The overall structural design 
of the joint remains consistent with the other modules, utilizing a U-shaped cylindrical 
configuration.
Raspberry PiPC
Arduino
STM32Main
Controller0x12 0x4c 0x01 0x01 0x03 0x63
0x05 0x1c 0x01 0x01 0x03 0x26Adapter
Board
Fig. 14  Communication diagram of serial bus servo actuator 
Fig. 13  Physical diagram of serial bus steering gear 

Page 12 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
1) STM 32 control board
The control board used in the snake robot designed in this study is STM 32 based multi-
functional main control board, as shown in Fig.  16. This board integrates several key 
components, including the STM32F103C8T6 microcontroller (minimal system board), 
a servo motor driver board, a TTL/USB conversion module, dedicated interfaces for 
OpenMV and laser sensors, serial communication interfaces, and a 4 + 2 key input mod -
ule. This high level of integration significantly reduces assembly space and simplifies the 
control architecture.
As the "brain" of the snake robot, the main control board is primarily responsible for 
receiving data from external sensors (such as the camera), analyzing and processing the 
incoming data, and subsequently issuing control commands to the servo driver board. 
The servos then execute the commands to achieve coordinated motion control of the 
entire snake robot.
2) Lithium cell
The snake-shaped robot designed in this study is powered by a lithium-ion battery pack. 
The batteries are connected in series, providing a total voltage of 7.4 V, which can be 
directly connected to the power input port of the STM32 multi-functional main control 
board. This setup enables simultaneous power supply to both the main control board 
and the servo motors.
Laser
InterfaceSerial 
InterfaceServo
Interface
OpenC V
Dedicated 
Interface
STM32
Breakout 
Interface
Power
Interface Switch4+2 Button 
ModuleMicroUSB
Interface
Fig. 16  Physical diagram of STM 32 multi-one master control board 
Fig. 15  Design of tail joint module 

Page 13 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
The specific battery model used is XP08002ECO, which is a rechargeable 2S lithium 
power battery. It has a capacity of 800 mAh, a nominal voltage of 7.4 V, and dimensions 
of 65 mm × 25 mm × 13.5 mm. The battery supports a maximum continuous discharge 
rate of 25C and a maximum continuous current of 20A.
3.4 Overall introduction of the serpentine robot
From the introduction of the joint module in the previous section, the serpentine robot 
designed in this paper is mainly divided into snake head joint, snake body joint and 
snake tail joint, which are connected and assembled through orthogonal series. The 
overall control process of the snake-shaped robot is shown in Fig.  17. First, the camera 
and various sensors transmit the collected image data to the STM 32 multi-integrated 
master control board and to the upper computer through the wireless WIFI module. As 
the core of the main control system, it sends the control instructions to the joint module 
servo steering gear according to the data received, so as to realize the specific motion 
gait of the snake-shaped robot. At the same time, each joint servo rudder transmits the 
state data during the operation process to the upper computer, and the upper computer 
receives the picture transmitted by the camera as shown in Fig.  18. The operator can 
monitor the running state of the snake robot in real time through the upper computer.
This paper the design of the snake robot entity shell mostly made of 3D printing, driven 
wheel bearings and the connection shaft part using metal material, to reduce the quality 
of the actual robot or actual robot, the whole actual robot or actual robot is composed 
of 11 joint modules, modules through 10 orthogonal joints, a total of 11 degrees of free -
dom, the specific number of joints can be according to the actual demand. The length 
of the robot is 720 mm, the diameter is 62 mm, and the net weight is 1.8 kg. The shell 
material is yellow-green toughness photosensitive resin, with high cost performance, 
Fig. 18  Return image of the snake robot head camera Fig. 17  Schematic diagram of the overall control process of the snake-shaped robot 

Page 14 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
relatively smooth surface detailed performance, and hardness and toughness are better 
than white resin. In addition, the overall simulation model of the robot and the physical 
machine are shown in Figs.  19 and 20.
4 Analysis of the serpentine locomotion of the serpentine robot
In nature, biological snakes have various forms of motion, which derived a variety of 
bionic snake-like robots. This chapter mainly analyzes the classic Serpentine locomo -
tion of serpentine robots, and first establishes the kinematic model of orthogonal joints. 
Then, the theoretical analysis of the snake robot and the dynamic simulation in ADAMS. 
Finally, the Serpentine locomotion control function is further analyzed and optimized to 
provide a reference for the subsequent snake robot path planning.
4.1 Kinematic model of the serpentine robot
The orthogonal connection structure of the snake robot is relatively complex. However, 
the size of each joint during movement does not significantly affect the overall posture. 
To simplify the kinematic modeling of the snake robot, this paper abstracts the robot as 
a spatial linkage mechanism and employs the D-H parameter method. The essence of 
D-H parameter method is to describe the relative pose between adjacent links through 
the coordinate transformation matrix, and then multiply these matrices to obtain the 
coordinate position of each joint of the snake robot in the base coordinate system, so as 
to establish the robot kinematic model.
4.1.1 D-H parameter method
The two basic coordinate transformations mainly used by D-H parameter method are 
translating homogeneous coordinate transformation and rotating homogeneous coordi -
nate transformation.
Fig. 20  Physical object of the snake robot 
Fig. 19  Overall simulation model of the snake-shaped robot 

Page 15 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
1. Translation of the homogeneous coordinate transformation
As shown in Fig.  21a), there are two coordinate systems and coordinate {A} systems 
{B} with {B} the same attitude {A} but APBORG  different origin in space {B}, and P 
the position BP of the coordinate system relative to the coordinate P system can be {A} 
used AP to represent. In the coordinate system, the position of the point is expressed 
as, because the two vectors have the same attitude, the vector of the point relative to the 
coordinate system can be calculated as follows:
AP=BP+APBORG  (1)
Set in the coordinate {A} system, there is a point along the axis X, Y, Z direction move -
ment of APBORG =(a, b, c )T a, b, c, i. e., the above mentioned Eq. ( 1) equation can be 
rewritten as:
AP=T rans(a, b, c)BP (2)
Equation ( 2) is equivalent to Eq. ( 1), Trans is the translation transformation, and Trans 
(a, b, c) is the translation homogeneous matrix shows in Eq. ( 3):
T rans (a, b, c)=
100 a
010 b
001 c
0001
 (3)
2. Rotate the homogeneous coordinate transformation
As shown in Fig.  21b), there are two coordinate systems and coordinate {A} systems 
{B} with different A
BR poses but {B} overlapping origins {A} in space, and {B} usually 
P the rotation matrix BP is used to represent {A} the AP position of the coordinate 
system relative to the coordinate system. In the coordinate system, the position of the 
point is expressed as, and then the vector of the modified point relative to the coordinate 
system can be obtained from the rotation Eq. ( 4).
AP=A
BRBP (4)
When a point in space is a rotation transformation relative θ to the coordinate axis x, 
y, and z, their Rot(x, θ),Rot(y, θ),Rot(z, θ) rotational homogeneous coordinate transfor -
mation is represented as follows:
Fig. 21  Schematic diagram of the coordinate transformation 

Page 16 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
Rot(x, θ )=
10 0 0
0 cos θ−sinθ0
0 sin θ cosθ 0
00 0 1
 (5)
Rot(y, θ )=
cosθ 0 sin θ0
0 100
−sinθ0 cos θ0
0 001
 (6)
Rot(z, θ )=
cosθ−sinθ00
sinθ cosθ 00
0 0 10
0 0 01
 (7)
4.1.2 Kinematic modeling of serpentine robots
In this paper, the D-H parameter method is used to model the orthogonal serpentine 
robot. Because the serpentine robot can run freely and the end is not fixed, the base 
frame system can be selected when establishing the D-H coordinate system. As O0 
shown in Fig.  22, the established O 11 joint orthogonal snake robot Z D-H coordinate 
system is X shown. Except for the base coordinates Y, the origin of the other coordinate 
system is set at the middle point of the joint rotation axis, the joint rotation axis, the cen -
tral axis of the joint, and the other axis is determined by the right hand rule.
According to the D-H parameter method, each link parameter is defined as follows:
1. Angle of the θi joint: the corner of x the axis z of two adjacent rods.
2. Offset distance of di the rod: the offset z distance of the axis di=0 of the two adjacent 
rods, here.
3. Length of the ai rod: the distance perpendicular to the two rotating joint axes.
4. The torsion Angle αi of the rod: the axis zi−1 of zi the two adjacent joints and the 
angle of the length direction of the αi=π
2 rod, apparently for the serpentine robot 
here.
The terminal position of the snake robot can be obtained by the changes determined 
by each rod, and the transformation of each rod can be calculated by the homogeneous 
coordinate transformation matrix determined by the D-H parameter, where the homo -
geneous coordinate transformation matrix includes:
(1) Turn around z the θi axis, and the corresponding homogeneous coordinate 
transformation rectangle is:
Fig. 22  D-H coordinate system of 11-joint orthogonal connection snake robot 

Page 17 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
T1=
cosθi−sinθi00
sinθicosθi00
0 0 10
0 0 01
 (8)
(2) Let the xi−1 length of the link moving l along the direction be, and the corresponding 
homogeneous coordinate transformation rectangle be:
T2=
100 l
0100
0010
0001
 (9)
(3) Around xi−1 the rotating αi−1 torsion Angle, the corresponding homogeneous 
coordinate transformation rectangle is:
T3=
10 00
0 cos αi−sinαi0
0 sin αicosαi0
00 01
 (10)
The homogeneous i coordinate transformation ii+1 matrix of the first joint relative to 
the first joint can be multiplied by the above three matrices:
iTi+1=T1·T2·T3 (11)
D-H parameters:
iTi+1=
cosθi−sinθi·cosθ sinθi·sinαi l·cosθi
sinθicosθi·cosαi−cosθi·sinαil·sinθi
0 sinαi cosαi 0
0 0 0 1
 (12)
Among αi=π
2 them, substitute it to obtain:
iTi+1=
cosθi0 sin θi l·cosθi
sinθi0−cosθil·sinθi
01 0 0
00 0 1
 (13)
Multi homogeneous coordinate transformation matrix of a series of rods to obtain the 
total transformation matrix from the base mark, and the D-H parameters are shown in 
Table  1.
0Tn=0T1·1T2···n−1Tn (14)
4.2 Theoretical analysis of the winding movement of the snake robot
The main purpose of studying the winding movement of a serpentine robot is to achieve 
precise control. To achieve this goal, reasonable kinematics or dynamics models are 
Table 1  D-H parameters
i αi−1 ai−1 di θi
1π
20 θ1
2π
20 θ2
··· ··· ··· ··· ···
10π
20 θ10

Page 18 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
needed according to the structure of the robot. In kinematic modeling, there are two 
main ways. One is to abstract the robot structure into the link structure, which has been 
introduced in the previous section, and the other is to build a motion model based on 
morphology. In this section will make theoretical analysis of the winding movement of 
the snake robot based on this method.
4.2.1 Serpenoid serpentine curve
Through long-term observation of the locomotion patterns of biological snakes, Profes -
sor Hirose from Japan proposed the Serpenoid curve in 1972, which can effectively rep -
licate the winding movement of real snakes. The Serpenoid curve, also known as the 
snake curve, has since become a widely used trajectory model in snake robot research. 
When combined with a driven wheel structure, the movement of the snake robot closely 
resembles that of a biological snake. As a result, many researchers have adopted the Ser -
penoid curve for motion control in snake robots and have achieved promising results.
The curvature equation of the Serpenoid curve is defined in Eq. ( 15):
ρ(s)=2Knπα0
Lsin(2Knπ
Ls)
 (15)
where it α0 is the initial bending angle Kn of the Serpenoid curve; the number of "S" L 
waves transmitted by the Serpenoid s curve; the length of the snake robot; and the dis -
placement of the snake robot on the Serpenoid curve.
To facilitate the study, the following formula is rewritten:
ρ(s)=−absin(bs)+c  (16)
where, a=−α0 is b=2Knπ
L the c initial curvature of the snake curve.
By integrating the above curvature Eq. ( 16), the deflection angle equation of the head 
joint module relative to the winding direction is presented in Eq. ( 17):
θ(s)=∫
−absin(bs)+cds =acos(bs)+ cs (17)
A Cartesian coordinate transformation is available for the above in Eq. ( 18):


x=s∫
0cosθdσ
y=s∫
0sinθdσ (18)
The θ=acos(bσ)+cσ  is another representation of the Serpenoid serpentine curve in 
the Cartesian coordinate system.
Because of the actual snake robot is composed of multiple rigid joint modules con -
tinuously, and not like Serpenoid snake curve for continuous change, so this requires the 
Serpenoid snake curve segment dispersion processing, the snake robot body approxi -
mate fit to Serpenoid snake curve, and the length of each section should be consistent 
with the snake robot joint module length.

Page 19 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
If the length of each joint module of the snake robot is the same, L and the overall 
length of the snake robot L
n is, then the length of each joint (xi,yi)(i=0,1,···,n) mod -
ule of the snake robot is, and the coordinate at the intersection of each joint is, which is 
also the interpolation point of the serpentine curve. The Eq. ( 19) can be discretized:


xi=i∑
k=1L
ncos[
acos(
bkL
n)
+ckL
n]
yi=i∑
k=1L
nsin[
acos(
bkL
n)
+ckL
n] (19)
This shows 1∼n the following relationships between the joint modules in Eq. ( 20):
yi−yi−1
xi−xi−1=sin(
acos(ibL
n)
+icL
n)
cos(
acos(ibL
n)
+icL
n)= tan(
acos(ibL
n)
+icL
n)
= tan( θi) (20)
From Eq. ( 20) is available to Eq. ( 21)
θi=acos(ibL
n)
+icL
n (21)
In the actual motion control process of the snake robot, the rotation of each joint mod -
ule is driven by the servo steering gear, so the relationship is required to control the 
winding movement of the snake robot. From Eq.  ( 21), the Angle of each joint is pre -
sented in Eq. ( 22):
φi=θi+1−θi=2asin(bL
2n)
sin(bL
ni+bL
2n)
+cL
n (22)
4.2.2 Serpentine motion control function
Serpenoid Snake curve is used to represent the movement of the robot, the actual move -
ment of the servo steering gear according to the change of time the output of different 
Angle, so you need to introduce ω the time parameter to rewrite the Angle formula, set 
the servo steering output angular speed, the formula (3.22) into the joint Angle rewrite 
about the function of time change, namely the Serpentine motion control function, 
rewrite:
φi(t)= Asin(
ωt+(
i+1
2)
k)
+γ (23)
where, A=2asin(bL
2n)
 it k=bL
n is γ=cL
n the φi angle i between the i+1 first joint 
module ω and the first module; it is the angular speed of the servo wheel rotation.
In view of the various motion modes of orthogonally connected to the snake robot, 
and to facilitate the study of the subsequent Serpentine locomotion gait, the motion 
control function of each joint angle of the snake robot can also be expressed as:
θi=Aisin(ωt+ki)+γi (24)
In: rudder i number; the i=1 ,2···n rotation i θi angle of the first servo rudder ω; rota -
tion angle speed; amplitude Ai; time t variable, motion k control parameter γi and joint 

Page 20 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
angle offset. The motion control function has few control parameters, so the snake robot 
by choosing different control parameters.
4.3 Simulation analysis of snake robot
4.3.1 Snake-shaped machine simulation modeling based on ADAMS software
ADAMS is a widely used virtual prototype analysis software in the field of product 
design and manufacturing. It provides comprehensive functions for modeling, simula -
tion, and visualization. With ADAMS, static, kinematic, and dynamic analyses of vir -
tual mechanical systems can be performed efficiently. Moreover, ADAMS serves as a 
versatile platform for virtual prototype development and supports secondary develop -
ment for specialized simulation applications. The software is composed of several func -
tional modules, including the core module, extension modules, interface modules, and 
domain-specific modules. These components make ADAMS a powerful and flexible 
tool capable of meeting the modeling and simulation needs across various engineering 
domains.
4.3.2 Simulation of the snake-shaped robot with serpentine locomotion
The following dynamic simulation of the winding movement of the snake robot is con -
ducted through the Serpentine motion control function. Because the winding movement 
is a two-dimensional motion, only the corner of the yaw joint needs to be set during the 
movement, and all the pitch joints are set to zero value. According to the snake robot 
model established in this paper, the joint is numbered from 1, where the odd number is 
the pitch joint and the even number is the yaw joint, then the gait control function of the 
snake robot is:
{
θi=Aisin ( ωt+ki)+γi, i =2,4..., k ̸=π
2
θi=0,i=1,3,5··· (25)
θi(t)={
Aisin(ωt+φi)+γi,i=1,3,5,...,
0, i=2,4,6,... (26)
It is the ω rotation speed of the servo rudder machine Ai, k, γi, which is the fixed 
value, and the parameter is the gait control parameter. The change of value deter -
mines the overall shape of the snake robot. To study the control effect of motion con -
trol function for snake robot, this paper introduced the snake robot model in ADAMS 
and ADAMS, as the research object, set the centroid coordinate of the snake of the 
head as (0,0), compared the control variable method, and set the comparison experi -
ment simulation motion time t= 10 s. Before the comparison experiment, the control 
ω=0.8,A =1,k=1,γ=0 parameters are selected, set the simulation motion time 
t= 30 s, and generate the Serpentine locomotion path of the five yaw joints in the x−z 
plane through the ADAMS post-processing module, as shown in Fig.  23.
As can be seen from Fig.  24, the motion control function can realize the basic gait of 
the snake robot, namely the sinusoid wave attitude. When the snake-shaped robot is just 
started from a neutral position, there will be a certain degree of joint shaking. Later, the 
snake-shaped robot can swing forward according to the periodic curve, and the adjacent 
joints are separated by the same phase difference, which also verifies the rationality of 
the snake-shaped robot modeling.

Page 21 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
When the control Ai, k, γi parameters take different values, the motion shape of the 
snake robot is different. The three control parameters are compared A and analyzed in 
the following simulation ω=0.8,k =1,γ=0. First A=0.6,0.8,1, the influence of 
the control parameter value on the snake robot is studied, fixed, selected in turn, and 
the corresponding motion control function is input into the model, and the simulation 
results are obtained as shown in Figs.  25 and 26.
From the above simulation results, we can see that in the meandering gait, for the 
control parameter A, the larger the A value, the larger the amplitude of the oscillation 
Fig. 25  Simulated gait of different control parameters A of serpentine locomotion gait 
Fig. 24  Simulation results of snake robot five-joint serpentine locomotion path 
Fig. 23  ADAMS 11-joint snake robot simulation model 

Page 22 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
amplitude of the A value, the smaller the A value, the smaller the oscillation amplitude, 
but the amplitude does not affect the number of waveforms.
Subsequently, the influence k of the control parameter value ω=0.8,A =1,γ=0 on 
the snake k=0 .6,0.8,1 robot was studied, fixed, selected in turn, and the correspond -
ing motion control function was input into the model, and the simulation results were 
obtained as shown in Figs.  27 and 28.
From the simulation results, we observe that in the winding motion gait the control 
parameter k inversely affects the path length within a fixed time: larger k values pro -
duce shorter travel distances, while smaller k values yield longer paths. Therefore, 
Fig. 28  Influence of control parameter k on snake-like robot under meandering gait 
Fig. 27  Simulated gait for different control parameters k of serpentine locomotion gait 
Fig. 26  Influence of control parameter A on snake-like robot under meandering gait 

Page 23 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
k should not be set too low. Finally, the influence γ of the control parameter value on 
ω=0.8,A =1,k=1 the snake robot γ=−0.2, 0,0.2 is studied, fixed, selected in turn, 
and the corresponding motion control function is input into the model, and the simula -
tion results are obtained as shown in Figs.  29 and 30.
From the above simulation results, it can be seen that in the γ Serpentine locomo -
tion gait, the value γ affects the bias of the waveform, which can play a role in changing 
the direction of the serpentine robot in the actual control. The similar gait control func -
tion of traveling wave motion is shown below, which is mainly realized by controlling the 
periodic motion of odd pitching joints. In this paper, mainly the Serpentine locomotion 
gait is studied, which is not over described here.
θi(t)={
Aisin(ωt+φi)+γi,i=1,3,5,...,
0, i=2,4,6,... (26)
Here, the odd‐numbered joints (i.e.i=1,3 ,5,... ) perform the pitch oscillations that 
drive vertical undulation, while the even‐numbered joints remain at zero angle in this 
phase to facilitate independent yaw control.
In Eq. ( 26), each amplitude Ai sets the peak deflection of the corresponding pitch 
joint, and the common angular frequency ω governs the temporal speed of the sinusoi -
dal wave. The phase offset φi allows adjacent joints to be arranged with a constant phase 
lag, ensuring a smooth, traveling‐wave pattern along the robot’s body. A bias term γi can 
be added to shift the entire oscillation up or down if asymmetrical behavior is desired. 
By coordinating these pitch oscillations with a complementary yaw‐joint control law, the 
robot realizes a continuous three‐dimensional serpentine locomotion, balancing path 
smoothness, propulsion efficiency, and stability in complex environments.
Fig. 30  Effect of control parameters under winding γ motion gait on snaking robot 
Fig. 29  Simulation gait with different control parameters of meandering γ gait 

Page 24 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
Through the Serpentine motion control function, the winding movement of the snake 
robot can be basically realized in different environments. To make the winding move -
ment gait form more diversified, it is improved and optimized combined with other 
functions. For example, in practice, if you want to achieve the snake robot, the swing 
amplitude at some joint modules is different, or the swing amplitude can gradually 
change between different joint modules. The Sigmoid function is introduced to improve 
the Serpentine locomotion control function. The traditional Sigmoid function expres -
sion is as follows:
S(x)=1
1+e−x (27)
To control the slope of the Sigmoid curve and the number of joint modules that change 
the amplitude, Eq. ( 27) is modified as follows:
S(i)=1
1+e−a(n−b) (28)
where the parameter a can control the slope of the b rising phase of the curve, the 
parameter can control n the number of joints with restricted amplitude, for the number 
of the current joint module. Combining Eqs. ( 25) and ( 28), the control function of the 
modified meandering moving gait based on the Sigmoid function is as follows:
θi=1
1+e−a(n−b)Asin(ωt +ki)+ε, i =2,4,6, ..., k ̸=π
2 (29)
Below analyze the a influence of control parameters on snake robot, select b=4 
improved control parameters A=1,ω=0.8,k=0.8,ε=0, select traditional 
a=0 .1,0.5,0.8 control parameters, select improved control parameters, input the 
corresponding motion control function model, the simulation gait results as shown in 
Fig.  31, to visually show the improved control function on the amplitude of the joint 
module, select the joint module and snake joint module as the research object, and gen -
erated by the ADAMS post-processing module is shown in Fig.  32.
From the above simulation results, the improved gait control function can change the 
amplitude of the joint a module. When the other parameters remain the same, the larger 
the a value, the greater the value, the greater the swing amplitude of the module, and the 
smaller the swing amplitude of the module a.
The following paper b analyzes the influence of the control parameters on a=0 .5 
the snake robot, selects A=1,ω=0.8,k=0.8,ε=0 the improved control b=4 ,6,8 
Fig. 31  Improving the simulated gait under different control a parameters of the serpentine locomotion gait 

Page 25 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
parameters, selects the traditional control parameters, selects the improved control 
parameters successively, inputs the corresponding motion control function into the 
model, and obtains the simulation gait results as shown in Fig.  33.
From the above simulation results, it can b be seen that the improved control param -
eters mainly affect the number b of restricted joint modules of the snake robot. When 
the other parameters remain unchanged, the larger the value, the more the number of 
restricted joint modules, which is not driven by the restricted joint module according to 
the normal Serpentine motion control function. The improved Serpentine locomotion 
gait can realize the swing amplitude of the snake robot from snake head to snake tail, 
which can reduce the shaking of the head camera module and enhance the stability of 
image acquisition.
4.4 Analysis and optimization of the serpentine locomotion control function
In the actual motion control of a snake robot, the motion path is typically predefined, 
and the robot's movement is then controlled accordingly using motion control func -
tions. Therefore, it is essential to analyze the relationship between the control functions 
and the resulting body configurations of the snake robot.
This section first investigates the correlation between the motion shape of the winding 
gait and its control parameters. It then establishes a fitting function that describes the 
relationship between these motion shape parameters. The derived function serves as a 
theoretical reference for subsequent research on path planning for snake robots.
Fig. 33  Simulated gait under different control parameters b of improved meandering gait 
Fig. 32  The meandering movement a path of the snake head and the snake tail joint module under different 
control parameters 

Page 26 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
4.4.1 Fitting method of common data
The classification of data fitting methods depends on the type of data and the target of 
fitting. The commonly used fitting methods are linear fitting, nonlinear fitting, polyno -
mial fitting, curve fitting, least squares fitting, data smoothing, parameter estimation, 
etc., the above methods are briefly introduced below.
① Linear fit
 For data with linear relationships, linear fitting methods, such as linear regression, 
can be used. Linear fits can be used to establish the rectilinear relationships between 
the variables, for example by fitting the data to a straight line by least squares. Of 
course, linear fitting also has its limitations, such as the inability to handle nonlinear 
relationships and the sensitivity of outliers. In practical application, the applicability 
of using linear fitting should be considered comprehensively according to the 
characteristics of the data and the fitting objectives.
② Polynomial fit
 For data with nonlinear relationships, polynomial fitting methods such as polynomial 
regression can be used. Polynomial fitting can be adapted to more complex data 
patterns by increasing the number of polynomials. Choosing the appropriate 
polynomial number is a key problem in polynomial fitting, and too low times may 
not capture complex patterns in the data, while too high times may cause overfitting. 
Methods such as cross-validation are usually used to select the best polynomial 
number.
③ Curve-fitting
 If the data shows a curve shape, you can use the curve fitting method. This includes 
fitting the data using curve models (e. g., exponential function, log function, power 
function) or non-parametric methods (e. g., interpolation by spline interpolation). 
It provides a flexible way to adapt the curve shape of the data and can be used for 
applications of prediction, interpolation, smoothing, etc. In practice, a suitable 
curve model or a non-parametric method is selected for fitting analysis based on the 
characteristics of the data and the fitting target.
④ Least square fit
 Least squares fit is a method to fit the data by minimizing the residual sum of squares 
between the observed values and the fitted model, which can be used for both linear 
and nonlinear fits. It provides a basis for establishing the relationship between the data 
and the model, and can be used in tasks such as prediction, inference, and association 
analysis. However, least squares fitting also has its limitations, such as sensitivity 
to outliers and inability to handle nonlinear relationships. In practical applications, 
comprehensively considering the characteristics of the data and fitting objectives are 
needed to determine the applicability of using least squares fitting.
⑤ Parameter estimation for fitting
 Parameter estimation fitting is a method of fitting the data by estimating the model 
parameters. It is based on the form of the assumed model and determines the value 
of the parameters by minimizing the difference between the observed values and 
the fitted model. In practice, appropriate parameter estimation methods need to be 
selected according to the characteristics of the data, model form and fitting target.

Page 27 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
In this study, since we are fitting the cosine wave shape of the winding motion path 
under various control parameters—and the data exhibit a clear curved relationship while 
requiring both computational efficiency and fitting accuracy—we preferentially employ 
a second-degree polynomial fitting. This approach accurately captures variations in 
amplitude and frequency without the risk of overfitting associated with higher-degree 
polynomials. For the subsequent mapping between control parameters and path shape 
parameters, the quadratic polynomial fit also yields errors that remain within an accept -
able range.
4.4.2 Analysis and optimization of serpentine locomotion control function
The gait control function of the snake robot is presented in Eq. ( 30):
{
θi=Aisin ( ωt+ki)+γi, i =2,4..., k ̸=π
2
θi=0,i=1,3,5··· (30)
It determines k Ai the shape of the snake robot and controls the direction γi of the speed 
of the snake ω robot.
When the control parameters of different k A combined values are taken and differ -
ent. Following A=0.8,ω =1,k=1,γ=0 four A=1,ω=1,k=0.6,γ=0 con -
trol A=1.2,ω =1,k=0.8,γ=0 parameters A=0.6,ω =1,k=0.8,γ=0, set the 
ADAMS simulation motion time t = 20 s, and the position coordinate of the head center 
of the snake robot is (0,0). With the snake head module as the research object, the move -
ment path of the snake robot in the set time is shown in Fig.  34.
Figure  34 shows that the Serpentine locomotion path of the snake robot resem -
bles a positive cosine wave. The control parameters ω and A determine the amplitude 
and angular frequency of this wave. To establish the relationship between the control 
parameters and the shape parameters, curve fitting is applied to the winding path data 
obtained under different parameter groups. Polynomial fitting is then used to derive 
the functional relationship between the control and shape parameters, enabling the 
snake robot to follow the desired motion trajectory. Specifically, the coordinate values 
of the Serpentine locomotion path are extracted and fitted using trigonometric func -
tions to obtain the motion path shape parameters. The control parameters are set as 
A=0.8,ω =1,k=1,γ=0. The ADAMS simulation is run for 10  s, with the center 
coordinate of the snake robot's head at (0,0). The simulation results of the Serpentine 
locomotion path are shown in Fig.  34. Using the ADAMS post-processing module, the 
relevant data for the Serpentine locomotion path are extracted. To ensure accuracy in 
Fig. 34  Serpentine locomotion path under different control parameters 

Page 28 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
subsequent curve fitting, data corresponding to one full positive cosine wave cycle—
excluding the initial jitter and deviation—are selected. These coordinate data are then 
exported in TXT format. The TXT file is imported into MATLAB, where the data are fit -
ted using a custom function in the MATLAB curve fitting toolbox. The form of the fitted 
function is presented in Eq. ( 31).
y=Aωsin(ωx+a)+b  (31)
The fitting effect of each parameter is shown in Fig.  35. Since the values of parameters a 
and b only affect the translation of the curve in the coordinate system of the curve, but 
does not affect A=0.8,ω =1,k=1,γ=0 the specific shape of the function curve, the 
shape parameter of the Aω= 23 .38mm, ω =0.0327rad/s  orthogonally connecting the 
Serpentine locomotion path of the snake robot under the control parameter is.
The above fitting process is repeated, and the values A of k the shape parameters of the 
control motion path of Aω different ω groups are shown in Table  2.
② By the expected motion Aω path ω shape parameters k A and determine the control 
parameters shows in Figs.  36, 37.
As can be seen from the correspondence Table  2, the correspondence between 
these two control parameters is unique, so as long as there are enough sample data as 
in Table  2, Aω the expected ω motion A k path shape parameter and the fitting func -
tion between the corresponding parameters can be solved by the method of polyno -
mial fitting. Using the polynomial fitting method in the MATLAB curve fitting toolbox 
and selecting the binary fitting method, the polynomial is found that the quadratic Table 2  A, k  and Aω,ω corresponding relationships
A k Aω/mm ω/rad ·s−1
0.8 1 23.38 0.0327
0.9 0.8 38.23 0.0222
1 0.6 69.16 0.0163
1 0.9 34.86 0.0282
1.1 0.7 58.26 0.0202
1.2 0.8 50.33 0.0255
Fig. 35  MATLAB curve fitting results 

Page 29 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
polynomial is enough to meet the fitting requirements. The final fitting function and the 
three-dimensional space of the fitting are as follows:
A=P1+P2Aω+P3ω+P4A2
ω+P5Aωω+P6ω2 (32)
k=C1+C2Aω+C3ω+C4A2
ω+C5Aωω+C6ω2 (33)
where the parameter Pi,i=1,2···6 values Cj,j=1,2···6 for the optimized sum are 
shown in Table  3.
Through the Eqs. ( 32) and ( 33), the value of the corresponding control parameters and 
A can k be obtained after given the desired winding path curve, and then the Serpentine 
locomotion control function can control the snake robot to move according to the pre -
determined trajectory.
The analysis and research of the winding movement of serpentine robot, first con -
structed the snake robot motion model using the D-H method, and then analyzed the 
theory of winding movement, the motion simulation through ADAMS, analyzed the 
Fig. 37  Control parameters and k fit Aω,ω three-dimensional space 
Fig. 36  Fitted 3 D space A of Aω,ω control parameters vs 

Page 30 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
influence of the snake robot, and combined with the Sigmoid function related improve -
ment. Finally, the relationship between the motion control parameters and the motion 
path shape parameters is optimized and the function equations between them are given, 
which provides a reference for the size of the control parameter value by setting the 
shape of the path planning of the serpentine robot.
5 Serpentine locomotion path planning based on the modified A * algorithm
Path planning has long been a popular research topic and is widely applied in areas such 
as robot navigation, autonomous driving, logistics and transportation, unmanned aerial 
vehicles (UAVs), and aerospace engineering. With the rapid development of intelligent 
systems, path planning algorithms have evolved rapidly, resulting in a growing diversity 
of algorithmic approaches.
In the field of mobile robotics, path planning algorithms are relatively mature. How -
ever, general-purpose algorithms are not directly applicable to snake robots due to their 
unique locomotion characteristics. Therefore, traditional path planning strategies must 
be adapted to accommodate the serpentine gait and the requirement for smooth, con -
tinuous curved paths.
In this study, the path planning method for the snake robot begins with an introduc -
tion to the traditional A* algorithm and its simulation implementation. Subsequently, 
improvements are proposed to meet the specific needs of serpentine path planning. 
Finally, a co-simulation model combining ADAMS and MATLAB is constructed to ver -
ify the effectiveness and rationality of the improved A* algorithm.
5.1 Principles of the traditional A * algorithm
The A * (A-star) algorithm is a heuristic search algorithm commonly used for graph 
search and path planning. It is more efficient in finding the shortest path from the start -
ing point to the end point, and it is guaranteed to find the optimal solution. The A * algo -
rithm combines the breadth first search of Dijkstra algorithm with the idea of heuristic 
function. It calculates the cost of each extended node through the evaluation function, 
retains the node with the minimum cost, and then continues to search down from it 
until the search reaches the end point. The general expression of the evaluation function 
is:
F(n)= G(n)+H (n) (34)
For the current n node, for the G(n)  true cost from the n beginning to H(n) the node, 
and n for the estimated cost from the node to the final point.
Function H(n) plays a crucial role in the A * algorithm, and the key to finding the 
shortest path H(n) lies in the choice of estimating the cost function. If these are not Table 3  Parameter values after optimization
parameter Optimize the value parameter Optimize the value
P1 − 0.5405 C1 0.3223
P2 0.01384 C2 − 0.00135
P3 42.97 C3 34.95
P4 − 0.0001123 C4 − 0.000000163
P5 0.5253 C5 − 0.09762
P6 − 673.2 C6 − 333.7

Page 31 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
considered in the selection process, it is difficult X(n) to n find a solution that meets the 
path H(n) requirements and minimized the cost. Assuming that we represent the true 
distance between the final point, the selection is roughly three cases:
① If the H(n)<X (n) estimated distance H(n) is less than the true distance, the 
extended range of the algorithm A * is large, but the optimal solution can be found.
② If H(n)>X (n) the estimated distance H(n) is greater than the true distance, 
the extended range of the A * algorithm is less, but the optimal solution cannot be 
guaranteed.
③ If H(n)=X(n) the estimated distance H(n) is equal to the real distance, the search 
process of the A * algorithm will be carried out by the shortest path, which is also the 
most efficient.
The common H(n) measures of functions mainly include Manhattan distance, diagonal 
distance and Euclidean distance. The three measures are calculated as follows:
① The Manhattan distance is the distance between the two points in the direction 
of the x-axis of the distance (xi,yi) plus (xj,yj) the distance in the direction of 
the y-axis. Assuming that the coordinates of the start point, and the final point are 
respectively, the Manhattan distance is calculated as:
D(i, j)=|xi−xj|+|yi−yj| (35)
 When the mobile robot only moves in the east, west, south and north directions on 
the map, it can be chosen H(n) as a function. The schematic diagram of Manhattan 
distance is shown in Fig.  38.
② Diagonal distance is to allow the node to move along the diagonal. So that in the 
process of movement, the node can move diagonal, horizontally and vertically 
to reach the destination (xi,yi) position (xj,yj). Assuming that the coordinates 
of the start point, and the final point are respectively and, the diagonal distance 
calculation formula is:
D(i, j)=√
2(|xi−xj|+|yi−yj|)+(|xi−xj|+|yi−yj|−2min(|x i−xj|,|yi−yj|)) (36)
 When the mobile robot can not only move in the x and y direction but also move 
in the diagonal direction in the map, it can choose the H(n) diagonal distance as a 
measure as a function. The diagonal distance diagram is shown in Fig.  39.
Fig. 38  A Schematic diagram of the Manhattan distance 

Page 32 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
③ Euclidean distance refers to the straight-line distance between two points. It is the 
shortest distance among the three measurement methods, but (xi,yi) the (xj,yj) 
calculation amount of the algorithm is large. Assuming that the coordinates of the 
starting point and the final point are respectively and, the calculation formula of 
Euclidean distance is:
D(i, j)=√
(xi−xj)2+(yi−yj)2 (37)
 When the mobile robot can travel along any Angle in the map, it can choose the 
H(n) euclidean distance as a function of the measurement.
A * algorithm has A variety of search methods, the commonly used search four domain 
search and 8 search two, in order to ensure the subsequent planning winding path curve 
is more obvious, this paper adopts 4 field search way G(n) , namely H(n) in the map 
of up and down four directions, so the Manhattan distance as A function and function 
value, their function expression is as follows:
G(n)= |xn−xstart|+|yn−ystart| (38)
H(n)=|xgoal−xn|+|ygoal−yn| (39)
In: the (xn,yn) current node coordinate (xstart ,ystart ), the starting point (xgoal,ygoal ) 
coordinate, and the final point coordinate.
A * Detailed steps of the algorithm are as follows:
①  Put the start point as the first point to be expanded into the Open List (the Open List 
is a list of squares to be expanded).
②  Place the four neighboring squares around the start point into the Open List and set 
their parent node to the start point.
③  Remove the start point from the Open List and place the start point into the Close 
List (the Close List is a list that stores no checking boxes).
④  Calculate the estimated local function F(n) value of the neighboring squares.
⑤  Select the square with F(n) the smallest value a from the Open List and repeat the 
third step.
⑥  Check a all adjacent and feasible squares:
1) Do not consider the obstacles and the squares in the "close list";
Fig. 39  Diagonal-distance diagram 

Page 33 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
2) If the a neighboring squares are not in the Open List, add them to the Open List, 
calculate the value of F(n) the squares, and set their parent a node to;
3) If an adjacent square is b already in the "open list", calculate the value of the new a 
path after b reaching F(n) the square from the start point;
 Comparing the value F(n) of the new path with the old path to determine whether 
it needs to be updated. If the total a cost of the F(n) new H(n) path is lower, 
modify the parent node and calculate the value does not change because the 
estimated F(n) cost of the square reaching the final point is fixed; if the total cost 
of the new path is high, the value does not change.
⑦ Repeat the fifth and sixth steps, and so the cycle.
⑧ End Judgment:
1) When the final square appears in the Open List, the path has been found;
2) When there is no data in the Open List, the path does not exist.
⑨ The start point, the nodes in the Close List, and the final point are successively 
connected to obtain the global path planned by the A * algorithm.
The specific flow chart of the A * algorithm is shown in Fig.  40.
5.2 Environment modeling and simulation experiment of the traditional A * algorithm
Since the A* algorithm requires a known map environment for path planning, a simu -
lation map must first be constructed before conducting A* algorithm experiments. To 
facilitate map construction, this study adopts the grid-based method to build the A* sim -
ulation environment. The grid method divides the robot’s planning area into multiple 
cells based on predefined rules. These grid cells are adjacent but non-overlapping, effec -
tively partitioning the space into sub-regions and improving the feasibility and efficiency 
of algorithm development.
Moreover, the resolution of the grid directly affects the planning results: lower resolu -
tion reduces computation but may sacrifice accuracy, while higher resolution improves 
precision at the cost of increased computational complexity. In path planning research, 
the grid method is typically used as an environment modeling technique rather than as a 
standalone planning algorithm. It is intended to be used in conjunction with other plan -
ning algorithms to support path planning studies.
In this paper, MATLAB is used to construct the grid map and conduct simula -
tion experiments. The grid map is set to a size of 20 × 20, with an obstacle ratio of 0.3. 
Obstacles are represented by randomly generated black squares. The starting and ending 
points are also randomly placed on the grid, with the starting point marked as a green 
circle and the target point marked as a red five-pointed star. An example of the gener -
ated grid map is shown in Fig.  41.
In the 20 * 20 size grid map constructed above, the traditional A * algorithm is used for 
simulation experiments, and the simulation results are shown in Fig.  42.
Gray area in the figure for A * algorithm search area, the deeper the color means the 
number of repeated search, you can see the traditional A * algorithm search range is 
larger, lead to lower efficiency, at the same time planning more path redundancy corner, 

Page 34 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
path smooth, so this paper through A series of optimization measures to improve the 
defects in the traditional A * algorithm.
5.3 Improve the A algorithm
The traditional A * algorithm has simple principles and has the advantages of complete -
ness and strong adaptability. If there is A feasible solution, A * algorithm can find the 
solution. Even in complex graphics, if the path connects the starting point and the end 
point, A * algorithm can find the path. However, due to the limitation of the mechanism 
of the algorithm itself, the path planned by A * algorithm has some disadvantages, such Fig. 40  Flow chart of the A * algorithm 

Page 35 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
as A large search range, more redundant corners, and not smooth enough path. In this 
section, the traditional A * algorithm is improved for these shortcomings to realize the 
planned path to meet the Serpentine locomotion requirements of the snake robot.
5.3.1 Improvement of the heuristic function formula
From the principle of A * algorithm, we can see that the H(n) core of A G(n)* algorithm 
is the enlightening function, and as the cost of the starting point to the current node, its 
value is generally fixed H(n). Therefore, the choice of enlightening function in the pro -
gramming of the A * algorithm is particularly important. The relationship between the 
enlightening function and the actual cost has the following cases:
① Is H(n) equal to zero: the A * algorithm has evolved into the Dijkstra algorithm, and 
the result is guaranteed to find the shortest path.
② Less H(n) than the actual H(n) cost: the smaller, the more squares extended by the A 
* algorithm, the shortest path can be found, but the operation speed is slower.
Fig. 42  Simulation results of the A * algorithm 
Fig. 41  Grid diagram of 20*20 specifications 

Page 36 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
③ Equals H(n) to the actual cost: strictly follow the best path to expand the square, 
the most efficient, the result ensures that the shortest path can be found, and the 
operation speed is faster.
④ Greater H(n) than the actual cost: the result is not guaranteed to find the shortest 
path, but the operation speed is faster.
⑤ Far H(n) more than the actual cost: the A * algorithm evolved into the BFS algorithm, 
the result cannot guarantee to find the shortest path, but the operation is very fast.
According to the above cases, if it H(n) is too low, although the shortest path can be 
found, but the H(n) search speed is reduced; if it is too high, the search speed is G(n) 
accelerated H(n) and the shortest path is abandoned. In practice, any weight can be 
changed to achieve the desired search effect of the algorithm.
Therefore, in order to effectively reduce the search range and improve the search effi -
ciency, the H(n) weight is changed H(n) by increasing the additional weight coefficient. 
If the weight is reduced, the A * algorithm tends H(n) to extend to the point near the 
beginning, rather than the grid point near the final point. On the contrary, if the weight 
is increased, the A * algorithm tends to expand to the final point direction, which is more 
enlightening. The evaluation function of the improved A * algorithm is:
F(n)= G(n)+w ·H(n) (40)
Is the weight w coefficient H(n) of the heuristic w≥1 function. Usually, the w A * algo -
rithm can search for the target point by changing the size of the weight coefficient. The 
simulation experiment results before and after the improvement of the heuristic func -
tion are shown in Fig.  43.
From the simulation results, the search efficiency and speed of A * algorithm have 
been improved by changing the coefficient weight, and the improved algorithm is more 
enlightening. However, with the decrease of w the expansion points, the path it finds 
may not be the shortest path, so the weight coefficient needs to be flexibly adjusted 
according to the requirements in actual operation.
Fig. 43  Simulation results before and after the improvement 

Page 37 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
5.3.2 Redundant corner optimization
It can be seen from the above simulation results that the traditional A * algorithm has 
too many corners when conducting A path search based on the Manhattan distance as 
the measurement unit.
As shown in the red box selection area of Fig.  44, functions can be used to optimize 
the path shown by the blue line in the figure, so that multiple unnecessary corners can 
be reduced. Of course, this paper does not optimize all corners. If it is found that the 
cost of a corner optimization becomes greater, the corner is not optimized, but only the 
corner at the same cost.
The specific steps of corner optimization are as follows:
① First need to get before the corner optimization of the original expansion of the parent 
grid marked value and location information, that is to get the point L is extended by 
which point, if the direction information is, said the current point is extended by the 
left point, namely the marked value of n the parent grid is minus the value of each line 
the length of each column, so the other three location information processing method 
is similar.
② Before the calculation for expected to go the next point value, need to judge the parent 
in the parent value is equal to the starting point, if equal to the starting point is that 
the point is expanded by the starting point, its extension in all directions are straight 
lines, then skip the optimization, into the next step.
③ Use the marked value of the parent grid obtained in the first step to view the direction 
information of the parent grid, and use the direction information to calculate the 
marked R value of the point expected to go in the next step. For example, if the direction 
of the parent square storage information is, then the parent square is extended by the 
point on the n right, now if you want to go straight line, then the expected point is 
the point on the left of the parent square, then expect to go point mark value is on the 
basis of the parent square minus, and the other three direction processing method is 
similar to this.
Fig. 44  Schematic diagram of unoptimized corners 

Page 38 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
④ Calculate the labeled values for the new points to be expanded. If the point intended 
to expand is the expected straight point, skip the optimization; if the expected point 
can be found in the "open list" in the matrix, but skip the optimization; if the expected 
point is an obstacle or beyond the boundary; if the point expected to go is at the cost 
of the point before the optimization.
In order to verify the effectiveness of redundant corner optimization on A * algorithm, 
the simulation experiment was conducted, and the results before and after the optimiza -
tion are shown in Fig.  45.
From the simulation results, it can be seen that through the optimization of redun -
dant corners, the number of path corners planned by the A * algorithm is significantly 
reduced, and the path is more smooth. Of course, some paths still have redundant cor -
ners, but the appropriate number of corners for the snake robot winding path planning 
is conducive to the formation of the winding path.
5.3.3 Path smoothing processing
Traditional A * algorithm using what way of search, the planning path will be peak and 
broken line, to enhance the comfort of the robot running, need to smooth planning path, 
this paper for planning path respectively Bessel curve and gradient descent two meth -
ods, by comparing the optimization effect of the two methods which method can meet 
the serpentine robot winding path planning requirements.
① Introduction to the Bessel curve.
Bessel curve is a parametric curve representation method, widely used in fields such as 
graphic design and path planning. The curve is represented by the start, stop, and con -
trol points, where the control point determines the shape of the curve. And the param -
eter equation of Bessel curve is defined by the control point. N + 1 control point can 
define N times polynomial curve, and the parameter equation of Bessel curve is:
P(t)=N∑
iPiBi,N(t)t∈[0,1] (41)
Fig. 45  Simulation results before and after redundant corner optimization 

Page 39 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
where: is p(t) the t coordinate of the Pi next i point, is the P0 coordinate Pn of the first 
vertex Pi, and Bi,N(t) are the starting point and end point respectively, for the control 
point; is Bernstein polynomial, defined as:
Bi,N(t)= Ci
Ntk(1−t)N−i (42)
where: Ci
N it is the binomial coefficient. The first order and second order Bessel curve 
shapes are shown in Figs.  46 and 47, where the parameter t = 0.85.
For the same reason, we can obtain the parameter equation of the Bessel curve of 
order 3 as follows:
P(t) = (1 −t)3P0+3t(1−t)2P1+3t2(1−t)P2+t3P3t∈[0,1] (43)
The Bessel curve of order 3 is shown in Fig.  48, where the parameter t = 0.85.
As shown in the P0 figure above, P3 it is the starting P1,P2 point of the curve, the end 
point of the curve, and the control point of the curve, which jointly determine the overall 
shape of the curve.
② Introduction of the gradient descent method
For example, if A is at the top of A peak, and if A wants to reach the lowest point of the 
peak as soon as possible, how then A can reach the lowest point as quickly as possible.
The fastest way is to base the current position and move in the steepest direction of 
that position. After moving for a distance, continue to move in the steepest direction 
Fig. 47  Second-order Bessel curve 
Fig. 46  First-order Bessel curve 

Page 40 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
based on the current position, repeat the process all the time, and finally A can reach the 
lowest point.
On the one hand, consider how to position the steepest direction, on the other hand, 
consider how many distances to relocate the direction after each move. The first prob -
lem is to calculate the degree ∇Jθ of "steep", which is the gradient, which is α a vector 
used J to represent θ. Solve the second moving θ1 distance problem, J with the repre -
sentative moving distance. It's about the function, assuming that A is at the beginning, 
the minimum point to move from this point, which is the lowest point of the mountain. 
First of all, we need to determine θ2 α the direction of advance. Since the direction of the 
gradient is the direction of the function at one point, the direction of the fastest descent 
rate is the opposite direction of the gradient, that is, the direction of the fastest descent, 
after a distance to reach the point. The expression is as follows:
(θi=θi−1−α×∇Jθ(θi−1) (44)
Iterate according to the above expression θ, constantly update the value until conver -
gence θ, and when the gradient at θ the lowest point is zero, the value stops updating. 
The coordinate point corresponding to the obtained value is the position of A. As shown 
in the schematic Fig.  49, starts represents the starting point of the path planning, end 
represents the end point of the path planning, the blue line is the path planned by the 
A * algorithm, and the green line is the path optimized by the gradient descent method.
To verify the optimization effect of the two path smoothing methods, their simula -
tion experiments were performed, and the optimization results were compared with the 
paths planned by the traditional A * algorithm. Maps a and b were randomly generated 
by Matlab, and the simulation results are shown in Fig.  50. The black line is the original 
path planned before A * algorithm, the red line is the path optimized by Bessel curve 
method, and the pink line is the path optimized by gradient descent method.
As shown in Fig.  51, compared with the gradient descent method, the path planned 
using the B-spline curve method is smoother. However, the B-spline path is more prone 
to intersecting with obstacles, and the winding characteristics of the trajectory are less 
pronounced. In contrast, the gradient descent method produces a path that more closely 
follows the initially planned trajectory, with clearer curvature and reduced likelihood 
Fig. 48  Bessel curve of order 13 

Page 41 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
Fig. 51  LOWESS local weighted regression smoothing simulation results 
Fig. 50  Simulation result of path smoothing processing 
Fig. 49  Schematic diagram of gradient descent method optimization 

Page 42 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
of contacting obstacles, making it more suitable for the winding path requirements of 
snake robots.
Nevertheless, the path generated by the gradient descent method may still lack 
smoothness. To further enhance path smoothness, noise reduction techniques are 
employed. Common smoothing methods include the moving average (movmean), 
median filter (movmedian), low-pass filter, Gaussian filter, Savitzky-Golay filter (sgolay), 
and Locally Weighted Scatterplot Smoothing (lowess).
In this study, MATLAB’s built-in smoothdata function is used to denoise and smooth 
the optimized path. As shown in Fig.  52, methods such as Gaussian filtering, Savitzky-
Golay filtering, and lowess smoothing all achieve good results. Taking lowess as an 
example, this method performs local weighted regression near each data point, assign -
ing higher weights to points closer to the target and lower weights to distant ones. It is 
often used to estimate smooth curves from noisy data. The lowess method is applied 
to smooth the paths planned on Map A and Map B, and the simulation results are pre -
sented in Fig.  53.
The black line in the figure is the original path planned before smoothing by the A * 
algorithm, the pink line is the path optimized by gradient descent, and the green line is 
the path reprocessed by lowess local weighted regression. It can be seen that after fur -
ther processing, the path smoothness is obviously improved, which is conducive to solv -
ing the problem of path planning with farther distance, and also meets the requirements 
of the Serpentine locomotion path of the snake robot. We prove the effectiveness of this 
algorithm.
5.3.4 System performance assurance mechanism analysis
To ensure the overall performance of the snake-like robot during path planning and 
execution, this study incorporates several key mechanisms across both the planning and 
motion control stages, as detailed below:
Fig. 53  Create the input variable 
Fig. 52  Block diagram of the joint simulation of ADAMS and MATLAB 

Page 43 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
First, during the path planning phase, the improved A* algorithm introduces a heuris -
tic function with adjustable weights to effectively guide the search process toward the 
target point and reduce unnecessary node expansion. Compared with the traditional A* 
algorithm, this approach significantly narrows the search space, improves planning effi -
ciency, reduces overall computational resource consumption, and enhances the system’s 
real-time responsiveness.
Second, to accommodate the unique requirements of continuity and smoothness in 
the serpentine locomotion of snake-like robots, this study applies redundant corner 
optimization and path smoothing on the initially planned trajectory. Specifically, the 
redundant corner optimization algorithm eliminates unnecessary turning nodes, effec -
tively reducing the frequency of curvature variation. On this basis, a combination of gra -
dient descent and LOWESS (Locally Weighted Scatterplot Smoothing) is used to further 
refine the path, generating a more continuous and natural trajectory curve that ensures 
stable and efficient motion in real-world environments.
In addition, at the motion control level, this study leverages the Serpenoid curve the -
ory to establish a functional mapping between joint control parameters and path shape 
characteristics, enabling adaptive adjustment of control parameters. By dynamically tun -
ing key parameters of serpentine motion—amplitude, wavelength, and phase offset—the 
snake-like robot can maintain joint motion synchrony and overall stability while track -
ing the planned path, thereby avoiding posture instability caused by abrupt local path 
changes.
Through the integration of these mechanisms, the proposed method not only improves 
path planning efficiency and smoothness, but also enhances the dynamic stability of the 
physical snake-like robot during execution via adaptive control parameter mechanisms, 
thereby achieving robust overall system performance assurance.
5.4 Joint simulation of ADAMS and MATLAB
To verify the rationality of the improved A * algorithm in the path planning of the ser -
pentine robot, the simulation experiment is conducted. In this section, the joint simula -
tion model is first built through ADAMS and MATLAB, and then the joint simulation 
experiment is conducted on the planning path involved.
5.4.1 Construction of the joint simulation model
To perform more complex and detailed dynamic simulations, ADAMS and MATLAB 
are integrated using a co-simulation approach. Data exchange between the two plat -
forms is achieved through a dedicated API interface, allowing ADAMS functions to be 
directly invoked within the MATLAB environment. In this setup, MATLAB sends the 
servo angle control data to ADAMS, which in turn feeds back the resulting joint angles 
of the servos to MATLAB. This interaction forms a complete closed-loop control system.
The co-simulation principle is illustrated in Fig.  51.
The joint simulation operation of ADAMS and MATLAB joint simulations is mainly 
implemented by Simulink. In Simulink, the integration of ADAMS and MATLAB can be 
performed using Simulink-ADAMS joint simulation toolkit or other similar tools. These 
tools provide direct graphical interface and functions for setting parameters of joint sim -
ulation, establishing simulation model, setting solver, defining simulation time and step 

Page 44 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
length, etc. In addition, oscilloscope module is usually used as display module to display 
curves or data of simulation results in real time.
In the simulation analysis of the snake robot Serpentine locomotion in the previous 
chapter, we have established the snake robot virtual prototype model in ADAMS, but 
with ADAMS alone Serpentine locomotion gait simulation is different through the 
ADAMS and MATLAB joint simulation need to determine the input variables and out -
put variables of the snake robot virtual prototype model. The input and output variables 
correspond to the status variables set in the ADAMS unit, with a total of 12 status vari -
ables, and 10 are set as the input variables. As shown in Fig.  53, the input variables corre -
spond to the rotating drive added by the VARVAL function in the snake-like robot servo 
rudder, and to directly reflect the winding path of the snake robot. 17, the relative dis -
placement of the center of the module on the plane x–z is associated with the two output 
variables. The input variables are transferred from MATLAB into ADAMS and serve as 
the output of the Simulink control system block diagram. The output variable is returned 
from ADAMS to MATLAB and used as input to the block diagram of the Simulink con -
trol system to form a closed-loop control loop (shows in Fig.  54).
To ensure a fair comparison and reproducibility, each planning method is executed 30 
times on the same environment map, thereby mitigating the effect of random fluctua -
tions. For each run, path length, planning time, and smoothness metric are recorded; the 
mean and standard deviation over 30 trials are then computed to capture the stability 
and variance of each algorithm’s performance.
Ten start–goal pairs ( Pj,Gj) (j=1 ,...,10) are randomly generated on the map in 
advance. All algorithms use the same ten pairs; each pair is tested three times, yielding 
30 experiments in total. This setup guarantees that each method is evaluated on identi -
cal planning tasks.
After setting the basic variables and related parameters, although ADAMS software 
provides some basic controller and optimization algorithm, but is not flexible and 
powerful in the control and optimization of complex system, so we need to export the 
mechanical system, combined with the MATLAB snake robot control system output 
control instructions transmitted to ADAMS mechanical model, the mechanical model 
simulation data feedback to the control system, for a new round of cycle.
Open the imported mechanical system model in MATLAB, first run the M file of the 
exported mechanical system, then run the adams_sys.slx file in the file and jump to the 
Simulink module to get the ADAMS mechanical system model, as shown in Fig.  55, 
Fig. 54  Create the output variable 

Page 45 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
where the Adams _ sub module is the mechanical system module imported in Simulink, 
as shown in Fig.  56, including 10 input variables, two output variables and the MSC Soft -
ware mechanical system model.
In this paper, the serpentine robot 3 d model has 11 joints driven by ten servo gear, and 
corresponding to ten input variables, after setting the relevant parameters, build control 
system in Simulink, mainly composed of input signal module, mechanical system mod -
ule and output oscilloscope module, and then based on the joint simulation experiment 
of path planning.
5.4.2 Joint simulation of the path planning of the serpentine robot
In the last section to improve the A * algorithm has planned the appropriate snake 
robot winding path, and then through the third chapter the fitting function between the 
motion path shape parameters and motion control parameters, can get the planning of 
the corresponding motion control parameters, finally through the Serpentine motion 
control function control snake robot expected path operation.
As shown in Fig.  57, the orange line for the planned winding path, because we plan the 
winding movement in the {A} path planning path is in the coordinate system, and the 
solution of the path shape parameters {B} need coordinate system origin in the start -
ing point {A} of the path, namely the coordinate system {B} established in the figure, 
so need to transform the coordinate system of the coordinate system of the coordinate 
Fig. 56  Mechanical system module imported in ads ams _ sub 
Fig. 55  Snake-shaped robot mechanical system module 

Page 46 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
system to the coordinate system. The coordinate transformation here is two-dimen -
sional coordinate transformation, and its specific transformation method is similar to 
the three-dimensional spatial coordinate transformation involved in the D-H parameter 
method in the previous section.
As can be seen from the planned winding path, the motion curve can be roughly 
divided into variable amplitude path and turning path. A joint simulation experiment is 
conducted on these ω=0.8 two main Serpentine locomotion paths to set the rotation 
speed of servo rudder in the joint simulation.
① Joint simulation experiment of the variable amplitude path
Select the shape Aω= 42 ,ω=0.023  parameters Aω= 26 ,ω=0.019  and the winding 
path curve, according to the fitting function between the path shape parameters and 
motion control parameters A=0.9823,k =0.7983  can A=0.5763,k =0.7824  get 
the control parameters of the winding path for and, set the two path running time are 
10 s, the corresponding program input Simulink model for joint simulation, set the joint 
simulation time is 20 s. Since the data output of the oscilloscope in Simulink is sepa -
rated from the x-axis and z-axis direction, the display is not intuitive enough, so the data 
needs to be integrated. The req file of the simulation results generated after the joint 
simulation are imported into ADAMS, and the data in the x-axis and the direction of the 
Serpentine locomotion path of the joint simulation is shown in Fig.  58.
Fig. 58  Joint simulation results of variable amplitude paths 
Fig. 57  Schematic diagram of the Serpentine locomotion path coordinate transformation 

Page 47 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
It can be seen from the above simulation results that in addition to some jitter when 
starting from the neutral position, the snake robot can make smooth and continuous 
Serpentine locomotion, and realize the amplitude change from large to small in the 
middle.
② Joint simulation experiment of the turning path
Select shape parameters Aω= 42 ,ω=0.023  of winding path curve, the correspond -
ing winding A=0.9823,k =0.7983,γ =0 path control parameters, the program first 
winding path, 8 s after γ=0 .2 change control parameters, the corresponding program 
input Simulink model for joint simulation, set the joint simulation time is 20 s, the same 
after ADAMS processing module turn winding path as shown in Fig.  59.
Can be seen from the simulation results, snake robot in addition to just by the neutral 
position will start some jitter, subsequent to the X axis direction, about a third toward 
the Y axis positive direction, turn after a small excessive according to the original path, 
turn Angle is roughly γ 45 degrees, so can adjust the value of the control parameters in 
winding turning direction and Angle.
Turn the Serpentine locomotion path simulation, with the selected shape 
parameters Aω= 42 ,ω=0.023  winding path curve of the corresponding 
A=0.9823,k =0.7983,γ =0 winding path control parameters γ=0 .2 for the pro -
gram, change the control γ=−0.2  parameters, after 8  s after 8  s, the corresponding 
program input Simulink model for joint simulation, set the joint simulation time is 24 s, 
after the ADAMS processing module of Serpentine locomotion path as shown in Fig.  60.
Fig. 60  Simulation results of the winding path 
Fig. 59  Joint simulation results of the turning path 

Page 48 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
It can be seen from the above simulation results that in addition to some jitter when 
starting from the neutral position, the snake robot can make a smooth and continuous 
winding movement in the future, and can basically return to the original direction after 
two turns in the opposite direction.
5.4.3 Comparative experiments and results discussion
To validate the effectiveness of the proposed method, this section presents a series of 
comparative experiments, in which the traditional A* algorithm, Dynamic Window 
Approach (DWA), and Rapidly-exploring Random Tree (RRT) methods are evaluated 
alongside the improved A* algorithm proposed in this study, under identical snake-like 
robot operating environments.
The evaluation metrics primarily include search time, path length, number of turns, 
path smoothness, and the adaptability of the snake-like robot's locomotion.
In a simulated 20 × 20 grid environment with an obstacle occupancy rate of 30%, the 
start and goal positions are randomly assigned. The simulation results are summarized 
in Table  4.
From the experimental results, it can be observed that the proposed method achieves 
comparable search time to the Dynamic Window Approach (DWA), while significantly 
outperforming it in terms of path length, number of turns, and path smoothness. Specif -
ically, the number of turns is reduced by approximately 27% compared to the traditional 
A* algorithm, and the path smoothness improves by around 16%, effectively mitigating 
the issues of energy consumption and motion instability caused by frequent turning dur -
ing execution.
Furthermore, the planned paths were mapped to serpentine locomotion trajectories of 
the snake-like robot on the ADAMS simulation platform. The results demonstrate that 
the paths generated by the proposed method yield higher consistency and better trajec -
tory tracking stability during actual robot movement, thereby validating the superiority 
and practical applicability of the approach in snake-like robot navigation scenarios.
This section has conducted a comparative analysis between the proposed improved 
A* path planning method and several commonly used path planning algorithms, with a 
particular focus on the motion characteristics of snake-like robots.
First, compared with the traditional A* algorithm, the proposed method introduces a 
weight-adjusted heuristic function, which effectively enhances the goal-directedness of 
the search and significantly reduces redundant node expansion. Additionally, through 
redundant corner optimization and path smoothing, it overcomes the issues of excessive 
turning points and discontinuities commonly seen in standard A* results, thus generat -
ing smoother trajectories better suited to continuous serpentine motion.
Second, in comparison with the Dynamic Window Approach (DWA), the proposed 
method not only considers obstacle avoidance, but also generates globally consistent 
Table 4  Comparative experimental results
Method Search time (s) Path length (number of 
grid cells)Number of turns Smooth -
ness 
Index
TraditA* 2.35 29 18 0.68
DWA 1.97 34 22 0.61
RRT* 3.12 27 21 0.65
Proposed method 1.98 28 13 0.79

Page 49 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
paths with periodic curvature characteristics, which aligns well with the repetitive ser -
pentine motion patterns of snake-like robots. In contrast, DWA is more suitable for 
short-term local obstacle avoidance and often struggles to produce globally smooth and 
continuous paths in complex environments.
Third, compared to sampling-based methods such as RRT*, the proposed method 
offers higher controllability and reproducibility in path planning. Although RRT* per -
forms well in high-dimensional spaces, its strong randomness in path generation and 
tree-like structure often fail to meet the stringent requirements of snake-like robots for 
trajectory continuity and control precision.
In summary, the proposed method not only ensures path safety and feasibility, but 
also significantly enhances trajectory continuity and smoothness. It achieves a bal -
ance between global search efficiency and local path optimization, demonstrating clear 
advantages in supporting the serpentine locomotion of snake-like robots in complex 
environments.
6 Serpentine robot prototype experiment
The theoretical analysis and motion simulation of the snake robot, and the path plan -
ning of the snake robot in the map is realized by improving the A * algorithm. In this 
chapter, the snake robot actual robot or actual robot will be used to test the winding gait, 
to verify the effectiveness of the winding gait. Finally, the actual robot or actual robot 
experiment of path planning and obstacle avoidance, to verify the rationality of the path 
planned by the snake robot.
6.1 Debugging of the software
In the second chapter of this paper has introduced the overall control process, the con -
trol of snake robot only use a central single chip to control multiple external devices, 
simplify the control circuit, the centralized control method can effectively reduce the 
control difficulty of convenient, and writing and entry program, can be real-time debug -
ging in the scene.
Generally speaking, since the snake robot has ten steering gear, and each steering gear 
needs one steering control line, it requires ten independent steering control lines, that is, 
no less than ten steering control ports. In order to reduce the number of steering gear, 
length of the control line and the control program, the serial bus servo steering gear, the 
result is the motion control of the STM 32 multi-one master control board as shown in 
Fig. 61.
Before the experiment of the solid robot, the power limit, power protection limit, cur -
rent protection value, neutral position, upper and lower limit of the angle. This paper 
completes a series of debugging through the servo gear control software. The interface of 
the master control software is shown in Fig.  62.
6.2 Parameter settings and tuning guidelines
To ensure optimal performance of the proposed path planning and motion control 
method in practical applications, this study provides a systematic analysis and summary 
of key parameter selection and tuning strategies, as detailed below:
(1) Heuristic weight coefficient w

Page 50 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
 In the improved A* path search process, the weight coefficient w in the heuristic 
function directly affects both search efficiency and path quality. Experimental 
results indicate that setting w within the range of 1.2–1.5 can achieve a good balance 
between search convergence and path optimality. A lower w may cause excessive 
expansion of the search space and increased computational cost, whereas a higher 
w could compromise the optimality of the path. Therefore, an initial value of 1.3 is 
recommended, with minor adjustments based on environmental complexity.
(2) Serpentine locomotion control parameters α,β
 During serpentine locomotion, the parameters of the sigmoid function that define the 
waveform shape and amplitude are critical. The recommended settings are as follows:
 Amplitude control parameter α: Set initially in the range of 2–3. A larger amplitude 
corresponds to wider serpentine motion, which is more suitable for environments 
with sparse obstacles.
Fig. 62  The control software interface of servo rudder 
Fig. 61  Commissioning of the servo-steering gear 

Page 51 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
 Wavelength control parameter β: Recommended to be set within 0.2–0.5, and 
dynamically adjusted based on the robot's length and the curvature of the target path. 
For smaller robots, a lower β value improves flexibility.
(3) Learning rate for path smoothing (gradient descent).
 In the path smoothing phase, gradient descent is used to optimize the piecewise linear 
path. The learning rate is suggested to be set between 0.05 and 0.1. An excessively 
high value may lead to oscillations in the smoothed path, while a very low value may 
result in slow convergence. In practice, an initial value of 0.07 is recommended, with 
adjustments based on convergence behavior.
(4) Window width for LOWESS smoothing.
 In the second-stage smoothing process, the window width of the LOWESS (Locally 
Weighted Scatterplot Smoothing) method directly impacts the smoothness of the 
resulting curve. It is recommended to set the window width to 10%–15% of the total 
number of path points. For example, if the path contains 100 points, the window 
width should be set to 10–15 points.
6.3 Actual robot or actual robot experiment and simulation results
The snake robot actual robot or actual robot used in this paper has been described 
above, but the object is shown in Fig.  63 Actual robot or actual robot experiments were 
conducted on the Serpentine locomotion gait of the snake robot and the Serpentine 
locomotion gait based on Sigmoid function, and the influence of the motion control 
parameters involved on the Serpentine locomotion gait was analyzed to confirm the 
consistency between the simulation results of the Serpentine locomotion gait and the 
actual robot or actual robot experiment. Finally, the related experiment of planning path 
obstacle avoidance is conducted.
6.3.1 Experimental verification of serpentine locomotion gait
The motor control parameters A, k and γ separately were experimentally 
ω=0.8,k=1,γ=0 verified A=0.6,0.8,1 below. First, the parameters are fixed, and 
the ADAMS simulation results and the movement of the actual robot or actual robot are 
obtained as shown in Fig.  64.
Fig. 63  Serpent robot actual robot or actual robot 

Page 52 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
Fixed parameters ω=0.8,A =1,γ=0 are selected k=0 .6,0.8,1 in turn to obtain 
the ADAMS simulation results and the movement of the actual robot or actual robot as 
shown in Fig.  65.
Fixed parameters ω=0.8,A =1,k=1 are γ=−0.2, 0,0.2 selected successively to 
obtain the ADAMS simulation results and the movement of the actual robot or actual 
robot as shown in Fig.  66.
According to the above experimental results, the k motion control parameter A and 
the swing amplitude and wavelength of the swing gait of the larger k, the larger the 
swing amplitude and the smaller the wavelength γ; the motion control parameter mainly 
affects γ the deflection direction of the winding gait, and the positive and negative val -
ues determine the left and right direction of the deflection of the snake robot.
The following is a actual robot or actual robot experiment on the modified mean -
dering gait based on the Sigmoid function. The improved meandering gait control b a 
function is shown in Eq. ( 28), and different aspects of the modified snake robot mean -
dering b=4 gait are known and controlled respectively A=1,ω=0.8,k=0.8,ε=0 
from the above. a=0 .1,0.5,0.8 First, the improved control parameters are selected, 
Fig. 65  Parameter k takes the experimental results with different values 
Fig. 64  Parameter A takes the experimental results with different values 

Page 53 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
the traditional control parameters are fixed, and the improved control parameters are 
selected in turn. The ADAMS simulation results, and the movement of the actual robot 
or actual robot are shown in Fig.  67.
Select the improved control a=0 .5 parameters, fix A=1,ω=0.8,k=0.8,ε=0 the 
traditional control b=4 ,6,8 parameters, and select the improved control parameters in 
turn, and get the ADAMS simulation results and the motion of the actual robot or actual 
robot are shown in Fig.  68.
According to the above experimental results a, the motion control parameters mainly 
affect a the inhibition effect of the restricted joints, the greater the value, the more obvi -
ous the inhibition b effect, the larger the swing amplitude difference b; the motion con -
trol parameters mainly affect the number of restricted joints of the robot, the larger the 
value, the more the number b of joints.
Fig. 67  Parameter values take a the experimental results with different values 
Fig. 66  The parameter values take γ the experimental results with different values 

Page 54 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
6.3.2 Experimental verification of obstacle avoidance in path planning
From the simulation work γ before known parameters can change the direction of the 
snake robot winding movement γ, so as long as the snake robot movement reasonable 
planning parameter values A=1,k=1,ω=0.8, can realize the snake γ=0 ,−0.2, 0.2 
robot path planning obstacle avoidance movement, select the control parameters, and 
selection of different control parameters to complete the entity machine experiment, 
experimental results as shown in Fig.  69.
It can be seen from the above experimental results that by selecting different control 
parameters, the snake robot avoided the obstacles in front after turning left and turned 
right into the narrow channel again and returned to the original track and direction, and 
Fig. 69  Results of obstacle avoidance experiment of serpentine robot 
Fig. 68  Parameter b values take the experimental results with different values 

Page 55 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
finally gradually drove out of the channel, so as to verify the rationality of planning path 
obstacle avoidance. The snake-shaped robot is mainly used to verify the relevant experi -
ments. This paper first introduces the debugging software of the servo steering gear used 
by the snake robot and then conducts the experiments on the Serpentine locomotion 
gait and the improved Serpentine locomotion gait respectively.
6.3.3 Prototype motion trajectory and posture error analysis
To further validate the practical effectiveness of the improved A* algorithm on a physical 
snake-like robot, this study conducted path tracking accuracy and posture consistency 
tests on a physical prototype platform. A ground marker method was employed: a refer -
ence path was predefined on the test field, with positioning markers placed every 0.5 m 
along the path. The position coordinates and posture angles of the snake-like robot as it 
passed each marker were manually measured, and the corresponding error metrics were 
calculated.
(1) Path tracking error analysis
A comparison between the simulated path and the prototype’s actual trajectory was con -
ducted. The average positional error at each key point is summarized in Table  5.
Based on the measurements, the overall average position error was 0.0594  m. The 
primary sources of error include uneven ground friction and servo delay in the joints. 
Overall, the snake-like robot demonstrated good path tracking capability, with trajectory 
deviations remaining within an acceptable range.
To provide a visual representation of the tracking performance, a comparison plot of 
the simulated and actual trajectories is shown in Fig.  48.
(2) Posture angle variation error analysis
To further evaluate the motion accuracy, the variation of key posture angles—namely, 
pitch and yaw—was measured during the prototype’s movement and compared with the 
simulation results. The comparative data are presented in Table  6.Table 5  Comparison of position errors between simulated and actual paths
Marker ID Simulated position (m) Measured position (m) Position error (m)
1 (0.00, 0.00) (0.02, − 0.01) 0.022
2 (1.00, 0.30) (1.04, 0.28) 0.05
3 (2.00, 0.60) (2.06, 0.62) 0.067
4 (3.00, 0.85) (3.05, 0.89) 0.064
5 (4.00, 1.10) (4.08, 1.15) 0.094
Table 6  Comparison of posture angle variation errors between simulation and prototype
Time(s) Simulated 
pitch angle (°)Measured pitch 
angle (°)Pitch angle 
error (°)Simulated yaw 
angle (°)Measured yaw 
angle (°)Yaw 
angle 
error 
(°)
2 5 5.8 0.8 2 2.4 0.4
4 8 9 1 4.5 5.2 0.7
6 6.5 7.3 0.8 7 7.5 0.5
8 4 4.6 0.6 9 9.6 0.6

Page 56 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
The average errors in both pitch and yaw angles were less than 1°, indicating that the 
physical robot was able to closely maintain the intended posture variation trends during 
execution, thereby exhibiting good trajectory tracking and dynamic stability.
6.3.4 Quantitative analysis of prototype motion experiments
To further validate the feasibility and effectiveness of the improved A* algorithm in prac -
tical snake-like robot locomotion, quantitative tests were conducted on the physical 
prototype platform. The evaluation primarily focused on path tracking accuracy, joint 
control precision, and motion completion efficiency, with comparative analysis against 
simulation results.
First, regarding path tracking accuracy, the robot's motion trajectory data were col -
lected during the experiment and compared with the planned path. The Mean Squared 
Error (MSE) was used as the evaluation metric. The experimental results showed that 
the average MSE between the actual motion trajectory and the planned path was 0.024 
m2, demonstrating that the physical snake-like robot could effectively track the planned 
trajectory, even maintaining high consistency in areas with turns and curvature changes.
Second, for joint control precision, the expected and actual angles of key joints were 
measured during execution. The results are summarized in Table  7.
From the data, it can be observed that the control errors of all joints were maintained 
within ± 3°, meeting the precision requirements for serpentine motion control and veri -
fying the effectiveness of the adaptive control parameter adjustment strategy on the 
physical prototype.
Finally, regarding motion completion time, the average time for the prototype to com -
plete a motion task along the planned path was recorded and compared with the simula -
tion results, as shown in Table  8.
It can be observed that the motion completion time of the physical prototype was 
slightly longer than that of the simulation. The primary causes are variations in ground 
friction and delays in joint actuation. However, the overall error remained within the 
range of 5–6%, demonstrating a high level of consistency between simulation and physi -
cal execution.
In summary, through the analysis of path tracking errors, joint angle control errors, 
and motion completion time comparisons, this study has comprehensively evaluated the 
effectiveness of the improved A* algorithm on the physical snake-like robot platform, Table 7  Statistical results of key joint angle control errors
Joint ID Expected angle range (°) Average control error (°)
Joint 1  ± 15  ± 2.3
Joint 3  ± 15  ± 2.7
Joint 5  ± 15  ± 2.5
Joint 7  ± 15  ± 2.8
Joint 9  ± 15  ± 2.6
Table 8  Comparison of motion completion time between simulation and prototype
Task ID Simulated completion time (s) Prototype completion time (s) Relative error (%)
Task 1 21.3 22.5 5.63%
Task 2 19.8 20.7 4.55%
Task 3 22 23.2 5.45%

Page 57 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
thereby further enhancing the persuasiveness and practical potential of the proposed 
method.
To verify the effectiveness of the system performance assurance mechanisms proposed 
in this study, a series of systematic simulation experiments were conducted based on a 
co-simulation platform integrating ADAMS and MATLAB, focusing on path search effi -
ciency, path continuity, and locomotion stability of the snake-like robot.
First, regarding path search efficiency, a comparison with the traditional A* algo -
rithm shows that the improved heuristic function significantly reduced the search 
space. Experimental data indicate that under the same start and goal settings, the aver -
age search time was reduced by approximately 15%, and the number of expanded nodes 
decreased by about 18%, thereby improving the real-time performance and computa -
tional efficiency of the path planning process.
Second, in terms of path continuity and smoothness, by comparing the path character -
istics before and after redundant corner optimization and smoothing, it was found that 
the number of turns was reduced by 28%, and the curvature variation rate was decreased 
by 22%. As a result, the optimized path became smoother and more continuous, which is 
beneficial for achieving stable serpentine locomotion.
Finally, regarding the locomotion stability of the snake-like robot, simulated experi -
ments based on the Serpenoid curve control strategy were conducted to analyze the 
synchronization between joint angle variations and path curvature changes. The simula -
tion results show that after adaptive adjustment of control parameters, the robot’s joint 
motions could respond in real time to changes in path curvature, with posture fluctua -
tion amplitude controlled within ± 5%, and the root mean square error (RMSE) of path 
tracking maintained below 2.3%, effectively verifying the robustness and precision of the 
motion control system.
In conclusion, the simulation experiments have fully validated the effectiveness of the 
multi-level system performance assurance mechanisms proposed in this study for snake-
like robot path planning and execution processes, providing strong support for subse -
quent physical prototype experiments.
7 Conclusion and future works
This paper focuses on the snake robot design, Serpentine locomotion gait analysis and 
path planning algorithm improvement. First, this paper designed and built an orthog -
onal connection. Then we build the kinematic model based on D-H method, optimize 
the Serpentine locomotion gait, and make the simulation motion analysis with ADAMS 
software. In addition, this paper combines the A * algorithm and various improvements 
to realize the special winding path planning requirements of the snake robot and uses 
ADAMS and MATLAB software for joint simulation. Finally, the snake robot actual 
robot or actual robot is used to verify the correctness and effectiveness of Serpentine 
locomotion gait and improved path planning algorithm. The main work and related 
aspects of this paper are summarized as follows:
(1) The orthogonal connection snake robot designed in this paper is based on the 
modular idea, which consists of snake head, snake body and snake tail joint in series. 
The mechanical structure of each joint module, steering gear, power supply, camera, 
wireless WIFI module and control board and other components are carefully designed 
and selected to ensure the rationality of the overall design of the snake robot.

Page 58 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
(2) In this paper for the winding movement of the snake robot, using D-H method to 
establish the snake robot kinematics model, established the snake robot model in 
ADAMS software, and the Serpentine motion control function and combined with 
Sigmoid function of motion control function improved motion simulation, analysis of 
the control parameters of the influence of the serpentine robot winding movement.
(3) This paper adopts the binary quadratic polynomial fitting method between the 
control parameters and the shape parameters of the motion path. The optimized fit is 
performed, and the functional relationship between them is obtained, which provides 
a theoretical basis for the subsequent study of serpentine robot path planning.
(4) In view of the planning requirements of the Serpentine locomotion path of the 
snake robot, this paper improves the search range of the traditional A * algorithm, 
the number of redundant corners and the degree of path smoothness and finally 
obtains the planning path that meets the requirements of the Serpentine locomotion. 
In addition, this paper uses ADAMS and MATLAB software to establish a joint 
simulation model on the variable amplitude path and turning path involved in the 
Serpentine locomotion path, to verify the rationality of the improved A * algorithm.
(5) In this paper, the correctness and effectiveness of the winding movement gait of the 
snake robot and the path planning obstacle avoidance movement are verified.
In this study, although optimization strategies based on the improved A* algorithm and 
adaptive control parameter methods were proposed to address autonomous path plan -
ning and serpentine motion control of snake-like robots in complex environments, sev -
eral major challenges were still encountered during theoretical derivation, simulation 
validation, and physical prototype implementation:
First, in the path planning phase, balancing path smoothness and obstacle avoidance 
safety remains a significant and complex technical challenge. Overemphasis on smooth -
ness may cause the robot to approach obstacle boundaries, increasing collision risk, 
whereas prioritizing safety margins alone may lead to sharp curvature variations, reduc -
ing the stability of serpentine locomotion. Therefore, dynamic trade-offs between curva -
ture and safety redundancy parameters must be carefully designed in path optimization.
Second, in serpentine motion control, due to the multi-degree-of-freedom and multi-
joint coordinated motion characteristics of snake-like robots, there exists complex 
dynamic coupling between different joints. Achieving synchronized joint angle varia -
tions while maintaining the continuity and stability of the overall posture, especially dur -
ing sharp path curvature changes, requires the motion control system to possess high 
responsiveness and strong adaptive capabilities.
Third, a certain gap exists between theoretical modeling and physical execution. In 
simulations, assumptions such as frictionless surfaces, ideal joints, and perfect path 
tracking are typically made. However, the physical snake-like robot is subject to practical 
limitations including joint actuation precision, link rigidity, and variable ground friction, 
leading to deviations between theoretical predictions and actual performance. Conse -
quently, it is necessary to incorporate fault-tolerance mechanisms into the motion con -
trol strategy and perform multiple rounds of field calibration and parameter tuning to 
achieve the desired path tracking and locomotion stability.
Moreover, this study focused on two-dimensional planar path planning. Extension to 
three-dimensional complex terrains (e.g., slopes, undulating surfaces) remains an area 
for future research. Future work will explore the integration of 3D terrain perception 

Page 59 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
and adaptive trajectory generation techniques to further enhance the environmental 
adaptability of snake-like robots.
In the end, through simulation analysis and experimental verification, the expected 
research results are obtained, and many problems involved in the snake robot are of 
great research value, so the following prospects are made below.
(1) The snake-shaped robot designed in this paper is only equipped with a camera, which 
is mainly used for image information collection, which is convenient for the operators 
to make decisions. It is expected that more sensors can be equipped in the future, to 
improve the functionality of the snake-shaped robot.
(2) In this paper, the path planned by the improved A * algorithm is close to the obstacle, 
which is expected to further improve the algorithm and improve the robustness of the 
algorithm.
(3) The path planning in this paper requires prior map information, and the real-time 
path planning of visual SLAM based on camera or lidar can be realized in the future.
Author contributions
Authors Zhao Guang-hui, and CHENG Wan-sheng are equally contributed for research investigation, conceptualization, 
analysis, methodology, software, validation, funding support, and manuscript draft, and review.
Funding
There is no external funding support for this work.
Data availability
Author declares that data used in this paper is available to this manuscript. Corresponding author will share the data in a 
reasonable request.
Declarations
Ethics approval and consent to participate
Not applicable.
Consent for publication
Not applicable.
Competing interests
The authors declare no competing interests.
Received: 10 March 2025 / Accepted: 18 June 2025
References
1. Hayashi R, Osuka K, Ono T. Trajectory control of an air cushion vehicle//Proceedings of IEEE/RSJ International Conference 
on Intelligent Robots and Systems (IROS'94). IEEE, 1994, 3: 1906–1913.
2. Pratt J, Chew CM, Torres A, et al. Virtual model control: an intuitive approach for bipedal locomotion. Int J Robot Res. 
2001;20(2):129–43.
3. Westervelt ER, Grizzle JW, Koditschek DE. Hybrid zero dynamics of planar biped walkers. IEEE Trans Automat Control. 
2003;48(1):42–56.
4. Fukuoka Y, Kimura H, Cohen AH. Adaptive dynamic walking of a quadruped robot on irregular terrain based on biological 
concepts. Int J Robot Res. 2003;22(3–4):187–202.
5. Shen WM, Krivokon M, Chiu H, et al. Multimode locomotion via SuperBot reconfigurable robots. Auton Robot. 
2006;20:165–77.
6. Ye C, Ma S, Li B, et al. Modular universal unit for a snake-like robot and reconfigurable robots. Adv Robotics. 
2009;23(7–8):865–87.
7. Xiao X, Murphy R. A review on snake robot testbeds in granular and restricted maneuverability spaces. Robot Auton Syst. 
2018;110:160–72.
8. Kano T, Sato T, Kobayashi R, et al. Local reflexive mechanisms essential for snakes’ scaffold-based locomotion. Bioinspir 
Biomim. 2012;7(4): 046008.
9. Jayne BC. Muscular mechanisms of snake locomotion: an electromyographic study of lateral undulation of the Florida 
banded water snake ( Nerodia fasciata ) and the yellow rat snake ( Elaphe obsoleta ). J Morphol. 1988;197(2):159–81.
10. Moon BR, Gans C. Kinematics, muscular activity and propulsion in gopher snakes. J Exp Biol. 1998;201(19):2669–84.
11. Travers M, Whitman J, Choset H. Shape-based coordination in locomotion control. Int J Robotics Res. 2018;37(10):1253–68.
12. Kamegawa T, Kuroki R, Gofuku A. Evaluation of snake robot’s behavior using randomized EARLI in crowded obsta -
cles//2014 IEEE International Symposium on Safety, Security, and Rescue Robotics. IEEE. 2014;2014:1–6.

Page 60 of 60
Guang-hui and Wan-sheng Discover Computing           (2025) 28:177 
13. Heckrotte C. Relations of body temperature, size, and crawling speed of the common garter snake. Thamnophis s sirtalis 
Copeia. 1967;4:759–63.
14. Jayne BC. Muscular mechanisms of snake locomotion: an electromyographic study of the sidewinding and concertina 
modes of Crotalus cerastes , Nerodia fasciata  and Elaphe obsoleta . J Exp Biol. 1988;140(1):1–33.
15. Jayne BC, Davis JD. Kinematics and performance capacity for the concertina locomotion of a snake ( Coluber constrictor ). J 
Exp Biol. 1991;156(1):539–56.
16. Jayne BC. What defines different modes of snake locomotion? Integr Comp Biol. 2020;60(1):156–70.
17. Gray J. The mechanism of locomotion in snakes. J Exp Biol. 1946;23(2):101–20.
18. Casal A, Yim MH. Self-reconfiguration planning for a class of modular robots//sensor fusion and decentralized control in 
robotic systems II. SPIE. 1999;3839:246–57.
19. Jayne BC. Kinematics of terrestrial snake locomotion. Copeia. 1986;1986(4):915–27.
20. Marvi H, Bridges J, Hu DL. Snakes mimic earthworms: propulsion using rectilinear travelling waves. J R Soc Interface. 
2013;10(84):20130188.
21. Mnih V, Kavukcuoglu K, Silver D, Graves A, Antonoglou I, Wierstra D, Riedmiller M. Playing Atari with Deep Reinforcement 
Learning. Proceedings of the 27th International Conference on Neural Information Processing Systems (NIPS 2015), pp. 
1–9, 2015.
22. Schulman J, Wolski F, Dhariwal P , Radford A, Klimov O. Proximal policy optimization algorithms. arXiv preprint, 2017. 2 
Serpentine robot design.
23. Sato M, Fukaya M, Iwasaki T. Serpentine locomotion with robotic snakes. IEEE Control Syst Mag. 2002;22(1):64–81.
24. Tao Y, Tao H, Zhuang Z, Stojanovic V, Paszke W. Quantized iterative learning control of communication-constrained sys -
tems with encoding and decoding mechanism. Trans Inst Meas Control. 2024;46(10):1943–54.
25. Fallahnezhad MS, Qazvini E. Transactions of the institute of measurement and control. 2017: 1097–1103.
26. Zhang Z et al. ADP-based prescribed-time control for nonlinear time-varying delay systems with uncertain parameters. 
IEEE Trans Autom Sci Eng. 2024.
27. Tao H, Zheng J, Wei J, Paszke W, Rogers E, Stojanovic V. Repetitive process based indirect-type iterative learning control for 
batch processes with model uncertainty and input delay. J Process Control. 2023;132: 103112.
28. Virgala I, Varga M, Sinčák PJ, Merva T, Mykhailyshyn R, Kelemen M. Mathematical framework for snake robot motion in a 
confined space. Appl Math Model. 2024;132:22–40.
29. Sang H, You Y, Sun X, Zhou Y. The hybrid path planning algorithm based on improved A* and artificial potential field for 
unmanned surface vehicle formations. Ocean Eng. 2021;223–224:108709.
30. Thanh HV, Quang VV. Experimental research on avoidance obstacle control for mobile robots using Q-learning (QL) and 
deep Q-learning (DQL) algorithms in dynamic environments. Actuators. 2024;13(1):26.
31. Qu H, Xing K, Takacs A. An improved genetic algorithm with co-evolutionary strategy for global path planning of multiple 
mobile robots. Neurocomputing. 2013;120:509–517.
32. Virgala I, Kelemen M, Prada E, Sukop M, Kot T, Bobovský Z, Varga M, Ferenčík P . A snake robot for locomotion in a pipe 
using trapezium-like travelling wave. Mech Mach Theory. 2021;158: 104221.
33. Elsayed BA, Takemori T, Tanaka M, Matsuno F. Mobile manipulation using a snake robot in a helical gait. IEEE/ASME Trans 
Mechatron. 2021;27(5):2600–11.
34. Takemori T, Tanaka M, Matsuno F. Hoop-passing motion for a snake robot to realize motion transition across different 
environments. IEEE Trans Robot. 2021;37(5):1696–711.
35. Chang L, Shan L, Jiang C, Dai Y. Reinforcement based mobile robot path planning with improved dynamic window 
approach in unknown environment. Autonomous Robots. 2021;45(1):51–76. 10.1007/s10514-020-09947-4
36. Montiel OH, Orozco-Rosas U, Sepúlveda RP . Path planning for mobile robots using bacterial potential field for avoiding 
static and dynamic obstacles. Expert Syst Appl. 2015;42(12):5177–5191. 10.1016/j.eswa.2015.02.033.
37. Takanashi T, Nakajima M, Takemori T, Tanaka M. Obstacle-aided locomotion of a snake robot using piecewise helixes. IEEE 
Robot Autom Lett. 2022;7(4):10542–9.
38. Syed UA, Kunwar F, Iqbal M. Guided autowave pulse coupled neural network (GAPCNN) based real time path planning 
and an obstacle avoidance scheme for mobile robots. Robot Auton Syst. 2014;62(4):474–86.
39. Qijie Z, Yue Z, Shihui L. A path planning algorithm based on RRT and SARSA (λ) in unknown and complex conditions. In 
2020 Chinese Control And Decision Conference (CCDC). IEEE; 2020. pp. 2035–2040
40. Kanada A, Takahashi R, Hayashi K, Hosaka R, Yukita W, Nakashima Y, Yokota T, Someya T, Kamezaki M, Kawahara Y, Yama -
moto M. Joint-repositionable Inner-wireless planar snake robot. IEEE Robot Autom Lett. 2025.
41. Li D, Deng H, Pan Z, Xiu Y. Collaborative obstacle avoidance algorithm of multiple bionic snake robots in fluid based on 
IB-LBM. ISA Trans. 2022;122:271–80.
42. Huang W, Guo X, Liu H, Fang Y. A robust model-based radius estimation approach for helical climbing motion of snake 
robots. IEEE ASME Trans Mechatron. 2023;28(6):3284–93.
43. Xiu Y, Li D, Deng H, Jiang S, Wu EQ. Path-following based on fuzzy line-of-sight guidance for a bionic snake robot with 
unknowns. IEEE ASME Trans Mechatron. 2023;28(6):3167–79.
44. Ji Z, Song G, Wang F, Li Y, Song A. Design and control of a snake robot with a gripper for inspection and maintenance in 
narrow spaces. IEEE Robot Autom Lett. 2023;8(5):3086–93.
Publisher's Note
Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.