"""
グレースケール値生成関連のクラス
"""

import numpy as np
from .base import GrayValueGenerator


class UniformGrayGenerator(GrayValueGenerator):
    """一様分布によるグレースケール値生成"""
    
    def generate(self) -> int:
        """一様分布でグレースケール値を生成する"""
        return np.random.randint(0, 256)


class GaussianGrayGenerator(GrayValueGenerator):
    """ガウス分布によるグレースケール値生成"""
    
    def __init__(self, mean: int = 128, std: int = 32):
        self.mean = mean
        self.std = std
    
    def generate(self) -> int:
        """ガウス分布でグレースケール値を生成する"""
        while True:
            gray = np.random.normal(self.mean, self.std)
            if 0 <= gray <= 255:
                return int(gray)


class GrayValueFactory:
    """グレースケール値生成器のファクトリークラス"""
    
    def create_generator(self, distribution: str, **params) -> GrayValueGenerator:
        """グレースケール値生成器を動的に生成"""
        if distribution == "uniform":
            return UniformGrayGenerator(**params)
        elif distribution == "gaussian":
            return GaussianGrayGenerator(**params)
        else:
            raise ValueError(f"Unknown distribution: {distribution}") 