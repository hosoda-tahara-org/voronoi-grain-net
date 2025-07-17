"""
Classes related to seed point generation
"""

import numpy as np
from .base import PointGenerator


class RandomPointGenerator(PointGenerator):
    """Generator for completely random seed points"""
    
    def generate(self, width: int, height: int, **kwargs) -> np.ndarray:
        if "points_num" not in kwargs:
            raise ValueError("points_num is required for RandomPointGenerator")
        points_num = kwargs["points_num"]
        return np.random.randint(0, [height, width], (points_num, 2))


class PoissonDiskPointGenerator(PointGenerator):
    """Generator for seed points using Poisson disk sampling"""
    
    def generate(self, width: int, height: int, **kwargs) -> np.ndarray:
        if "min_distance" not in kwargs:
            raise ValueError("min_distance is required for PoissonDiskPointGenerator")
        if "max_attempts" not in kwargs:
            raise ValueError("max_attempts is required for PoissonDiskPointGenerator")
        
        min_distance = kwargs["min_distance"]
        max_attempts = kwargs["max_attempts"]
        
        points = np.empty((0, 2), dtype=int)
        attempts = 0
        min_distance_squared = min_distance ** 2
        
        while attempts < max_attempts:
            new_point = np.random.randint(0, [height, width], 2)
            
            if len(points) == 0:  # Add the first point unconditionally
                points = np.vstack([points, new_point])
                attempts = 0
            else:
                distances_squared = np.sum((points - new_point) ** 2, axis=1)
                if np.all(distances_squared >= min_distance_squared):
                    points = np.vstack([points, new_point])
                    attempts = 0
                else:
                    attempts += 1
        
        return points


class PointGeneratorFactory:
    """Factory class for creating seed point generators"""
    
    def create_generator(self, method: str, **params) -> PointGenerator:
        """Dynamically create a seed point generator"""
        if method == "random":
            return RandomPointGenerator()
        elif method == "poisson_disk":
            return PoissonDiskPointGenerator()
        else:
            raise ValueError(f"Unknown point generation method: {method}")
