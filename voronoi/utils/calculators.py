"""
Classes related to Voronoi diagram computation
"""

import cv2
import numpy as np
from typing import List


class VoronoiCalculator:
    """Class for computing Voronoi diagrams"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
    
    def calculate(self, points: np.ndarray) -> List[np.ndarray]:
        subdiv = cv2.Subdiv2D((0, 0, self.width, self.height))
        for y, x in points:
            subdiv.insert((x.astype(float), y.astype(float)))
        facets, _ = subdiv.getVoronoiFacetList([])
        return [f.astype(int) for f in facets]
