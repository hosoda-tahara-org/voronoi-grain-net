"""
画像処理関連のクラス
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple
from perlin_numpy import generate_perlin_noise_2d
from .base import ImageProcessor


class CropProcessor(ImageProcessor):
    """画像を切り出すプロセッサー"""
    
    def __init__(self, crop_width: int = 2560, crop_height: int = 1536):
        self.crop_width = crop_width
        self.crop_height = crop_height
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """画像を中心から指定範囲を切り出す"""
        image_height, image_width = image.shape[:2]
        
        if self.crop_width > image_width or self.crop_height > image_height:
            raise ValueError("切り出しサイズが画像サイズより大きいです")
        
        top = (image_height - self.crop_height) // 2
        left = (image_width - self.crop_width) // 2
        
        return image[top:top + self.crop_height, left:left + self.crop_width]


class DefectProcessor(ImageProcessor):
    """欠陥を追加するプロセッサー"""
    
    def __init__(self, min_num: int = 0, max_num: int = 10, 
                 min_size: int = 10, max_size: int = 40, 
                 color: Tuple[int, int, int] = (0, 0, 0)):
        self.min_num = min_num
        self.max_num = max_num
        self.min_size = min_size
        self.max_size = max_size
        self.color = color
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """欠陥（ランダムな楕円）を追加する"""
        h, w = image.shape[:2]
        image_defected = image.copy()
        num_defects = np.random.randint(self.min_num, self.max_num + 1)
        
        for _ in range(num_defects):
            center = (np.random.randint(0, w), np.random.randint(0, h))
            size = (np.random.randint(self.min_size, self.max_size), 
                   np.random.randint(self.min_size, self.max_size))
            cv2.ellipse(image_defected, center, size, 0, 0, 360, self.color, -1)
        
        return image_defected


class GaussianNoiseProcessor(ImageProcessor):
    """ガウスノイズを追加するプロセッサー"""
    
    def __init__(self, mean: float = 0, std: float = 20):
        self.mean = mean
        self.std = std
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """ガウスノイズを追加する"""
        noise = np.random.normal(self.mean, self.std, image.shape)
        return self._apply_noise(image, noise)
    
    def _apply_noise(self, image: np.ndarray, noise: np.ndarray) -> np.ndarray:
        """画像にノイズを加えてクリッピング"""
        noised_image = image.astype(np.float64) + noise
        return np.clip(noised_image, 0, 255).astype(np.uint8)


class PerlinNoiseProcessor(ImageProcessor):
    """パーリンノイズを追加するプロセッサー"""
    
    def __init__(self, res: Tuple[int, int] = (32, 32), noise_range: float = 20):
        self.res = res
        self.noise_range = noise_range
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """パーリンノイズを追加する"""
        height, width = image.shape[:2]
        perlin_noise = generate_perlin_noise_2d((height, width), self.res)
        perlin_noise = np.interp(perlin_noise, 
                                (perlin_noise.min(), perlin_noise.max()), 
                                (-self.noise_range, self.noise_range))
        perlin_noise = perlin_noise[..., np.newaxis]  # チャネル次元追加
        return self._apply_noise(image, perlin_noise)
    
    def _apply_noise(self, image: np.ndarray, noise: np.ndarray) -> np.ndarray:
        """画像にノイズを加えてクリッピング"""
        noised_image = image.astype(np.float64) + noise
        return np.clip(noised_image, 0, 255).astype(np.uint8)


class ProcessorFactory:
    """プロセッサーを生成するファクトリークラス"""
    
    def __init__(self):
        self._processors = {
            "crop": CropProcessor,
            "defect": DefectProcessor,
            "gaussian_noise": GaussianNoiseProcessor,
            "perlin_noise": PerlinNoiseProcessor,
        }
        
    def create_processor(self, processor_type: str, **params) -> ImageProcessor:
        """プロセッサーを動的に生成"""
        if processor_type not in self._processors:
            raise ValueError(f"Unknown processor: {processor_type}")
        return self._processors[processor_type](**params)


class ImagePipeline:
    """画像処理パイプラインクラス"""
    
    def __init__(self, config: Dict[str, Any]):
        self.factory = ProcessorFactory()
        self.image_processors = []  # imageのみに適用
        self.both_processors = []   # 両方に適用
        
        # 設定からプロセッサーを順次構築
        for proc_config in config.get("post_processors", []):
            processor = self.factory.create_processor(
                proc_config["type"], 
                **proc_config.get("params", {})
            )
            
            # apply_toパラメータに基づいて分類
            apply_to = proc_config["apply_to"]
            if apply_to == "both":
                self.both_processors.append(processor)
            else:  # "image"の場合
                self.image_processors.append(processor)
    
    def process(self, image: np.ndarray, label: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """imageとlabelに適切にプロセッサーを適用"""
        # 両方に適用
        for processor in self.both_processors:
            image = processor.process(image)
            label = processor.process(label)
        
        # imageのみに適用
        for processor in self.image_processors:
            image = processor.process(image)
        
        return image, label 