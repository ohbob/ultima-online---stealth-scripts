import time

from py_stealth import *
import matplotlib.pyplot as plt
import math
import random

trees = [3274, 3275, 3277, 3280, 3283, 3287, 3286, 3288, 3290, 3293, 3296, 3320, 3323, 3326, 3329, 3393, 3394, 3395,
         3396, 3415, 3416, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484,
         3492, 3496]

caves = [1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352,
         1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363, 1386
         ]


def get_tiles(radius: int, tiles):
    x, y = GetX(Self()), GetY(Self())
    min_x = x - radius
    min_y = y - radius
    max_x = x + radius
    max_y = y + radius

    found_tiles = []
    for tile in tiles:
        found_tiles.extend(GetLandTilesArray(min_x, min_y, max_x, max_y, WorldNum(), tile))
        found_tiles.extend(GetStaticTilesArray(min_x, min_y, max_x, max_y, WorldNum(), tile))
    return found_tiles


def calculate_total_steps(dataset, player_position):
    """
    Calculates the total number of steps required to visit all points in the dataset from the player's position.

    :param dataset: List of tuples, each tuple contains (tile, x, y, z)
    :param player_position: Tuple containing the player's (x, y) position
    :return: Total number of steps (distance)
    """
    if not dataset:
        return 0

    total_steps = 0
    current_position = player_position

    for _, x, y, _ in dataset:
        next_position = (x, y)
        step_distance = math.sqrt(
            (next_position[0] - current_position[0]) ** 2 + (next_position[1] - current_position[1]) ** 2)
        total_steps += step_distance
        current_position = next_position

    return int(total_steps)


def plot_multiple_tree_maps(datasets, player_positions, titles, radius=25, rotation_angle=320):
    """
    Plots multiple tree maps in a 2x2 grid layout based on given datasets with sequential numbering on each dot,
    a path from the player, and additional title information.

    :param datasets: List of datasets, each dataset is a list of tuples (tile, x, y, z)
    :param player_positions: List of tuples containing the player's (x, y) positions for each dataset
    :param titles: List of title strings for each dataset
    :param radius: Radius around the player to consider for plotting (same for all maps)
    :param rotation_angle: Angle in degrees to rotate the map (same for all maps)
    """

    def rotate_point(x, y, angle, origin=(0, 0)):
        ox, oy = origin
        px, py = x - ox, y - oy
        qx = ox + math.cos(angle) * px - math.sin(angle) * py
        qy = oy + math.sin(angle) * px + math.cos(angle) * py
        return qx, qy

    num_datasets = len(datasets)
    # Adjust here for a 2x2 grid layout
    fig, axs = plt.subplots(2, 2, figsize=(20, 20))  # 2 rows, 2 columns
    axs = axs.flatten()  # Flatten the array to make indexing easier

    for idx, data in enumerate(datasets):
        if idx < num_datasets:
            ax = axs[idx]

            # Extracting x and y coordinates from 'data'
            x_coords = [x for _, x, y, _ in data]
            y_coords = [y for _, x, y, _ in data]

            # Rotate each point
            angle_radians = math.radians(rotation_angle)
            player_position = player_positions[idx]
            rotated_coords = [rotate_point(px, py, angle_radians, origin=player_position) for px, py in
                              zip(x_coords, y_coords)]

            # Plotting the path
            current_pos = player_position
            for i, (x, y) in enumerate(rotated_coords):
                ax.plot([current_pos[0], x], [current_pos[1], y], color='black', linestyle='-', linewidth=0.5)
                current_pos = (x, y)

            # Plotting the trees and annotations
            annotation_offset = 0.3
            for i, (x, y) in enumerate(rotated_coords):
                ax.scatter(x, y, color='green')
                ax.text(x + annotation_offset, y + annotation_offset, str(i + 1), color='blue', fontsize=10)

            ax.scatter([], [], color='green', label=f'Trees ({len(data)})')
            ax.scatter(*player_position, color='red', label='Player Position', s=100)

            # Adding the title (additional text)
            ax.set_title(titles[idx], loc='left')
            ax.set_xlabel("X Coordinate")
            ax.set_ylabel("Y Coordinate")
            ax.legend()
            ax.grid(True)

    plt.tight_layout()
    plt.show()


def calculate_route(points, tsp_algorithm):
    def calculate_distance(point1, point2):
        """Calculate the Euclidean distance between two points."""
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def calculate_all_distances():
        """Precompute distances between all pairs of points."""
        num_points = len(points)
        dist_matrix = [[0] * num_points for _ in range(num_points)]
        for i in range(num_points):
            for j in range(i + 1, num_points):
                dist = calculate_distance(points[i], points[j])
                dist_matrix[i][j] = dist_matrix[j][i] = dist
        return dist_matrix

    dist_matrix = calculate_all_distances()
    return tsp_algorithm(points, dist_matrix)



def adapted_tsp_algorithm(dataset, tsp_algorithm):
    # Create a mapping from (x, y) to the full data tuple
    xy_to_full_data = {(x, y): full_data for full_data in dataset for _, x, y, _ in [full_data]}

    # Extract x and y coordinates from dataset
    points = [(x, y) for _, x, y, _ in dataset]

    # Start timing
    start_time = time.perf_counter()

    # Calculate the route using the given TSP algorithm
    path, length = calculate_route(points, tsp_algorithm)

    # Stop timing
    elapsed_time = time.perf_counter() - start_time

    # Map the sorted (x, y) path back to the original dataset format
    adapted_path = [xy_to_full_data[(x, y)] for x, y in path]

    return adapted_path, int(length), elapsed_time


def nearest_neighbor_tsp(points, dist_matrix):
    best_path, best_length = None, float('inf')
    num_points = len(points)

    for start_index in range(num_points):
        path = [start_index]
        total_length = 0
        visited = {start_index}

        current_index = start_index
        while len(visited) < num_points:
            nearest_index, nearest_distance = min(
                ((i, dist_matrix[current_index][i]) for i in range(num_points) if i not in visited),
                key=lambda x: x[1]
            )

            visited.add(nearest_index)
            path.append(nearest_index)
            total_length += nearest_distance
            current_index = nearest_index

        if total_length < best_length:
            best_length = total_length
            best_path = [points[i] for i in path]

    return best_path, best_length


def random_path_tsp(points, dist_matrix):
    path = random.sample(range(len(points)), len(points))
    total_length = sum(dist_matrix[path[i - 1]][path[i]] for i in range(1, len(points)))
    return [points[i] for i in path], total_length


def greedy_tsp(points, dist_matrix):
    start_index = 0
    path = [start_index]
    total_length = 0
    visited = {start_index}

    while len(visited) < len(points):
        nearest_index, nearest_distance = min(
            ((i, dist_matrix[path[-1]][i]) for i in range(len(points)) if i not in visited),
            key=lambda x: x[1]
        )

        visited.add(nearest_index)
        path.append(nearest_index)
        total_length += nearest_distance

    # Do not return to start; just calculate the path traversed
    return [points[i] for i in path], total_length


def two_opt_tsp(points, dist_matrix):
    def two_opt_swap(route, i, k):
        """Perform a 2-opt swap by reversing the route segment between i and k."""
        return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

    num_points = len(points)
    best_route = list(range(num_points))
    improved = True

    while improved:
        improved = False
        best_distance = sum(dist_matrix[best_route[i - 1]][best_route[i]] for i in range(1, num_points))
        for i in range(1, num_points - 1):
            for k in range(i + 1, num_points):
                new_route = two_opt_swap(best_route, i, k)
                new_distance = sum(dist_matrix[new_route[j - 1]][new_route[j]] for j in range(1, num_points))
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True

    # Do not loop back to the start
    return [points[i] for i in best_route], best_distance


def simulated_annealing_tsp(points, dist_matrix):
    def total_distance(route):
        """Calculate the total distance of a route."""
        return sum(dist_matrix[route[i - 1]][route[i]] for i in range(1, len(route)))

    def random_swap(route):
        """Swap two random elements in the route."""
        a, b = random.sample(range(len(route)), 2)
        route[a], route[b] = route[b], route[a]
        return route

    current_route = list(range(len(points)))
    current_distance = total_distance(current_route)
    best_route = current_route
    best_distance = current_distance
    temperature = 1.0
    cooling_rate = 0.003

    while temperature > 0.01:
        new_route = random_swap(current_route[:])
        new_distance = total_distance(new_route)

        if new_distance < current_distance or random.uniform(0, 1) < math.exp(
                (current_distance - new_distance) / temperature):
            current_route = new_route
            current_distance = new_distance

            if current_distance < best_distance:
                best_route = current_route
                best_distance = current_distance

        temperature *= 1 - cooling_rate

    # Do not append the starting point again at the end
    return [points[i] for i in best_route], best_distance


def sorted_tree_tsp(points, dist_matrix):
    origin_index = 0
    sorted_indices = sorted(range(len(points)), key=lambda i: dist_matrix[origin_index][i])
    total_distance = sum(dist_matrix[sorted_indices[i]][sorted_indices[i+1]] for i in range(len(points)-1))
    sorted_points = [points[i] for i in sorted_indices]
    return sorted_points, total_distance


def generate_data(num_points, x_range=(0, 1000), y_range=(0, 1000)):
    return [(random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1])) for _ in range(num_points)]


# player_position = (1771, 1477)
# data = [(3277, 1748, 1491, 0), (3277, 1752, 1452, 0), (3277, 1764, 1485, 0), (3277, 1768, 1473, 0), (3277, 1772, 1491, 0), (3277, 1780, 1485, 0), (3277, 1784, 1458, 0), (3277, 1796, 1461, 0), (3280, 1748, 1464, 0), (3280, 1752, 1473, 0), (3280, 1752, 1488, 0), (3280, 1756, 1464, 0), (3280, 1756, 1470, 0), (3280, 1760, 1458, 0), (3280, 1760, 1491, 0), (3280, 1760, 1494, 0), (3280, 1768, 1479, 0), (3280, 1776, 1458, 0), (3280, 1776, 1497, 0), (3280, 1780, 1455, 0), (3280, 1780, 1461, 0), (3280, 1780, 1470, 0), (3280, 1784, 1497, 0), (3280, 1788, 1458, 0), (3280, 1788, 1461, 0), (3280, 1788, 1464, 0), (3280, 1788, 1485, 0), (3280, 1792, 1470, 0), (3280, 1796, 1485, 0), (3283, 1752, 1455, 0), (3283, 1752, 1476, 0), (3283, 1752, 1497, 0), (3283, 1752, 1500, 0), (3283, 1760, 1482, 0), (3283, 1768, 1467, 0), (3283, 1768, 1470, 0), (3283, 1780, 1482, 0), (3287, 1748, 1476, 0), (3287, 1760, 1497, 0), (3287, 1768, 1458, 0), (3287, 1768, 1491, 0), (3287, 1772, 1479, 0), (3287, 1780, 1479, 0), (3287, 1784, 1473, 0), (3287, 1784, 1479, 0), (3287, 1788, 1488, 0), (3287, 1788, 1497, 0), (3287, 1792, 1461, 0), (3287, 1792, 1476, 0), (3286, 1748, 1476, 0), (3286, 1760, 1497, 0), (3286, 1768, 1458, 0), (3286, 1768, 1491, 0), (3286, 1772, 1479, 0), (3286, 1780, 1479, 0), (3286, 1784, 1473, 0), (3286, 1784, 1479, 0), (3286, 1788, 1488, 0), (3286, 1788, 1497, 0), (3286, 1792, 1461, 0), (3286, 1792, 1476, 0), (3288, 1748, 1461, 0), (3288, 1748, 1473, 0), (3288, 1748, 1485, 0), (3288, 1748, 1494, 0), (3288, 1756, 1500, 0), (3288, 1764, 1500, 0), (3288, 1772, 1461, 0), (3288, 1772, 1488, 0), (3288, 1780, 1452, 0), (3288, 1784, 1500, 0), (3288, 1788, 1455, 0), (3288, 1792, 1464, 0), (3288, 1792, 1467, 0), (3288, 1796, 1467, 0), (3290, 1748, 1455, 0), (3290, 1756, 1461, 0), (3290, 1764, 1458, 0), (3290, 1764, 1464, 0), (3290, 1764, 1467, 0), (3290, 1768, 1494, 0), (3290, 1772, 1458, 0), (3290, 1772, 1470, 0), (3290, 1776, 1461, 0), (3290, 1784, 1467, 0), (3290, 1788, 1500, 0), (3293, 1760, 1476, 0), (3293, 1764, 1488, 0), (3293, 1768, 1461, 0), (3293, 1768, 1476, 0), (3293, 1768, 1482, 0), (3293, 1780, 1464, 0), (3293, 1780, 1467, 0), (3293, 1784, 1452, 0), (3293, 1792, 1482, 0), (3293, 1796, 1488, 0), (3296, 1748, 1467, 0), (3296, 1748, 1482, 0), (3296, 1748, 1488, 0), (3296, 1752, 1470, 0), (3296, 1752, 1491, 0), (3296, 1764, 1461, 0), (3296, 1772, 1452, 0), (3296, 1776, 1470, 0), (3296, 1776, 1479, 0), (3296, 1780, 1458, 0), (3296, 1780, 1473, 0), (3296, 1780, 1500, 0), (3296, 1784, 1461, 0), (3296, 1784, 1464, 0), (3296, 1784, 1491, 0), (3296, 1788, 1452, 0), (3296, 1788, 1491, 0), (3296, 1792, 1479, 0), (3296, 1796, 1458, 0), (3296, 1796, 1500, 0)]

player_position = (GetX(Self()), GetY(Self()))
data = get_tiles(50, trees)

dataset1, dataset1_steps, dataset1_time = adapted_tsp_algorithm(data, nearest_neighbor_tsp)
dataset2, dataset2_steps, dataset2_time = adapted_tsp_algorithm(data, sorted_tree_tsp,)
dataset3, dataset3_steps, dataset3_time = adapted_tsp_algorithm(data, greedy_tsp,)
dataset4, dataset4_steps, dataset4_time = adapted_tsp_algorithm(data, two_opt_tsp)
datasets = [dataset1, dataset2, dataset3, dataset4, ]
player_positions = [player_position, player_position, player_position, player_position]
titles = [
    f"nearest_neighbor_tsp, Length: {dataset1_steps}, Time: {dataset1_time}",
    f"sorted_tree_tsp, Length:  {dataset2_steps}, Time: {dataset2_time}",
    f"greedy_tsp, Length:  {dataset3_steps}, Time: {dataset3_time}",
    f"two_opt_tsp, Length:  {dataset4_steps}, Time: {dataset4_time}",
]
# Call the function to plot the maps
plot_multiple_tree_maps(datasets, player_positions, titles)
