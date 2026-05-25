import numpy as np

class SnakeGaitGenerator:
    def __init__(self, num_joints=12):
        """
        Gait generator for a snake robot.
        num_joints: number of joints (default is 12)
        """
        self.num_joints = num_joints

    def generate_serpenoid_gait(self, t, A, omega, lag, gamma=0.0):
        """
        Generates the standard discretized Serpenoid curve joint angles.
        theta_i = A * sin(omega * t + (i + 1/2)*lag) + gamma
        t: current time or phase step
        A: amplitude (in radians)
        omega: angular frequency
        lag: phase lag between adjacent joints
        gamma: steering offset bias (in radians)
        """
        angles = np.zeros(self.num_joints)
        for i in range(self.num_joints):
            # Paper definition of phase offset: (i + 0.5) * lag
            phase = (i + 0.5) * lag
            angles[i] = A * np.sin(omega * t + phase) + gamma
        return angles

    def generate_sigmoid_gait(self, t, A, omega, lag, a=1.0, b=3.0, gamma=0.0, head_at_start=True):
        """
        Generates joint angles with the Sigmoid-improved amplitude stabilization.
        theta_i = S(n) * A * sin(omega * t + phase_i) + gamma
        where S(n) = 1 / (1 + exp(-a * (n - b)))
        
        t: current time or phase step
        A: target amplitude (in radians)
        omega: angular frequency
        lag: phase lag between adjacent joints
        a: slope parameter of the Sigmoid function
        b: center parameter of the Sigmoid function (number of restricted head joints)
        gamma: steering offset bias (in radians)
        head_at_start: if True, joint index 0 is the head (so n starts at 1 and increases to 12).
                       if False, joint index 11 is the head (so n starts at 12 and decreases to 1).
        """
        angles = np.zeros(self.num_joints)
        for i in range(self.num_joints):
            # Determine n (the joint number starting from the head)
            # n is 1-indexed for the Sigmoid formula
            if head_at_start:
                n = i + 1
            else:
                n = self.num_joints - i
                
            # Sigmoid dampening factor
            sigmoid_factor = 1.0 / (1.0 + np.exp(-a * (n - b)))
            
            # Phase calculation (based on head position)
            phase = (i + 0.5) * lag
            
            # Joint angle equation
            angles[i] = sigmoid_factor * A * np.sin(omega * t + phase) + gamma
            
        return angles

    def generate_arduino_style_gait(self, step_counter, amplitude_deg, frequency, lag_rad, offset_deg, turn_offset_deg=0.0):
        """
        Replicates the Arduino sketch math for comparison/firmware validation.
        theta_i = 90 + offset + turn_offset + amplitude * cos(frequency * step_counter * pi/180 + phase_lag)
        """
        angles_deg = np.zeros(self.num_joints)
        for i in range(self.num_joints):
            joint_idx_1based = i + 1
            # Phase lag matching: s1.write(cos(... + 5*lag)), s2: 4*lag, ..., s12: -6*lag
            phase_multiplier = 6 - joint_idx_1based
            phase = phase_multiplier * lag_rad
            
            # Convert step counter to radians
            angle_rad = frequency * step_counter * np.pi / 180.0
            
            # Joint angle
            angles_deg[i] = 90.0 + offset_deg + turn_offset_deg + amplitude_deg * np.cos(angle_rad + phase)
            
        return angles_deg
