"""
ボロノイ図生成パッケージ

このパッケージは、設定ファイルに基づいてボロノイ図を生成するための
モジュラーなアーキテクチャを提供します。

主要なクラス:
    - VoronoiGenerator: メインの生成クラス
    - PointGeneratorFactory: 母点生成器のファクトリー
    - GrayValueFactory: グレースケール値生成器のファクトリー
    - ImagePipeline: 画像処理パイプライン
"""

from .generator import VoronoiGenerator
from .point_generators import PointGeneratorFactory
from .gray_generators import GrayValueFactory
from .processors import ImagePipeline

__all__ = [
    'VoronoiGenerator',
    'PointGeneratorFactory', 
    'GrayValueFactory',
    'ImagePipeline'
]

__version__ = "1.0.0"
