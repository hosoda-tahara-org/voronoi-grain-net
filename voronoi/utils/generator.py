"""
ボロノイ図生成のメインクラス
"""

import numpy as np
from typing import Dict, Any, Tuple
from .point_generators import PointGeneratorFactory
from .gray_generators import GrayValueFactory
from .calculators import VoronoiCalculator
from .renderers import ImageRenderer
from .processors import ImagePipeline


class VoronoiGenerator:
    """ボロノイ図生成のメインクラス
    
    Attributes:
        width (int): 画像の幅
        height (int): 画像の高さ
        point_generator (PointGenerator): 母点生成器
        label_info (Dict): ラベル描画設定
        gray_generator (GrayValueGenerator): グレースケール値生成器
        voronoi_calculator (VoronoiCalculator): ボロノイ計算器
        image_renderer (ImageRenderer): 画像描画器
        image_pipeline (ImagePipeline): 画像処理パイプライン
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.width = config["width"]
        self.height = config["height"]
        
        # 母点生成器を初期化
        method = config["point_generation"]["method"]
        self.point_generator = PointGeneratorFactory().create_generator(
            method, 
            **config["point_generation"]["params"]
        )
        
        # 描画設定
        self.label_info = config.get("label_info", {})
        
        # グレースケール値生成器を初期化
        image_info = config["image_info"]
        self.gray_generator = GrayValueFactory().create_generator(
            image_info["method"],
            **image_info.get("params", {})
        )

        # その他のコンポーネントを初期化
        self.voronoi_calculator = VoronoiCalculator(self.width, self.height)
        self.image_renderer = ImageRenderer(self.width, self.height)
        self.image_pipeline = ImagePipeline(config)
    
    def generate(self, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """ボロノイ図を生成する
        
        Args:
            **kwargs: 母点生成の動的パラメータ
                - ランダム生成の場合: points_num
                - ポアソンディスクの場合: min_distance, max_attempts
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: (画像, ラベル)のタプル
        """
        # 母点生成
        points = self.point_generator.generate(self.width, self.height, **kwargs)
        
        # ボロノイ計算
        facets = self.voronoi_calculator.calculate(points)
        
        # 画像描画
        voronoi_label = self.image_renderer.render_voronoi_label(facets, **self.label_info)
        voronoi_image = self.image_renderer.render_voronoi_image(facets, self.gray_generator)
        
        # 後処理（imageとlabelの両方に適用）
        voronoi_image, voronoi_label = self.image_pipeline.process_both(voronoi_image, voronoi_label)
        
        return voronoi_image, voronoi_label 