import random
from math import sqrt, floor

import pandas as pd
import numpy as np
from PIL import Image

# From a sample of (x, y) points, each belonging to one of two categories, figure out which areas of the (x, y) domain correspond with each label
# However, in this example, they are randomly generated, so there's not much of a pattern
def do_k_nearest_neighbor(resolution, data_points_count, k_selections_count):
    data = [(random.random() * 2 - 1, random.random() * 2 - 1, random.choice([True, False])) for _ in range(data_points_count)]
    grid_result = np.array([[None] * resolution] * resolution)

    colors = {True: [150, 30, 20], False: [20, 30, 150]}
    point_colors = {True: [230, 50, 30], False: [30, 50, 230]}

    for x in range(resolution):
        x_coord = x / (resolution / 2) - 1
        print(f"Working: {round(x / resolution * 100, 2)} %")
        for y in range(resolution):
            y_coord = y / (resolution / 2) - 1

            distances = [(i, point, sqrt((point[0] - x_coord) ** 2 + (point[1] - y_coord) ** 2)) for i, point in zip(range(data_points_count), data)]
            distances_sorted = sorted(distances, key=lambda x: x[2])
            closest_k = distances_sorted[0:k_selections_count]
            count_true = len([x for x in closest_k if x[1][2] is True])
            count_false = len([x for x in closest_k if x[1][2] is False])
            grid_result[x][y] = True if count_true > count_false else False

    image_array = np.array([[[0, 0, 0]] * resolution] * resolution, dtype='uint8')
    for x in range(resolution):
        for y in range(resolution):
            image_array[x][y] = colors[grid_result[x][y]]

    for point in data:
        x_int = floor((point[0] + 1) * (resolution / 2))
        y_int = floor((point[1] + 1) * (resolution / 2))

        # plot a 5x5 square for each point
        for x_coord in range(5):
            x_to_plot = x_int + x_coord - 2
            if x_to_plot < 0 or x_to_plot >= resolution:
                continue
            for y_coord in range(5):
                y_to_plot = y_int + y_coord - 2
                if y_to_plot < 0 or y_to_plot >= resolution:
                    continue
                image_array[x_to_plot][y_to_plot] = point_colors[point[2]]

    image = Image.fromarray(image_array, mode='RGB')
    image.save(f"outputs/k-nearest-neighbors_{resolution}x{resolution}_{data_points_count}pts_k{k_selections_count}.png")
    #grid_df = pd.DataFrame(data=grid_result, columns=range(resolution))

if __name__ == "__main__":
    do_k_nearest_neighbor(400, 50, 5)
    print("done")



