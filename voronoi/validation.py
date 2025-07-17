import yaml
import os
from typing import Dict, Any, List, Union
import sys

class VoronoiConfigValidator:
    """Class for validating Voronoi diagram generation configuration files"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate the entire configuration file"""
        self.errors = []
        self.warnings = []
        
        # Check for required sections
        if "voronoi" not in config:
            self.errors.append("'voronoi' section is required")
            return False
        
        voronoi_config = config["voronoi"]
        
        # Validate each section
        self._validate_basic_settings(voronoi_config)
        self._validate_point_generation(voronoi_config)
        self._validate_image_info(voronoi_config)
        self._validate_post_processors(voronoi_config)
        self._validate_datatype_info(voronoi_config)
        self._validate_split_settings(voronoi_config)
        
        return len(self.errors) == 0
    
    def _validate_basic_settings(self, config: Dict[str, Any]):
        """Validate basic settings"""
        # width
        if "width" not in config:
            self.errors.append("'width' is required")
        elif not isinstance(config["width"], int) or config["width"] <= 0:
            self.errors.append("'width' must be a positive integer")
        
        # height
        if "height" not in config:
            self.errors.append("'height' is required")
        elif not isinstance(config["height"], int) or config["height"] <= 0:
            self.errors.append("'height' must be a positive integer")
        
        # output_dir
        if "output_dir" not in config:
            self.errors.append("'output_dir' is required")
        elif not isinstance(config["output_dir"], str):
            self.errors.append("'output_dir' must be a string")
    
    def _validate_point_generation(self, config: Dict[str, Any]):
        """Validate point generation settings"""
        if "point_generation" not in config:
            self.errors.append("'point_generation' section is required")
            return
        
        pg_config = config["point_generation"]
        
        # method
        if "method" not in pg_config:
            self.errors.append("'point_generation.method' is required")
        elif pg_config["method"] not in ["random", "poisson_disk"]:
            self.errors.append("'point_generation.method' must be 'random' or 'poisson_disk'")
        
        # params
        if "params" not in pg_config:
            self.errors.append("'point_generation.params' is required")
        else:
            params = pg_config["params"]
            method = pg_config.get("method", "")
            
            if method == "random":
                if "points_num" not in params:
                    self.errors.append("'points_num' is required for 'random' method")
                elif not isinstance(params["points_num"], list):
                    self.errors.append("'points_num' must be a list")
                elif not all(isinstance(x, int) and x > 0 for x in params["points_num"]):
                    self.errors.append("Each element of 'points_num' must be a positive integer")
            
            elif method == "poisson_disk":
                if "min_distance" not in params:
                    self.errors.append("'min_distance' is required for 'poisson_disk' method")
                elif not isinstance(params["min_distance"], list):
                    self.errors.append("'min_distance' must be a list")
                elif not all(isinstance(x, (int, float)) and x > 0 for x in params["min_distance"]):
                    self.errors.append("Each element of 'min_distance' must be a positive number")
                
                if "max_attempts" in params:
                    if not isinstance(params["max_attempts"], int) or params["max_attempts"] <= 0:
                        self.errors.append("'max_attempts' must be a positive integer")
        
    def _validate_image_info(self, config: Dict[str, Any]):
        """Validate image information"""
        if "image_info" not in config:
            self.errors.append("'image_info' section is required")
            return
        
        image_config = config["image_info"]
        
        # method
        if "method" not in image_config:
            self.errors.append("'image_info.method' is required")
        elif image_config["method"] not in ["uniform", "gaussian"]:
            self.errors.append("'image_info.method' must be 'uniform' or 'gaussian'")
        
        # params (for gaussian)
        if image_config.get("method") == "gaussian":
            if "params" not in image_config:
                self.errors.append("'image_info.params' is required for 'gaussian' method")
            else:
                params = image_config["params"]
                if "mean" not in params:
                    self.errors.append("'mean' is required for 'gaussian' method")
                elif not isinstance(params["mean"], (int, float)) or not (0 <= params["mean"] <= 255):
                    self.errors.append("'mean' must be a number between 0-255")
                
                if "std" not in params:
                    self.errors.append("'std' is required for 'gaussian' method")
                elif not isinstance(params["std"], (int, float)) or params["std"] <= 0:
                    self.errors.append("'std' must be a positive number")
    
    def _validate_post_processors(self, config: Dict[str, Any]):
        """Validate post-processors"""
        if "post_processors" not in config:
            self.warnings.append("'post_processors' section is missing (no post-processing will be applied)")
            return
        
        processors = config["post_processors"]
        if not isinstance(processors, list):
            self.errors.append("'post_processors' must be a list")
            return
        
        valid_types = ["crop", "elliptical_mask", "gaussian_noise", "perlin_noise"]
        valid_apply_to = ["image", "label", "both"]
        
        for i, processor in enumerate(processors):
            if not isinstance(processor, dict):
                self.errors.append(f"post_processors[{i}] must be a dictionary")
                continue
            
            # type
            if "type" not in processor:
                self.errors.append(f"post_processors[{i}].type is required")
            elif processor["type"] not in valid_types:
                self.errors.append(f"post_processors[{i}].type must be one of {valid_types}")
            
            # apply_to
            if "apply_to" not in processor:
                self.errors.append(f"post_processors[{i}].apply_to is required")
            elif processor["apply_to"] not in valid_apply_to:
                self.errors.append(f"post_processors[{i}].apply_to must be one of {valid_apply_to}")
            
            # params
            if "params" not in processor:
                self.errors.append(f"post_processors[{i}].params is required")
            else:
                self._validate_processor_params(processor["type"], processor["params"], i)
    
    def _validate_processor_params(self, processor_type: str, params: Dict[str, Any], index: int):
        """Validate processor-specific parameters"""
        if processor_type == "crop":
            if "crop_width" not in params:
                self.errors.append(f"post_processors[{index}].params.crop_width is required")
            elif not isinstance(params["crop_width"], int) or params["crop_width"] <= 0:
                self.errors.append(f"post_processors[{index}].params.crop_width must be a positive integer")
            
            if "crop_height" not in params:
                self.errors.append(f"post_processors[{index}].params.crop_height is required")
            elif not isinstance(params["crop_height"], int) or params["crop_height"] <= 0:
                self.errors.append(f"post_processors[{index}].params.crop_height must be a positive integer")
        
        elif processor_type == "elliptical_mask":
            required_params = ["min_num", "max_num", "min_size", "max_size", "color"]
            for param in required_params:
                if param not in params:
                    self.errors.append(f"post_processors[{index}].params.{param} is required")
            
            if "min_num" in params and "max_num" in params:
                if not isinstance(params["min_num"], int) or params["min_num"] < 0:
                    self.errors.append(f"post_processors[{index}].params.min_num must be a non-negative integer")
                if not isinstance(params["max_num"], int) or params["max_num"] < 0:
                    self.errors.append(f"post_processors[{index}].params.max_num must be a non-negative integer")
                if params["min_num"] > params["max_num"]:
                    self.errors.append(f"post_processors[{index}].params.min_num must be less than or equal to max_num")
            
            if "min_size" in params and "max_size" in params:
                if not isinstance(params["min_size"], int) or params["min_size"] <= 0:
                    self.errors.append(f"post_processors[{index}].params.min_size must be a positive integer")
                if not isinstance(params["max_size"], int) or params["max_size"] <= 0:
                    self.errors.append(f"post_processors[{index}].params.max_size must be a positive integer")
                if params["min_size"] > params["max_size"]:
                    self.errors.append(f"post_processors[{index}].params.min_size must be less than or equal to max_size")
            
            if "color" in params:
                if not isinstance(params["color"], list) or len(params["color"]) != 3:
                    self.errors.append(f"post_processors[{index}].params.color must be a 3-element list")
                elif not all(isinstance(x, int) and 0 <= x <= 255 for x in params["color"]):
                    self.errors.append(f"Each element of post_processors[{index}].params.color must be an integer between 0-255")
        
        elif processor_type == "gaussian_noise":
            if "mean" not in params:
                self.errors.append(f"post_processors[{index}].params.mean is required")
            elif not isinstance(params["mean"], (int, float)):
                self.errors.append(f"post_processors[{index}].params.mean must be a number")
            
            if "std" not in params:
                self.errors.append(f"post_processors[{index}].params.std is required")
            elif not isinstance(params["std"], (int, float)) or params["std"] <= 0:
                self.errors.append(f"post_processors[{index}].params.std must be a positive number")
        
        elif processor_type == "perlin_noise":
            if "res" not in params:
                self.errors.append(f"post_processors[{index}].params.res is required")
            elif not isinstance(params["res"], list) or len(params["res"]) != 2:
                self.errors.append(f"post_processors[{index}].params.res must be a 2-element list")
            elif not all(isinstance(x, int) and x > 0 for x in params["res"]):
                self.errors.append(f"Each element of post_processors[{index}].params.res must be a positive integer")
            
            if "noise_range" not in params:
                self.errors.append(f"post_processors[{index}].params.noise_range is required")
            elif not isinstance(params["noise_range"], (int, float)) or params["noise_range"] <= 0:
                self.errors.append(f"post_processors[{index}].params.noise_range must be a positive number")
    
    def _validate_datatype_info(self, config: Dict[str, Any]):
        """Validate datatype information"""
        if "datatype_info" not in config:
            self.errors.append("'datatype_info' section is required")
            return
        
        datatype_config = config["datatype_info"]
        if not isinstance(datatype_config, dict):
            self.errors.append("'datatype_info' must be a dictionary")
            return
        
        for datatype, params in datatype_config.items():
            if not isinstance(params, dict):
                self.errors.append(f"datatype_info.{datatype} must be a dictionary")
                continue
            
            # diagram_num
            if "diagram_num" not in params:
                self.errors.append(f"datatype_info.{datatype}.diagram_num is required")
            elif not isinstance(params["diagram_num"], int) or params["diagram_num"] <= 0:
                self.errors.append(f"datatype_info.{datatype}.diagram_num must be a positive integer")
            
            # seed
            if "seed" not in params:
                self.errors.append(f"datatype_info.{datatype}.seed is required")
            elif not isinstance(params["seed"], int):
                self.errors.append(f"datatype_info.{datatype}.seed must be an integer")
    
    def _validate_split_settings(self, config: Dict[str, Any]):
        """Validate split settings"""
        if "split" not in config:
            self.errors.append("'split' section is required")
            return
        
        split_config = config["split"]
        
        # split_width
        if "split_width" not in split_config:
            self.errors.append("'split.split_width' is required")
        elif not isinstance(split_config["split_width"], int) or split_config["split_width"] <= 0:
            self.errors.append("'split.split_width' must be a positive integer")
        
        # split_height
        if "split_height" not in split_config:
            self.errors.append("'split.split_height' is required")
        elif not isinstance(split_config["split_height"], int) or split_config["split_height"] <= 0:
            self.errors.append("'split.split_height' must be a positive integer")
        
        # Warning when split size is larger than original image size
        if "width" in config and "height" in config:
            if split_config.get("split_width", 0) > config["width"]:
                self.warnings.append("split_width is larger than the original image width")
            if split_config.get("split_height", 0) > config["height"]:
                self.warnings.append("split_height is larger than the original image height")
    
    def get_errors(self) -> List[str]:
        """Get list of error messages"""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get list of warning messages"""
        return self.warnings
    
    def print_validation_results(self):
        """Print validation results"""
        if self.errors:
            print("❌ Validation errors:")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  - {warning}")

def validate_yaml_file(config_file: str) -> bool:
    """Function to validate YAML file"""
    try:
        with open(config_file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        
        validator = VoronoiConfigValidator()
        is_valid = validator.validate_config(config)
        
        validator.print_validation_results()
        return is_valid
        
    except yaml.YAMLError as e:
        print(f"❌ YAML file parsing error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {config_file}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validation.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    is_valid = validate_yaml_file(config_file)
    
    if not is_valid:
        sys.exit(1) 