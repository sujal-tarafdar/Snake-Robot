import numpy as np

class OrthogonalSnakeKinematics:
    def __init__(self, num_joints=12, link_length=0.05):
        """
        Orthogonal joint snake robot kinematics solver.
        num_joints: number of joints (typically 12 for the target hardware)
        link_length: length of each link segment in meters (default 0.05m / 50mm)
        """
        self.num_joints = num_joints
        self.link_length = link_length

    def forward_kinematics(self, joint_angles):
        """
        Computes the 3D position of each joint segment.
        joint_angles: array of length self.num_joints in radians.
                      Odd-indexed joints (1, 3, 5...) are pitch joints (rotate around Y axis).
                      Even-indexed joints (2, 4, 6...) are yaw joints (rotate around Z axis).
                      In 0-indexing:
                      - index 0, 2, 4, ... are pitch joints.
                      - index 1, 3, 5, ... are yaw joints.
        Returns:
            positions: numpy array of shape (num_joints + 1, 3) representing (x, y, z) coords.
        """
        assert len(joint_angles) == self.num_joints, f"Expected {self.num_joints} joint angles, got {len(joint_angles)}"
        
        # 13 points for 12 joints (from tail segment 0 to head segment 12)
        positions = np.zeros((self.num_joints + 1, 3))
        
        # Base transformation matrix (Tail segment at origin)
        T_global = np.eye(4)
        positions[0] = T_global[:3, 3]
        
        for i in range(self.num_joints):
            theta = joint_angles[i]
            # Check if pitch (odd joint number: 1, 3, 5... which is index 0, 2, 4...)
            # or yaw (even joint number: 2, 4, 6... which is index 1, 3, 5...)
            if i % 2 == 0:
                # Pitch joint - rotation around local Y-axis
                cos_t = np.cos(theta)
                sin_t = np.sin(theta)
                T_rot = np.array([
                    [cos_t,  0.0, sin_t, 0.0],
                    [0.0,    1.0, 0.0,   0.0],
                    [-sin_t, 0.0, cos_t, 0.0],
                    [0.0,    0.0, 0.0,   1.0]
                ])
            else:
                # Yaw joint - rotation around local Z-axis
                cos_t = np.cos(theta)
                sin_t = np.sin(theta)
                T_rot = np.array([
                    [cos_t, -sin_t, 0.0, 0.0],
                    [sin_t,  cos_t, 0.0, 0.0],
                    [0.0,    0.0,   1.0, 0.0],
                    [0.0,    0.0,   0.0, 1.0]
                ])
                
            # Translation along the local X-axis (forward to next joint)
            T_trans = np.array([
                [1.0, 0.0, 0.0, self.link_length],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])
            
            # Combine rotation and translation
            T_local = T_rot @ T_trans
            # Accumulate global transformation
            T_global = T_global @ T_local
            # Save the position of segment i+1
            positions[i + 1] = T_global[:3, 3]
            
        return positions


def calculate_alternate_link_kinematics(theta):
    """
    Computes the resulting scale link orientation angle phi from the actuated joint angle theta.
    Based on the 6th-order polynomial approximation from Raisuddin Khan et al. (2008):
    phi = 0.065*theta^6 + 0.0708*theta^5 + 0.0302*theta^4 + 0.0537*theta^3 + 0.059*theta^2 - 0.5613*theta + 2.2924
    
    theta: Actuated joint angle (in radians, range [-pi/4, pi/4])
    Returns: phi (in radians)
    """
    # Enforce range constraints: -pi/4 <= theta <= pi/4
    theta = np.clip(theta, -np.pi/4, np.pi/4)
    
    phi = (0.065 * (theta**6) + 
           0.0708 * (theta**5) + 
           0.0302 * (theta**4) + 
           0.0537 * (theta**3) + 
           0.059 * (theta**2) - 
           0.5613 * theta + 
           2.2924)
    return phi
