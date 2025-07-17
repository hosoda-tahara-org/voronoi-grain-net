"""
Classes related to image processing
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple
from perlin_numpy import generate_perlin_noise_2d
from .base import ImageProcessor


class CropProcessor(ImageProcessor):
    """Processor for cropping the image"""

    def __init__(self, crop_width: int = 2560, crop_height: int = 1536):
        self.crop_width = crop_width
        self.crop_height = crop_height

    def process(self, image: np.ndarray) -> np.ndarray:
        """Crop the center region of the image"""
        image_height, image_width = image.shape[:2]

        if self.crop_width > image_width or self.crop_height > image_height:
            raise ValueError("Crop size exceeds image dimensions")

        top = (image_height - self.crop_height) // 2
        left = (image_width - self.crop_width) // 2

        return image[top:top + self.crop_height, left:left + self.crop_width]


class EllipticalMaskProcessor(ImageProcessor):
    """Processor for adding elliptical mask defects"""
    
    def __init__(self, min_num: int = 0, max_num: int = 10,
                 min_size: int = 10, max_size: int = 40,
                 color: Tuple[int, int, int] = (0, 0, 0)):
        self.min_num = min_num
        self.max_num = max_num
        self.min_size = min_size
        self.max_size = max_size
        self.color = color

    def process(self, image: np.ndarray) -> np.ndarray:
        """Add random elliptical masks to the image"""
        h, w = image.shape[:2]
        image_masked = image.copy()
        num_masks = np.random.randint(self.min_num, self.max_num + 1)

        for _ in range(num_masks):
            center = (np.random.randint(0, w), np.random.randint(0, h))
            size = (np.random.randint(self.min_size, self.max_size),
                    np.random.randint(self.min_size, self.max_size))
            cv2.ellipse(image_masked, center, size, 0, 0, 360, self.color, -1)

        return image_masked


class GaussianNoiseProcessor(ImageProcessor):
    """Processor for adding Gaussian noise"""

    def __init__(self, mean: float = 0, std: float = 20):
        self.mean = mean
        self.std = std

    def process(self, image: np.ndarray) -> np.ndarray:
        """Add Gaussian noise to the image"""
        noise = np.random.normal(self.mean, self.std, image.shape)
        return self._apply_noise(image, noise)

    def _apply_noise(self, image: np.ndarray, noise: np.ndarray) -> np.ndarray:
        """Apply noise to the image and clip values"""
        noised_image = image.astype(np.float64) + noise
        return np.clip(noised_image, 0, 255).astype(np.uint8)


class PerlinNoiseProcessor(ImageProcessor):
    """Processor for adding Perlin noise"""

    def __init__(self, res: Tuple[int, int] = (32, 32), noise_range: float = 20):
        self.res = res
        self.noise_range = noise_range

    def process(self, image: np.ndarray) -> np.ndarray:
        """Add Perlin noise to the image"""
        height, width = image.shape[:2]
        perlin_noise = generate_perlin_noise_2d((height, width), self.res)
        perlin_noise = np.interp(
            perlin_noise,
            (perlin_noise.min(), perlin_noise.max()),
            (-self.noise_range, self.noise_range)
        )
        perlin_noise = perlin_noise[..., np.newaxis]  # Add channel dimension
        return self._apply_noise(image, perlin_noise)

    def _apply_noise(self, image: np.ndarray, noise: np.ndarray) -> np.ndarray:
        """Apply noise to the image and clip values"""
        noised_image = image.astype(np.float64) + noise
        return np.clip(noised_image, 0, 255).astype(np.uint8)


class ProcessorFactory:
    """Factory class for creating image processors"""

    def __init__(self):
        self._processors = {
            "crop": CropProcessor,
            "elliptical_mask": EllipticalMaskProcessor,
            "gaussian_noise": GaussianNoiseProcessor,
            "perlin_noise": PerlinNoiseProcessor,
        }

    def create_processor(self, processor_type: str, **params) -> ImageProcessor:
        """Dynamically create an image processor"""
        if processor_type not in self._processors:
            raise ValueError(f"Unknown processor: {processor_type}")
        return self._processors[processor_type](**params)


class ImagePipeline:
    """Image processing pipeline"""

    def __init__(self, config: Dict[str, Any]):
        self.factory = ProcessorFactory()
        self.image_processors = []  # Applied only to image
        self.both_processors = []   # Applied to both image and label

        # Build processors from configuration
        for proc_config in config.get("post_processors", []):
            processor = self.factory.create_processor(
                proc_config["type"],
                **proc_config.get("params", {})
            )

            # Classify based on apply_to parameter
            apply_to = proc_config["apply_to"]
            if apply_to == "both":
                self.both_processors.append(processor)
            else:  # Apply only to image
                self.image_processors.append(processor)

    def process(self, image: np.ndarray, label: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Apply processors to the image and label as specified"""
        # Apply processors to both
        for processor in self.both_processors:
            image = processor.process(image)
            label = processor.process(label)

        # Apply processors only to image
        for processor in self.image_processors:
            image = processor.process(image)

        return image, label
