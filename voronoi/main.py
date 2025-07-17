import sys
import os
import time
import numpy as np
import yaml
import cv2
from tqdm import tqdm
from utils import VoronoiGenerator
from splitters import VoronoiSplitter
from validation import VoronoiConfigValidator

def validate_config_file(config):
    """Execute validation of the configuration file"""
    validator = VoronoiConfigValidator()
    if not validator.validate_config(config):
        validator.print_validation_results()
        sys.exit(1)
    if validator.get_warnings():
        validator.print_validation_results()
        print()

def check_directory(output_dir):
    """Check if the output directory exists and ask whether to overwrite it."""
    if os.path.exists(output_dir):
        answer = input(f"The directory '{output_dir}' already exists. Do you want to overwrite it? (y/n): ")
        if answer.lower() != "y":
            print("The process was interrupted.")
            sys.exit(0)

def create_directory(output_dir, datatype_info):
    """Create the output directory."""
    for datatype, params in datatype_info.items():
        os.makedirs(f"{output_dir}/{datatype}/images", exist_ok=True)
        os.makedirs(f"{output_dir}/{datatype}/labels", exist_ok=True)

def save_images(output_dir, datatype, name, image, label):
    """Save images and labels."""
    base_path = f"{output_dir}/{datatype}"
    cv2.imwrite(f"{base_path}/images/{name}.png", image)
    cv2.imwrite(f"{base_path}/labels/{name}.png", label)

def main(config_file):
    # Load config file
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # Execute validation
    validate_config_file(config)
    
    voronoi_config = config["voronoi"]
    output_dir = voronoi_config["output_dir"]
    datatype_info = voronoi_config["datatype_info"]

    # Initialize
    voronoi_generator = VoronoiGenerator(voronoi_config)
    voronoi_splitter = VoronoiSplitter(voronoi_config)
    
    # Create output directory
    check_directory(output_dir)
    create_directory(output_dir, datatype_info)

    # Generate and save Voronoi diagrams
    for datatype, params in datatype_info.items():
        np.random.seed(params["seed"]) # Set random seed
        name_counter = 0
        for i in tqdm(range(params["diagram_num"]), desc=f"Generating {datatype} images"):
            # Get parameters
            point_params = voronoi_config["point_generation"]["params"]
            if voronoi_config["point_generation"]["method"] == "random": # random_sampling
                points_num_list = point_params["points_num"]
                points_num = points_num_list[i % len(points_num_list)]
                kwargs = {"points_num": points_num}
            else:  # poisson_disk_sampling
                min_distance_list = point_params["min_distance"]
                min_distance = min_distance_list[i % len(min_distance_list)]
                max_attempts = point_params.get("max_attempts", 100)
                kwargs = {"min_distance": min_distance, "max_attempts": max_attempts}
            
            voronoi_image, voronoi_label = voronoi_generator.generate(**kwargs) # Generate Voronoi diagram
            image_list, label_list = voronoi_splitter(voronoi_image, voronoi_label) # Split images and labels

            # Save
            for image, label in zip(image_list, label_list):
                save_images(output_dir, datatype, name_counter, image, label)
                name_counter += 1

if __name__ == "__main__":
    args = sys.argv
    try:
        # Validate the arguments
        if len(args) != 2:
            raise ValueError("ValueError: The number of arguments is invalid.")
        config_file = args[1]
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"File not found: {config_file}")
        if not config_file.endswith('.yaml'):
            raise ValueError("ValueError: The configuration file must be in yaml format.")
        
        # Run the main function
        main(config_file)

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
