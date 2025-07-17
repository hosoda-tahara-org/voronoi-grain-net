"""
Basic structure and abstract classes for Voronoi diagram generation
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List


class PointGenerator(ABC):
    """Abstract base class for generating seed points"""

    @abstractmethod
    def generate(self, width: int, height: int, **kwargs) -> np.ndarray:
        """Generate seed points"""
        pass


class GrayValueGenerator(ABC):
    """Abstract base class for generating grayscale values"""

    @abstractmethod
    def generate(self) -> int:
        """Generate a grayscale value"""
        pass


class ImageProcessor(ABC):
    """Abstract base class for image processing"""
    
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """Process the image"""
        pass
