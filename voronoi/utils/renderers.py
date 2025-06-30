"""
画像描画関連のクラス
"""

import cv2
import numpy as np
from typing import List, Tuple
from .base import GrayValueGenerator


class ImageRenderer:
    """画像を描画するクラス"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
    
    def create_initial_image(self, grayscale_value: int = 0) -> np.ndarray:
        """初期画像を作成する"""
        return np.full((self.height, self.width, 1), grayscale_value, dtype=np.uint8)
    
    def render_voronoi_image(self, facets: List[np.ndarray], 
                           gray_generator: GrayValueGenerator) -> np.ndarray:
        """ボロノイ領域を着色した画像を作成する"""
        voronoi_image = self.create_initial_image()
        
        for facet in facets:
            random_gray = gray_generator.generate()
            cv2.fillConvexPoly(voronoi_image, facet, (random_gray))
        
        return voronoi_image
    
    def render_voronoi_label(self, facets: List[np.ndarray], 
                           color: Tuple[int, int, int] = (255, 255, 255), 
                           thickness: int = 2) -> np.ndarray:
        """正解ラベルを作成する"""
        voronoi_label = self.create_initial_image()
        cv2.polylines(voronoi_label, facets, True, color, thickness=thickness)
        return voronoi_label
    
    def draw_points(self, image: np.ndarray, points: np.ndarray, 
                   radius: int = 4, color: Tuple[int, int, int] = (255, 255, 255), 
                   thickness: int = -1) -> np.ndarray:
        """画像上に母点を描画する（可視化用）"""
        for y, x in points:
            cv2.circle(image, (x, y), radius, color, thickness)
        return image 