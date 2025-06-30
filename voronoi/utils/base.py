"""
ボロノイ図生成の基本構造と抽象クラス
"""

import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List


class PointGenerator(ABC):
    """母点生成の抽象基底クラス"""
    
    @abstractmethod
    def generate(self, width: int, height: int, **kwargs) -> np.ndarray:
        """母点を生成する"""
        pass


class GrayValueGenerator(ABC):
    """グレースケール値生成の抽象基底クラス"""
    
    @abstractmethod
    def generate(self) -> int:
        """グレースケール値を生成する"""
        pass


class ImageProcessor(ABC):
    """画像処理の抽象基底クラス"""
    
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """画像を処理する"""
        pass 