"""
Test code for Voronoi diagram generation
"""

import numpy as np
import matplotlib.pyplot as plt
from utils.generator import VoronoiGenerator

if __name__ == "__main__":
    WIDTH, HEIGHT = 2560, 1536
    RANDOM_SEED = 1

    np.random.seed(RANDOM_SEED)
    
    # Example configuration 1: Random generation
    config_random = {
        "width": WIDTH,
        "height": HEIGHT,
        "point_generation": {
            "method": "random",
            "params": {
                "points_num": [1000, 800, 600, 400, 200]
            }
        },
        "label_info": {"color": (255, 255, 255), "thickness": 2},
        "image_info": {
            "method": "gaussian",
            "params": {"mean": 128, "std": 32}
        },
        "post_processors": [
            {"type": "crop", "params": {"crop_width": 2560, "crop_height": 1536}, "apply_to": "both"},
            {"type": "elliptical_mask", "params": {"min_num": 0, "max_num": 10}, "apply_to": "image"},
            {"type": "gaussian_noise", "params": {"mean": 0, "std": 20}, "apply_to": "image"},
            {"type": "perlin_noise", "params": {"res": [32, 32], "noise_range": 20}, "apply_to": "image"},
        ]
    }
    
    # Example configuration 2: Poisson disk sampling
    config_poisson = {
        "width": WIDTH,
        "height": HEIGHT,
        "point_generation": {
            "method": "poisson_disk",
            "params": {
                "min_distance": [30, 50, 70, 90, 110],
                "max_attempts": 100
            }
        },
        "label_info": {"color": (255, 255, 255), "thickness": 2},
        "image_info": {
            "method": "gaussian",
            "params": {"mean": 128, "std": 32}
        },
        "post_processors": [
            {"type": "crop", "params": {"crop_width": 2560, "crop_height": 1536}, "apply_to": "both"},
            {"type": "elliptical_mask", "params": {"min_num": 0, "max_num": 10}, "apply_to": "image"},
            {"type": "gaussian_noise", "params": {"mean": 0, "std": 20}, "apply_to": "image"},
            {"type": "perlin_noise", "params": {"res": [32, 32], "noise_range": 20}, "apply_to": "image"},
        ]
    }
    
    # Test with random generation (multiple times with different parameters)
    print("Testing Random Point Generation...")
    voronoi_random = VoronoiGenerator(config_random)
    
    plt.figure(figsize=(15, 10))
    for i in range(5):
        points_num = config_random["point_generation"]["params"]["points_num"][i]
        voronoi_image_random, voronoi_label_random = voronoi_random.generate(points_num=points_num)
        
        plt.subplot(2, 5, i + 1)
        plt.imshow(voronoi_label_random, cmap="gray")
        plt.title(f"Random Label {i+1}\n(points: {points_num})")
        plt.axis("off")
        
        plt.subplot(2, 5, i + 6)
        plt.imshow(voronoi_image_random, cmap="gray")
        plt.title(f"Random Image {i+1}\n(points: {points_num})")
        plt.axis("off")
    
    plt.tight_layout()
    plt.show()
    
    # Test with Poisson disk (multiple times with different parameters)
    print("Testing Poisson Disk Point Generation...")
    voronoi_poisson = VoronoiGenerator(config_poisson)
    
    plt.figure(figsize=(15, 10))
    for i in range(5):
        min_distance = config_poisson["point_generation"]["params"]["min_distance"][i]
        voronoi_image_poisson, voronoi_label_poisson = voronoi_poisson.generate(min_distance=min_distance)
        
        plt.subplot(2, 5, i + 1)
        plt.imshow(voronoi_label_poisson, cmap="gray")
        plt.title(f"Poisson Label {i+1}\n(dist: {min_distance})")
        plt.axis("off")
        
        plt.subplot(2, 5, i + 6)
        plt.imshow(voronoi_image_poisson, cmap="gray")
        plt.title(f"Poisson Image {i+1}\n(dist: {min_distance})")
        plt.axis("off")
    
    plt.tight_layout()
    plt.show()
