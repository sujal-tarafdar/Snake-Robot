import os
import time
import numpy as np
import matplotlib.pyplot as plt
from improved_astar import GridMap, ImprovedAStarPlanner, prune_path_corners, gradient_descent_smooth, lowess_smooth_path
from parameter_fitting import fit_path_to_sinusoid, map_shape_to_control_params

def calculate_corners(path):
    """
    Counts the number of corners (turns) in the path.
    A turn is detected when the direction vector between consecutive segments changes.
    """
    if path is None or len(path) <= 2:
        return 0
    
    corners = 0
    for i in range(1, len(path) - 1):
        p1 = np.array(path[i-1])
        p2 = np.array(path[i])
        p3 = np.array(path[i+1])
        
        v1 = p2 - p1
        v2 = p3 - p2
        
        # Calculate dot product and norm to find angle
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 > 0 and norm_v2 > 0:
            cos_angle = np.dot(v1, v2) / (norm_v1 * norm_v2)
            # If vectors are not parallel (cos_angle close to 1.0), it's a corner
            if cos_angle < 0.99:  # approx threshold for turns
                corners += 1
    return corners

def run_planning_tests():
    print("=== Testing Snake Robot Improved A* Planner and Smoothing ===")
    
    # 1. Define 20x20 Grid Map with obstacle blocks
    width, height = 20, 20
    obstacles = []
    
    # Scattered box obstacles
    # Box 1
    for x in range(4, 8):
        for y in range(4, 8):
            obstacles.append((x, y))
    # Box 2
    for x in range(12, 16):
        for y in range(12, 16):
            obstacles.append((x, y))
    # Box 3
    for x in range(8, 12):
        for y in range(10, 14):
            obstacles.append((x, y))
        
    grid = GridMap(width=width, height=height, obstacles=obstacles)
    
    # Start and Goal points
    start = (1, 1)
    goal = (18, 18)
    
    # 2. Traditional A* Planner (w = 1.0)
    trad_planner = ImprovedAStarPlanner(grid, heuristic_weight=1.0)
    start_time = time.time()
    trad_path, trad_expanded = trad_planner.plan(start, goal)
    trad_time = time.time() - start_time
    
    # 3. Improved A* Planner (w = 1.3)
    imp_planner = ImprovedAStarPlanner(grid, heuristic_weight=1.3)
    start_time = time.time()
    imp_path, imp_expanded = imp_planner.plan(start, goal)
    imp_time = time.time() - start_time
    
    # 4. Search Space Reduction Check
    reduction_pct = ((trad_expanded - imp_expanded) / trad_expanded) * 100.0
    print(f"\nTraditional A* Nodes Expanded: {trad_expanded}")
    print(f"Improved A* Nodes Expanded: {imp_expanded}")
    print(f"Search Space Reduction: {reduction_pct:.2f}% (Target: >= 15%)")
    assert reduction_pct >= 15.0, f"Reduction was {reduction_pct:.2f}%, which is less than 15%"
    
    # 5. Path Optimizations (Pruning + Double Smoothing)
    pruned_path = prune_path_corners(imp_path, grid)
    gd_path = gradient_descent_smooth(pruned_path, grid, alpha=0.5, beta=0.15)
    smoothed_path = lowess_smooth_path(gd_path, frac=0.3)
    
    # 6. Corner Reduction Metrics
    orig_corners = calculate_corners(imp_path)
    pruned_corners = calculate_corners(pruned_path)
    smoothed_corners = calculate_corners(smoothed_path)
    
    corner_reduction_pct = ((orig_corners - smoothed_corners) / orig_corners) * 100.0
    print(f"\nCorners in Raw Path: {orig_corners}")
    print(f"Corners in Pruned Path: {pruned_corners}")
    print(f"Corners in Smoothed Path: {smoothed_corners}")
    print(f"Corner Reduction: {corner_reduction_pct:.2f}% (Target: >= 25%)")
    assert corner_reduction_pct >= 25.0, f"Corner reduction was {corner_reduction_pct:.2f}%, which is less than 25%"
    
    # 7. Sinusoidal Curve Fitting & Gait Mapping
    # Convert path to separate x and y coordinate arrays
    x_coords = np.array([p[0] for p in smoothed_path])
    y_coords = np.array([p[1] for p in smoothed_path])
    
    # Fit smoothed path to y = A_w * sin(omega * x + phase) + offset
    # In order to simulate physical coordinates (e.g. millimeters) as in the paper,
    # let's assume each grid cell is 50 mm (0.05 meters).
    cell_size_mm = 50.0
    x_coords_mm = x_coords * cell_size_mm
    y_coords_mm = y_coords * cell_size_mm
    
    A_w, omega_val, phase_val, offset_val = fit_path_to_sinusoid(x_coords_mm, y_coords_mm)
    print(f"\nFitted Spatial Wave Amplitude A_w: {A_w:.4f} mm")
    print(f"Fitted Spatial Frequency omega: {omega_val:.4f} rad/mm")
    
    # Map to control parameters using binary quadratic polynomial regression
    A_control, k_control = map_shape_to_control_params(A_w, omega_val)
    print(f"Mapped Joint Control Amplitude A: {A_control:.4f} rad ({np.degrees(A_control):.2f}°)")
    print(f"Mapped Joint Control Phase Lag k: {k_control:.4f} rad ({np.degrees(k_control):.2f}°)")
    
    # 8. Visualizations
    plt.figure(figsize=(10, 10))
    
    # Draw Grid and Obstacles
    obstacle_x = [obs[0] for obs in obstacles]
    obstacle_y = [obs[1] for obs in obstacles]
    plt.scatter(obstacle_x, obstacle_y, color='#2b2b2b', marker='s', s=450, label='Obstacles')
    
    # Draw Paths
    if trad_path:
        tx, ty = zip(*trad_path)
        plt.plot(tx, ty, 'x--', color='#7f7f7f', label='Traditional A* Path', alpha=0.7, linewidth=1.5)
        
    if imp_path:
        ix, iy = zip(*imp_path)
        plt.plot(ix, iy, 'o-', color='#d62728', label='Improved A* Path (Raw)', alpha=0.5, linewidth=2)
        
    if pruned_path:
        px, py = zip(*pruned_path)
        plt.plot(px, py, '^-', color='#ff7f0e', label='Pruned Path (Line of Sight)', linewidth=2)
        
    if smoothed_path:
        sx, sy = zip(*smoothed_path)
        plt.plot(sx, sy, 's-', color='#1f77b4', label='Stage-2 LOWESS Smoothed Path', linewidth=3)
        
    # Draw Start and Goal
    plt.scatter([start[0]], [start[1]], color='green', marker='o', s=200, zorder=5, label='Start')
    plt.scatter([goal[0]], [goal[1]], color='blue', marker='*', s=250, zorder=5, label='Goal')
    
    plt.title('Improved A* Path Planning and Double-Stage Smoothing', fontsize=14, fontweight='bold')
    plt.xlabel('Grid X', fontsize=12)
    plt.ylabel('Grid Y', fontsize=12)
    plt.xlim(-1, width)
    plt.ylim(-1, height)
    plt.grid(True, which='both', color='#cccccc', linestyle=':', alpha=0.5)
    plt.legend(fontsize=11, loc='upper left')
    plt.gca().set_aspect('equal', adjustable='box')
    
    plt.tight_layout()
    chart_path = 'path_planning_comparison.png'
    plt.savefig(chart_path, dpi=300)
    print(f"\nSaved planning comparison plot to: {os.path.abspath(chart_path)}")
    plt.close()
    
    # Also plot the fitted sine curve over the smoothed path
    plt.figure(figsize=(10, 5))
    fit_x = np.linspace(np.min(x_coords_mm), np.max(x_coords_mm), 200)
    fit_y = A_w * np.sin(omega_val * fit_x + phase_val) + offset_val
    plt.plot(x_coords_mm, y_coords_mm, 'o', color='#1f77b4', label='Smoothed Path Coordinates')
    plt.plot(fit_x, fit_y, '-', color='#2ca02c', linewidth=2.5, label=f'Fitted Sine: A_w={A_w:.1f}mm, $\\omega$={omega_val:.4f}')
    plt.title('Sinusoidal Parameter Fitting of Planned Path', fontsize=14, fontweight='bold')
    plt.xlabel('X coordinate (mm)', fontsize=12)
    plt.ylabel('Y coordinate (mm)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    fit_plot_path = 'path_sinusoid_fitting.png'
    plt.savefig(fit_plot_path, dpi=300)
    print(f"Saved path sinusoid fitting plot to: {os.path.abspath(fit_plot_path)}")
    plt.close()
    
    print("Path planner and smoothing verification test script successfully prepared.\n")

if __name__ == '__main__':
    run_planning_tests()
