"""
Classes related to image splitting
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import os
from natsort import natsorted


class ImageSplitter:
    """Class for splitting an image into multiple smaller images
    
    Attributes:
        width (int): Width of each split image
        height (int): Height of each split image
    """
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
    
    def split_image(self, image: np.ndarray) -> List[np.ndarray]:
        """Split an image into multiple smaller images

        Args:
            image (np.ndarray): The image to be split

        Returns:
            List[np.ndarray]: A list of split images

        Raises:
            ValueError: If the image size is not divisible by the split size
        """
        h, w = image.shape[:2]
        rows = h // self.height
        columns = w // self.width
        
        if w % self.width != 0 or h % self.height != 0:
            raise ValueError(f"Image size ({w}x{h}) is not divisible by split size ({self.width}x{self.height})")

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
    """Class for splitting Voronoi images and their corresponding labels

    Attributes:
        splitter (Optional[ImageSplitter]): Image splitter (None if splitting is not specified in the config)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the splitter

        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        self.splitter = None
        if "split" in config:
            split_config = config["split"]
            self.splitter = ImageSplitter(
                split_config["split_width"], 
                split_config["split_height"]
            )

    def __call__(self, image: np.ndarray, label: np.ndarray) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """Split the image and label

        Args:
            image (np.ndarray): The image to be split
            label (np.ndarray): The label to be split

        Returns:
            Tuple[List[np.ndarray], List[np.ndarray]]: A tuple of (list of split images, list of split labels)

        Note:
            If "split" is specified in the config, both image and label will be split accordingly.
            If not, they will be returned as single-element lists.
        """
        if self.splitter:
            image_list = self.splitter.split_image(image)
            label_list = self.splitter.split_image(label)
        else:
            image_list, label_list = [image], [label]
        
        return image_list, label_list
