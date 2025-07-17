"""
Classes related to grayscale value generation
"""

import numpy as np
from .base import GrayValueGenerator


class UniformGrayGenerator(GrayValueGenerator):
    """Grayscale value generator using a uniform distribution"""
    
    def generate(self) -> int:
        return np.random.randint(0, 256)


class GaussianGrayGenerator(GrayValueGenerator):
    """Grayscale value generator using a Gaussian distribution"""
    
    def __init__(self, mean: int = 128, std: int = 32):
        self.mean = mean
        self.std = std
    
    def generate(self) -> int:
        while True:
            gray = np.random.normal(self.mean, self.std)
            if 0 <= gray <= 255:
                return int(gray)


class GrayValueFactory:
    """Factory class for creating grayscale value generators"""
    
    def create_generator(self, distribution: str, **params) -> GrayValueGenerator:
        """Dynamically create a grayscale value generator"""
        if distribution == "uniform":
            return UniformGrayGenerator(**params)
        elif distribution == "gaussian":
            return GaussianGrayGenerator(**params)
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
