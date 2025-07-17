"""
Main class for generating Voronoi diagrams
"""

import numpy as np
from typing import Dict, Any, Tuple
from .point_generators import PointGeneratorFactory
from .gray_generators import GrayValueFactory
from .calculators import VoronoiCalculator
from .renderers import ImageRenderer
from .processors import ImagePipeline


class VoronoiGenerator:
    """Main class for generating Voronoi diagrams

    Attributes:
        width (int): Width of the image
        height (int): Height of the image
        point_generator (PointGenerator): Seed point generator
        label_info (Dict): Label rendering settings
        gray_generator (GrayValueGenerator): Grayscale value generator
        voronoi_calculator (VoronoiCalculator): Voronoi diagram calculator
        image_renderer (ImageRenderer): Image renderer
        image_pipeline (ImagePipeline): Image post-processing pipeline
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.width = config["width"]
        self.height = config["height"]
        
        # Initialize seed point generator
        method = config["point_generation"]["method"]
        self.point_generator = PointGeneratorFactory().create_generator(
            method, 
            **config["point_generation"]["params"]
        )
        
        # Label rendering configuration
        self.label_info = config.get("label_info", {})
        
        # Initialize grayscale value generator
        image_info = config["image_info"]
        self.gray_generator = GrayValueFactory().create_generator(
            image_info["method"],
            **image_info.get("params", {})
        )

        # Initialize other components
        self.voronoi_calculator = VoronoiCalculator(self.width, self.height)
        self.image_renderer = ImageRenderer(self.width, self.height)
        self.image_pipeline = ImagePipeline(config)
    
    def generate(self, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
        """Generate a Voronoi diagram

        Args:
            **kwargs: Dynamic parameters for seed point generation
                - For random generation: points_num
                - For Poisson disk sampling: min_distance, max_attempts

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple of (image, label)
        """
        # Generate seed points
        points = self.point_generator.generate(self.width, self.height, **kwargs)
        
        # Compute Voronoi diagram
        facets = self.voronoi_calculator.calculate(points)
        
        # Render image and label
        voronoi_label = self.image_renderer.render_voronoi_label(facets, **self.label_info)
        voronoi_image = self.image_renderer.render_voronoi_image(facets, self.gray_generator)
        
        # Post-processing
        voronoi_image, voronoi_label = self.image_pipeline.process(voronoi_image, voronoi_label)
        
        return voronoi_image, voronoi_label
