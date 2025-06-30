"""
画像分割関連のクラス
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import os
from natsort import natsorted


class ImageSplitter:
    """画像を複数の画像に分割するクラス
    
    Attributes:
        width (int): 分割後の画像の幅
        height (int): 分割後の画像の高さ
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
    
    def split_image(self, image: np.ndarray) -> List[np.ndarray]:
        """画像を複数の画像に分割する
        
        Args:
            image (np.ndarray): 分割する画像
            
        Returns:
            List[np.ndarray]: 分割された画像のリスト
            
        Raises:
            ValueError: 画像サイズが分割サイズで割り切れない場合
        """
        h, w = image.shape[:2]
        rows = h // self.height
        columns = w // self.width
        
        if w % self.width != 0 or h % self.height != 0:
            raise ValueError(f"画像サイズ({w}x{h})が分割サイズ({self.width}x{self.height})で割り切れません")

        split_images = []
        for i in range(rows):
            for j in range(columns):
                top = i * self.height
                bottom = (i + 1) * self.height
                left = j * self.width
                right = (j + 1) * self.width
                cropped_image = image[top:bottom, left:right]
                split_images.append(cropped_image)
        
        return split_images


class VoronoiSplitter:
    """ボロノイ図とラベルを分割するクラス
    
    Attributes:
        splitter (Optional[ImageSplitter]): 画像分割器（設定で分割が有効な場合のみ）
    """
    
    def __init__(self, config: Dict[str, Any]):
        """初期化
        
        Args:
            config (Dict[str, Any]): 設定辞書
        """
        self.splitter = None
        if "split" in config:
            split_config = config["split"]
            self.splitter = ImageSplitter(
                split_config["split_width"], 
                split_config["split_height"]
            )

    def __call__(self, image: np.ndarray, label: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """画像とラベルを分割する
        
        Args:
            image (np.ndarray): 分割する画像
            label (np.ndarray): 分割するラベル
            
        Returns:
            Tuple[List[np.ndarray], List[np.ndarray]]: (分割された画像のリスト, 分割されたラベルのリスト)
            
        Note:
            config内にsplitが設定されている場合、画像とラベルを分割します。
            splitが設定されていない場合は、リストに変換して返します。
        """
        if self.splitter:
            image_list = self.splitter.split_image(image)
            label_list = self.splitter.split_image(label)
        else:
            image_list, label_list = [image], [label]
        
        return image_list, label_list
