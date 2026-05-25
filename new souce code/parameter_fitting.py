import numpy as np
from scipy.optimize import curve_fit

def sine_model(x, A_w, omega, phase, offset):
    """
    Trigonometric model function for the path shape:
    y = A_w * sin(omega * x + phase) + offset
    """
    return A_w * np.sin(omega * x + phase) + offset

def fit_path_to_sinusoid(x_coords, y_coords):
    """
    Fits path (x, y) coordinates to the sinusoid: y = A_w * sin(omega * x + phase) + offset
    Returns:
        A_w: Curve amplitude (amplitude of spatial wave in mm/units)
        omega: Spatial frequency (rad/mm or rad/unit)
        phase: Phase shift
        offset: Center offset
    """
    x = np.array(x_coords)
    y = np.array(y_coords)
    
    # Robust initial guesses
    a_guess = (np.max(y) - np.min(y)) / 2.0
    if a_guess == 0:
        a_guess = 1.0
        
    offset_guess = np.mean(y)
    
    # Frequency guess: assume roughly 1-2 waves over the range of x
    x_range = np.max(x) - np.min(x)
    if x_range == 0:
        x_range = 1.0
    omega_guess = 2.0 * np.pi / x_range
    
    phase_guess = 0.0
    
    p0 = [a_guess, omega_guess, phase_guess, offset_guess]
    
    # Constraints to keep parameters reasonable
    # A_w > 0, omega > 0
    bounds = (
        [0.0, 0.0, -2.0*np.pi, -np.inf],
        [np.inf, np.inf, 2.0*np.pi, np.inf]
    )
    
    try:
        popt, pcov = curve_fit(sine_model, x, y, p0=p0, bounds=bounds, maxfev=5000)
        A_w, omega, phase, offset = popt
        return A_w, omega, phase, offset
    except Exception as e:
        print(f"Warning: Curve fitting failed ({e}). Returning initial guesses.")
        return a_guess, omega_guess, phase_guess, offset_guess


def map_shape_to_control_params(A_w, omega):
    """
    Maps path shape parameters (A_w, omega) to robot joint control parameters (A, k)
    using the binary quadratic polynomial regression from Zhao Guang-hui & Cheng Wan-sheng (2025).
    
    Formula:
    A = P1 + P2*A_w + P3*omega + P4*A_w^2 + P5*A_w*omega + P6*omega^2
    k = C1 + C2*A_w + C3*omega + C4*A_w^2 + C5*A_w*omega + C6*omega^2
    
    Optimized coefficients from Table 3 of the paper:
    P1 = -0.5405, P2 = 0.01384, P3 = 42.97, P4 = -0.0001123, P5 = 0.5253, P6 = -673.2
    C1 = 0.3223, C2 = -0.00135, C3 = 34.95, C4 = -1.63e-7, C5 = -0.09762, C6 = -333.7
    
    A_w: wave amplitude of path (typically in mm, e.g. 23.38 to 69.16)
    omega: spatial frequency of path (typically in rad/mm, e.g. 0.0163 to 0.0327)
    
    Returns:
        A: joint amplitude (control parameter A, typically in radians, e.g. 0.8 to 1.2)
        k: joint phase lag (control parameter k, typically in radians, e.g. 0.6 to 1.0)
    """
    # Table 3 coefficients
    P = [-0.5405, 0.01384, 42.97, -0.0001123, 0.5253, -673.2]
    C = [0.3223, -0.00135, 34.95, -1.63e-7, -0.09762, -333.7]
    
    # Calculate A
    A = (P[0] + 
         P[1] * A_w + 
         P[2] * omega + 
         P[3] * (A_w ** 2) + 
         P[4] * A_w * omega + 
         P[5] * (omega ** 2))
         
    # Calculate k
    k = (C[0] + 
         C[1] * A_w + 
         C[2] * omega + 
         C[3] * (A_w ** 2) + 
         C[4] * A_w * omega + 
         C[5] * (omega ** 2))
         
    # Apply safety clipping to keep A and k within physically stable limits
    # e.g., A in [0.2, 2.0] radians, k in [0.1, 2.0] radians
    A = np.clip(A, 0.2, 2.0)
    k = np.clip(k, 0.1, 2.0)
    
    return A, k
