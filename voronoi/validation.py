import yaml
import os
from typing import Dict, Any, List, Union
import sys

class VoronoiConfigValidator:
    """ボロノイ図生成設定ファイルのバリデーションを行うクラス"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """設定ファイル全体のバリデーション"""
        self.errors = []
        self.warnings = []
        
        # 必須セクションの存在チェック
        if "voronoi" not in config:
            self.errors.append("'voronoi' セクションが必須です")
            return False
        
        voronoi_config = config["voronoi"]
        
        # 各セクションのバリデーション
        self._validate_basic_settings(voronoi_config)
        self._validate_point_generation(voronoi_config)
        self._validate_image_info(voronoi_config)
        self._validate_post_processors(voronoi_config)
        self._validate_datatype_info(voronoi_config)
        self._validate_split_settings(voronoi_config)
        
        return len(self.errors) == 0
    
    def _validate_basic_settings(self, config: Dict[str, Any]):
        """基本設定のバリデーション"""
        # width
        if "width" not in config:
            self.errors.append("'width' が必須です")
        elif not isinstance(config["width"], int) or config["width"] <= 0:
            self.errors.append("'width' は正の整数である必要があります")
        
        # height
        if "height" not in config:
            self.errors.append("'height' が必須です")
        elif not isinstance(config["height"], int) or config["height"] <= 0:
            self.errors.append("'height' は正の整数である必要があります")
        
        # output_dir
        if "output_dir" not in config:
            self.errors.append("'output_dir' が必須です")
        elif not isinstance(config["output_dir"], str):
            self.errors.append("'output_dir' は文字列である必要があります")
    
    def _validate_point_generation(self, config: Dict[str, Any]):
        """母点生成設定のバリデーション"""
        if "point_generation" not in config:
            self.errors.append("'point_generation' セクションが必須です")
            return
        
        pg_config = config["point_generation"]
        
        # method
        if "method" not in pg_config:
            self.errors.append("'point_generation.method' が必須です")
        elif pg_config["method"] not in ["random", "poisson_disk"]:
            self.errors.append("'point_generation.method' は 'random' または 'poisson_disk' である必要があります")
        
        # params
        if "params" not in pg_config:
            self.errors.append("'point_generation.params' が必須です")
        else:
            params = pg_config["params"]
            method = pg_config.get("method", "")
            
            if method == "random":
                if "points_num" not in params:
                    self.errors.append("'random' メソッドでは 'points_num' が必須です")
                elif not isinstance(params["points_num"], list):
                    self.errors.append("'points_num' はリストである必要があります")
                elif not all(isinstance(x, int) and x > 0 for x in params["points_num"]):
                    self.errors.append("'points_num' の各要素は正の整数である必要があります")
            
            elif method == "poisson_disk":
                if "min_distance" not in params:
                    self.errors.append("'poisson_disk' メソッドでは 'min_distance' が必須です")
                elif not isinstance(params["min_distance"], list):
                    self.errors.append("'min_distance' はリストである必要があります")
                elif not all(isinstance(x, (int, float)) and x > 0 for x in params["min_distance"]):
                    self.errors.append("'min_distance' の各要素は正の数である必要があります")
                
                if "max_attempts" in params:
                    if not isinstance(params["max_attempts"], int) or params["max_attempts"] <= 0:
                        self.errors.append("'max_attempts' は正の整数である必要があります")
        
    def _validate_image_info(self, config: Dict[str, Any]):
        """画像情報のバリデーション"""
        if "image_info" not in config:
            self.errors.append("'image_info' セクションが必須です")
            return
        
        image_config = config["image_info"]
        
        # method
        if "method" not in image_config:
            self.errors.append("'image_info.method' が必須です")
        elif image_config["method"] not in ["uniform", "gaussian"]:
            self.errors.append("'image_info.method' は 'uniform' または 'gaussian' である必要があります")
        
        # params (gaussianの場合)
        if image_config.get("method") == "gaussian":
            if "params" not in image_config:
                self.errors.append("'gaussian' メソッドでは 'image_info.params' が必須です")
            else:
                params = image_config["params"]
                if "mean" not in params:
                    self.errors.append("'gaussian' メソッドでは 'mean' が必須です")
                elif not isinstance(params["mean"], (int, float)) or not (0 <= params["mean"] <= 255):
                    self.errors.append("'mean' は0-255の数値である必要があります")
                
                if "std" not in params:
                    self.errors.append("'gaussian' メソッドでは 'std' が必須です")
                elif not isinstance(params["std"], (int, float)) or params["std"] <= 0:
                    self.errors.append("'std' は正の数値である必要があります")
    
    def _validate_post_processors(self, config: Dict[str, Any]):
        """後処理プロセッサーのバリデーション"""
        if "post_processors" not in config:
            self.warnings.append("'post_processors' セクションがありません（後処理は適用されません）")
            return
        
        processors = config["post_processors"]
        if not isinstance(processors, list):
            self.errors.append("'post_processors' はリストである必要があります")
            return
        
        valid_types = ["crop", "defect", "gaussian_noise", "perlin_noise"]
        valid_apply_to = ["image", "label", "both"]
        
        for i, processor in enumerate(processors):
            if not isinstance(processor, dict):
                self.errors.append(f"post_processors[{i}] は辞書である必要があります")
                continue
            
            # type
            if "type" not in processor:
                self.errors.append(f"post_processors[{i}].type が必須です")
            elif processor["type"] not in valid_types:
                self.errors.append(f"post_processors[{i}].type は {valid_types} のいずれかである必要があります")
            
            # apply_to
            if "apply_to" not in processor:
                self.errors.append(f"post_processors[{i}].apply_to が必須です")
            elif processor["apply_to"] not in valid_apply_to:
                self.errors.append(f"post_processors[{i}].apply_to は {valid_apply_to} のいずれかである必要があります")
            
            # params
            if "params" not in processor:
                self.errors.append(f"post_processors[{i}].params が必須です")
            else:
                self._validate_processor_params(processor["type"], processor["params"], i)
    
    def _validate_processor_params(self, processor_type: str, params: Dict[str, Any], index: int):
        """プロセッサー固有のパラメータバリデーション"""
        if processor_type == "crop":
            if "crop_width" not in params:
                self.errors.append(f"post_processors[{index}].params.crop_width が必須です")
            elif not isinstance(params["crop_width"], int) or params["crop_width"] <= 0:
                self.errors.append(f"post_processors[{index}].params.crop_width は正の整数である必要があります")
            
            if "crop_height" not in params:
                self.errors.append(f"post_processors[{index}].params.crop_height が必須です")
            elif not isinstance(params["crop_height"], int) or params["crop_height"] <= 0:
                self.errors.append(f"post_processors[{index}].params.crop_height は正の整数である必要があります")
        
        elif processor_type == "defect":
            required_params = ["min_num", "max_num", "min_size", "max_size", "color"]
            for param in required_params:
                if param not in params:
                    self.errors.append(f"post_processors[{index}].params.{param} が必須です")
            
            if "min_num" in params and "max_num" in params:
                if not isinstance(params["min_num"], int) or params["min_num"] < 0:
                    self.errors.append(f"post_processors[{index}].params.min_num は0以上の整数である必要があります")
                if not isinstance(params["max_num"], int) or params["max_num"] < 0:
                    self.errors.append(f"post_processors[{index}].params.max_num は0以上の整数である必要があります")
                if params["min_num"] > params["max_num"]:
                    self.errors.append(f"post_processors[{index}].params.min_num は max_num 以下である必要があります")
            
            if "min_size" in params and "max_size" in params:
                if not isinstance(params["min_size"], int) or params["min_size"] <= 0:
                    self.errors.append(f"post_processors[{index}].params.min_size は正の整数である必要があります")
                if not isinstance(params["max_size"], int) or params["max_size"] <= 0:
                    self.errors.append(f"post_processors[{index}].params.max_size は正の整数である必要があります")
                if params["min_size"] > params["max_size"]:
                    self.errors.append(f"post_processors[{index}].params.min_size は max_size 以下である必要があります")
            
            if "color" in params:
                if not isinstance(params["color"], list) or len(params["color"]) != 3:
                    self.errors.append(f"post_processors[{index}].params.color は3要素のリストである必要があります")
                elif not all(isinstance(x, int) and 0 <= x <= 255 for x in params["color"]):
                    self.errors.append(f"post_processors[{index}].params.color の各要素は0-255の整数である必要があります")
        
        elif processor_type == "gaussian_noise":
            if "mean" not in params:
                self.errors.append(f"post_processors[{index}].params.mean が必須です")
            elif not isinstance(params["mean"], (int, float)):
                self.errors.append(f"post_processors[{index}].params.mean は数値である必要があります")
            
            if "std" not in params:
                self.errors.append(f"post_processors[{index}].params.std が必須です")
            elif not isinstance(params["std"], (int, float)) or params["std"] <= 0:
                self.errors.append(f"post_processors[{index}].params.std は正の数値である必要があります")
        
        elif processor_type == "perlin_noise":
            if "res" not in params:
                self.errors.append(f"post_processors[{index}].params.res が必須です")
            elif not isinstance(params["res"], list) or len(params["res"]) != 2:
                self.errors.append(f"post_processors[{index}].params.res は2要素のリストである必要があります")
            elif not all(isinstance(x, int) and x > 0 for x in params["res"]):
                self.errors.append(f"post_processors[{index}].params.res の各要素は正の整数である必要があります")
            
            if "noise_range" not in params:
                self.errors.append(f"post_processors[{index}].params.noise_range が必須です")
            elif not isinstance(params["noise_range"], (int, float)) or params["noise_range"] <= 0:
                self.errors.append(f"post_processors[{index}].params.noise_range は正の数値である必要があります")
    
    def _validate_datatype_info(self, config: Dict[str, Any]):
        """データタイプ情報のバリデーション"""
        if "datatype_info" not in config:
            self.errors.append("'datatype_info' セクションが必須です")
            return
        
        datatype_config = config["datatype_info"]
        if not isinstance(datatype_config, dict):
            self.errors.append("'datatype_info' は辞書である必要があります")
            return
        
        for datatype, params in datatype_config.items():
            if not isinstance(params, dict):
                self.errors.append(f"datatype_info.{datatype} は辞書である必要があります")
                continue
            
            # diagram_num
            if "diagram_num" not in params:
                self.errors.append(f"datatype_info.{datatype}.diagram_num が必須です")
            elif not isinstance(params["diagram_num"], int) or params["diagram_num"] <= 0:
                self.errors.append(f"datatype_info.{datatype}.diagram_num は正の整数である必要があります")
            
            # seed
            if "seed" not in params:
                self.errors.append(f"datatype_info.{datatype}.seed が必須です")
            elif not isinstance(params["seed"], int):
                self.errors.append(f"datatype_info.{datatype}.seed は整数である必要があります")
    
    def _validate_split_settings(self, config: Dict[str, Any]):
        """分割設定のバリデーション"""
        if "split" not in config:
            self.errors.append("'split' セクションが必須です")
            return
        
        split_config = config["split"]
        
        # split_width
        if "split_width" not in split_config:
            self.errors.append("'split.split_width' が必須です")
        elif not isinstance(split_config["split_width"], int) or split_config["split_width"] <= 0:
            self.errors.append("'split.split_width' は正の整数である必要があります")
        
        # split_height
        if "split_height" not in split_config:
            self.errors.append("'split.split_height' が必須です")
        elif not isinstance(split_config["split_height"], int) or split_config["split_height"] <= 0:
            self.errors.append("'split.split_height' は正の整数である必要があります")
        
        # 分割サイズが元画像サイズより大きい場合の警告
        if "width" in config and "height" in config:
            if split_config.get("split_width", 0) > config["width"]:
                self.warnings.append("split_width が元画像の width より大きいです")
            if split_config.get("split_height", 0) > config["height"]:
                self.warnings.append("split_height が元画像の height より大きいです")
    
    def get_errors(self) -> List[str]:
        """エラーメッセージのリストを取得"""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """警告メッセージのリストを取得"""
        return self.warnings
    
    def print_validation_results(self):
        """バリデーション結果を出力"""
        if self.errors:
            print("❌ バリデーションエラー:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("⚠️  警告:")
            for warning in self.warnings:
                print(f"  - {warning}")

def validate_yaml_file(config_file: str) -> bool:
    """YAMLファイルをバリデーションする関数"""
    try:
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
        validator = VoronoiConfigValidator()
        is_valid = validator.validate_config(config)
        
        validator.print_validation_results()
        return is_valid
        
    except yaml.YAMLError as e:
        print(f"❌ YAMLファイルの解析エラー: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {config_file}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python validation.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    is_valid = validate_yaml_file(config_file)
    
    if not is_valid:
        sys.exit(1) 