import numpy as np
import math

class GridMap:
    def __init__(self, width=20, height=20, obstacles=None):
        """
        Represents a 2D grid map.
        0: Free cell
        1: Obstacle cell
        """
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=int)
        
        if obstacles is not None:
            for obs in obstacles:
                x, y = obs
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.grid[x, y] = 1

    def is_free(self, x, y):
        """Checks if cell is within bounds and free of obstacles."""
        return 0 <= x < self.width and 0 <= y < self.height and self.grid[x, y] == 0

    def is_line_of_sight_free(self, p1, p2):
        """
        Ray-casting using Bresenham's Line Algorithm to check if a straight line
        between p1 and p2 is completely free of obstacles.
        """
        x1, y1 = int(round(p1[0])), int(round(p1[1]))
        x2, y2 = int(round(p2[0])), int(round(p2[1]))
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
        x, y = x1, y1
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        # Check boundary/starting points
        if not self.is_free(x, y):
            return False
            
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                x += sx
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                if not self.is_free(x, y):
                    return False
        else:
            err = dy / 2.0
            while y != y2:
                y += sy
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                if not self.is_free(x, y):
                    return False
                    
        return self.is_free(x2, y2)


class ImprovedAStarPlanner:
    def __init__(self, grid_map, heuristic_weight=1.3):
        """
        Improved A* Planner with weighted heuristic.
        heuristic_weight (w): typically in the range [1.2, 1.5].
        """
        self.grid_map = grid_map
        self.w = heuristic_weight

    def _heuristic(self, p1, p2):
        """Euclidean distance heuristic."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def plan(self, start, goal):
        """
        Plans a path from start to goal.
        start: tuple (x, y)
        goal: tuple (x, y)
        Returns:
            path: list of (x, y) coordinates representing the planned path, or None if no path exists.
            nodes_expanded: number of nodes expanded during the search.
        """
        # Node structure: (x, y) -> [g_score, parent_node]
        open_set = {start: [0.0, None]}
        closed_set = {}
        nodes_expanded = 0
        
        # Actions: 8-connected grid movement
        moves = [
            (1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), # Cardinals
            (1, 1, math.sqrt(2)), (1, -1, math.sqrt(2)),          # Diagonals
            (-1, 1, math.sqrt(2)), (-1, -1, math.sqrt(2))
        ]
        
        while open_set:
            # Find node in open_set with minimum f_score = g + w*h
            current = min(
                open_set.keys(),
                key=lambda x: open_set[x][0] + self.w * self._heuristic(x, goal)
            )
            
            g_current, parent = open_set[current]
            
            # Move current to closed_set
            closed_set[current] = [g_current, parent]
            del open_set[current]
            nodes_expanded += 1
            
            # Goal check
            if current == goal:
                # Reconstruct path
                path = []
                curr = goal
                while curr is not None:
                    path.append(curr)
                    curr = closed_set[curr][1]
                path.reverse()
                return path, nodes_expanded
                
            # Expand neighbors
            for dx, dy, cost in moves:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if not self.grid_map.is_free(neighbor[0], neighbor[1]):
                    continue
                    
                if neighbor in closed_set:
                    continue
                    
                g_new = g_current + cost
                
                if neighbor not in open_set:
                    open_set[neighbor] = [g_new, current]
                else:
                    if g_new < open_set[neighbor][0]:
                        open_set[neighbor] = [g_new, current]
                        
        return None, nodes_expanded


def prune_path_corners(path, grid_map):
    """
    Redundant corner turn pruning.
    Iteratively simplifies the path by skipping redundant intermediate nodes
    if a direct straight line between parent and descendant is obstacle-free.
    """
    if path is None or len(path) <= 2:
        return path
        
    pruned = [path[0]]
    curr_idx = 0
    
    while curr_idx < len(path) - 1:
        next_idx = curr_idx + 1
        # Greedy line-of-sight lookahead
        for test_idx in range(curr_idx + 2, len(path)):
            if grid_map.is_line_of_sight_free(path[curr_idx], path[test_idx]):
                next_idx = test_idx
        
        pruned.append(path[next_idx])
        curr_idx = next_idx
        
    return pruned


def gradient_descent_smooth(path, grid_map, alpha=0.5, beta=0.15, tolerance=0.00001, max_iterations=500):
    """
    Stage 1 Smooth: Gradient Descent path optimization.
    Pulls nodes closer to neighbors (midpoint tension) while retaining coordinate fidelity
    to the original nodes and checking obstacle boundary constraints.
    """
    if path is None or len(path) <= 2:
        return path
        
    smoothed = [np.array(p, dtype=float) for p in path]
    original = [np.array(p, dtype=float) for p in path]
    N = len(smoothed)
    
    change = tolerance + 1.0
    iteration = 0
    
    while change > tolerance and iteration < max_iterations:
        change = 0.0
        # Start and Goal points (smoothed[0] and smoothed[N-1]) remain fixed
        for i in range(1, N - 1):
            old_val = np.copy(smoothed[i])
            
            # Gradient components
            data_fidelity = original[i] - smoothed[i]
            smoothness_midpoint = smoothed[i-1] + smoothed[i+1] - 2.0 * smoothed[i]
            
            # Gradient descent step
            new_val = smoothed[i] + alpha * data_fidelity + beta * smoothness_midpoint
            
            # Obstacle boundary check
            grid_x, grid_y = int(round(new_val[0])), int(round(new_val[1]))
            if grid_map.is_free(grid_x, grid_y):
                smoothed[i] = new_val
                change += np.linalg.norm(smoothed[i] - old_val)
                
        iteration += 1
        
    return [tuple(p) for p in smoothed]


def lowess_smooth_path(path, frac=0.25):
    """
    Stage 2 Smooth: Locally Weighted Scatterplot Smoothing (LOWESS) regression.
    Smooths parametric coordinates x(t) and y(t) as functions of path progress index t.
    frac: fraction of path points used to construct the local neighborhood regression window.
    """
    if path is None or len(path) <= 3:
        return path
        
    N = len(path)
    t = np.arange(N, dtype=float)
    x = np.array([p[0] for p in path], dtype=float)
    y = np.array([p[1] for p in path], dtype=float)
    
    # Neighborhood window size (minimum of 3 points)
    K = max(3, int(round(frac * N)))
    
    smoothed_x = np.zeros(N)
    smoothed_y = np.zeros(N)
    
    # Keep endpoints fixed
    smoothed_x[0], smoothed_y[0] = x[0], y[0]
    smoothed_x[-1], smoothed_y[-1] = x[-1], y[-1]
    
    for i in range(1, N - 1):
        t0 = t[i]
        dists = np.abs(t - t0)
        
        # Sort distances and get K nearest neighbors
        idx_neighbors = np.argsort(dists)[:K]
        d_max = dists[idx_neighbors[-1]]
        if d_max == 0:
            d_max = 1e-6
            
        # Tricube kernel weights: w_j = (1 - (d_j / d_max)^3)^3 for d_j < d_max
        w = np.zeros(N)
        for idx in idx_neighbors:
            d = dists[idx]
            if d < d_max:
                w[idx] = (1.0 - (d / d_max)**3)**3
            else:
                w[idx] = 0.0
                
        # Weighted linear regression: Y = a + b * T
        # Solve least squares: X_reg^T * W * X_reg * beta = X_reg^T * W * Y
        T_neighbors = t[idx_neighbors]
        x_neighbors = x[idx_neighbors]
        y_neighbors = y[idx_neighbors]
        w_neighbors = w[idx_neighbors]
        
        # Construction of design matrix
        X_reg = np.vstack([np.ones(len(T_neighbors)), T_neighbors]).T
        W = np.diag(w_neighbors)
        
        # Solve for x-coordinate
        lhs = X_reg.T @ W @ X_reg
        # Add tiny regularization to prevent singularity
        lhs += np.eye(2) * 1e-9
        
        rhs_x = X_reg.T @ W @ x_neighbors
        beta_x = np.linalg.solve(lhs, rhs_x)
        smoothed_x[i] = beta_x[0] + beta_x[1] * t0
        
        # Solve for y-coordinate
        rhs_y = X_reg.T @ W @ y_neighbors
        beta_y = np.linalg.solve(lhs, rhs_y)
        smoothed_y[i] = beta_y[0] + beta_y[1] * t0
        
    return [(smoothed_x[i], smoothed_y[i]) for i in range(N)]
