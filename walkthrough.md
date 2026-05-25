# Snake Robot Path Planning and Gait Kinematics Walkthrough

This document summarizes the implementation details, mathematical formulations, and verification results for the snake robot gait kinematics and path planning project. All source code is located in the [new souce code](file:///d:/IITbwb/snake%20robot/new%20souce%20code/) folder.

---

## 1. Key Mathematical Models and Formulations

### A. Gait Generation and Stabilization
The robot supports two modes of locomotion:
1. **Standard Serpenoid Curve:**
   $$\phi_i(t) = A \sin(\omega t + (i + 1/2)k) + \gamma$$
   This produces continuous forward progress but subjects the head of the snake to high-frequency lateral oscillation.

2. **Sigmoid-Improved Head Stabilization (Proposed by Zhao & Cheng, 2025):**
   To mitigate head oscillation (e.g., to stabilize a camera or head sensor), a Sigmoid dampening function $S(n)$ is applied:
   $$\theta_i = S(n) \cdot A \sin(\omega t + (i+0.5)k) + \gamma$$
   $$S(n) = \frac{1}{1 + e^{-a(n-b)}}$$
   * $n$: 1-indexed joint position from the head ($1 \le n \le 12$).
   * $a$: Slope parameter controlling the transition sharpness (default: $1.0$).
   * $b$: Number of restricted head joints (default: $3.0$).
   * As $n$ increases (moving towards the tail), $S(n) \to 1.0$, allowing the tail to oscillate at full amplitude while the head remains stabilized.

### B. Denavit-Hartenberg (D-H) 3D Forward Kinematics
We model the snake as an orthogonal joint system (alternating pitch and yaw joints) to determine the 3D position of each segment. 
* Odd joints ($1, 3, \dots, 11$; 0-indexed $0, 2, \dots, 10$) are pitch joints rotating about the local Y-axis.
* Even joints ($2, 4, \dots, 12$; 0-indexed $1, 3, \dots, 11$) are yaw joints rotating about the local Z-axis.

$$T_{local, i} = R_i \cdot T_x(L)$$
* For pitch joints: $R_i = R_y(\theta_i)$
* For yaw joints: $R_i = R_z(\theta_i)$
* $T_x(L)$: Translation along the segment axis by link length $L = 50\text{ mm}$.

### C. Alternate Link Scale Kinematics
Based on the Raisuddin Khan alternate-link scale kinematics relation, the passive link orientation angle $\varphi$ as a function of the actuated joint angle $\theta$ is approximated by a 6th-order polynomial:
$$\varphi = 0.065\theta^6 + 0.0708\theta^5 + 0.0302\theta^4 + 0.0537\theta^3 + 0.059\theta^2 - 0.5613\theta + 2.2924$$
where $\theta$ is restricted to $[-\pi/4, \pi/4]$ radians.

### D. Path Sinusoidal Fitting and Control Parameter Mapping
Once a smooth path is planned, we fit its $(x, y)$ coordinates to a sinusoidal curve:
$$y = A_\omega \sin(\omega x + \phi) + \text{offset}$$
Using the binary quadratic regression model with optimized coefficients from the paper, we map the fitted spatial amplitude $A_\omega$ (in mm) and spatial frequency $\omega$ (in rad/mm) directly to joint control amplitude $A$ and phase lag $k$:
$$A = P_1 + P_2 A_\omega + P_3 \omega + P_4 A_\omega^2 + P_5 A_\omega \omega + P_6 \omega^2$$
$$k = C_1 + C_2 A_\omega + C_3 \omega + C_4 A_\omega^2 + C_5 A_\omega \omega + C_6 \omega^2$$

Coefficients (Table 3):
* $P = [-0.5405, 0.01384, 42.97, -0.0001123, 0.5253, -673.2]$
* $C = [0.3223, -0.00135, 34.95, -1.63 \times 10^{-7}, -0.09762, -333.7]$

---

## 2. Verification Results and Visualizations

We executed the full suite of verification tests to ensure algorithm compliance.

### A. Gait and Kinematics Validation (`test_kinematics.py`)
Running the kinematics test successfully produced the following visualizations:

1. **Gait Amplitude Envelope:** Shows how the joint oscillation amplitude is dampened near the head to ensure camera/sensor stability.
   ![Gait Amplitude Envelope Comparison](C:/Users/sujal/.gemini/antigravity/brain/5cbda28f-39bb-4645-ae0c-f74edff545f8/gait_amplitude_envelope.png)

2. **3D Snake Robot Configuration:** Reconstructs the 3D spatial curve of the snake robot body under serpentine and Sigmoid-dampened motion. Notice the stabilized (straightened) head segment of the Sigmoid snake at the tail-to-head transition.
   ![3D Snake Robot Configuration](C:/Users/sujal/.gemini/antigravity/brain/5cbda28f-39bb-4645-ae0c-f74edff545f8/snake_3d_shapes.png)

3. **Alternate Link Kinematics:** Shows the 6th-order polynomial mapping between the actuated joint angle and the passive scale link orientation.
   ![Alternate Link Kinematics](C:/Users/sujal/.gemini/antigravity/brain/5cbda28f-39bb-4645-ae0c-f74edff545f8/alternate_link_kinematics.png)

---

### B. Path Planning and Smoothing Validation (`test_planner.py`)
Evaluating the A* path planner and double-stage smoothing produced the following metrics:

| Metric | Traditional A* ($w=1.0$) | Improved A* ($w=1.3$) | Improvement | Target |
| :--- | :--- | :--- | :--- | :--- |
| **Nodes Expanded** | 113 | 27 | **76.11% Reduction** | $\ge 15\%$ |
| **Path Corners** | 7 | 2 | **71.43% Reduction** | $\ge 25\%$ |

1. **Planning and Smoothing Comparison:** Shows the jagged traditional A* search compared to the highly optimized, corner-pruned, and LOWESS-smoothed final path.
   ![Path Planning Comparison](C:/Users/sujal/.gemini/antigravity/brain/5cbda28f-39bb-4645-ae0c-f74edff545f8/path_planning_comparison.png)

2. **Path Sinusoid Fitting:** Demonstrates how the smoothed path coordinates fit the sinusoidal path model ($R^2 \approx 1.0$), which is subsequently mapped back into joint servo control signals.
   ![Path Sinusoidal Fitting](C:/Users/sujal/.gemini/antigravity/brain/5cbda28f-39bb-4645-ae0c-f74edff545f8/path_sinusoid_fitting.png)

---

## 3. Developed Source Code Inventory

All files are verified and compile/execute correctly:

1. **[kinematics.py](file:///d:/IITbwb/snake%20robot/new%20souce%20code/kinematics.py):** Python kinematics module. Implements 3D orthogonal coordinate projection and Raisuddin alternate kinematics.
2. **[gait_generator.py](file:///d:/IITbwb/snake%20robot/new%20souce%20code/gait_generator.py):** Gait calculations (standard and Sigmoid curves).
3. **[parameter_fitting.py](file:///d:/IITbwb/snake%20robot/new%20souce%20code/parameter_fitting.py):** Regression fitting of planned path to control values using optimized paper coefficients.
4. **[improved_astar.py](file:///d:/IITbwb/snake%20robot/new%20souce%20code/improved_astar.py):** Weighted A* algorithm, Bresenham LOS checking, and two-stage smoothing.
5. **[Serpentine_Sigmoid_Control.ino](file:///d:/IITbwb/snake%20robot/new%20souce%20code/Serpentine_Sigmoid_Control.ino):** Fully featured, Arduino-compatible firmware. Uses `Servo.h` to drive 12 servos on pins 2–13 and maps remote inputs on pins 14–17. Integrates the Sigmoid amplitude formula in C++.
6. **[test_kinematics.py](file:///d:/IITbwb/snake%20robot/new%20souce%20code/test_kinematics.py):** Execution test generating the 3D plots and kinematics validation.
7. **[test_planner.py](file:///d:/IITbwb/snake%20robot/new%20souce%20code/test_planner.py):** Performance profiling of nodes expanded and path smoothers.
8. **[Concertina_Control.ino](file:///d:/IITbwb/snake%20robot/new%20souce%20code/Concertina_Control.ino):** Arduino firmware implementing the Concertina gait using alternating odd/even joint phase loops.

---

## 4. Concertina Gait Implementation Details

The Concertina motion logic functions as follows:
* **Phase Toggling:** Alternates between `oddPhase` and `evenPhase` at a frequency controlled by `phaseDelay` (e.g., 2000 ms).
* **Odd Phase Loop:** Moves odd-indexed joints together according to $A \sin(\omega t)$, while keeping even-indexed joints stationary at their center position calibration.
* **Even Phase Loop:** Moves even-indexed joints together according to $A \sin(\omega t)$, while keeping odd-indexed joints stationary at their center calibration.
* **Range Constraints:** Constrains joint motion safely. For the odd/even joints with a center of $90^\circ$, limits are $[60^\circ, 120^\circ]$. For `servo[2]` (calibrated at a center offset of $180^\circ$), the code adapts its bounds to $[140^\circ, 180^\circ]$ to ensure full range of motion.
