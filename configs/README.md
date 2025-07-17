# Configuration Files

This directory contains configuration files for generating Voronoi diagram images with different parameters.


## Configuration Options

| Category | Subcategory | Description |
|----------|-------------|-------------|
| **width** | | Width of the generated Voronoi diagram image (pixels) |
| **height** | | Height of the generated Voronoi diagram image (pixels) |
| **output_dir** | | Output directory path for generated images and labels |
| **point_generation** | method: "random" | Generates seed points using uniform random sampling |
| | method: "poisson_disk" | Generates seed points using Poisson disk sampling |
| | points_num | Number of seed points to generate (for uniform method) |
| | min_distance | Minimum separation distance between points (for poisson_disk method) |
| | max_attempts | Maximum attempts to place valid points (for poisson_disk method) |
| **label_info** | color | RGB color values for boundary lines |
| | thickness | Line thickness of boundary lines |
| **image_info** | method: "uniform" | Assigns grayscale values sampled from a uniform distribution (0–255) |
| | method: "gaussian" | Assigns grayscale values sampled from a Gaussian distribution (mean, std) |
| | mean | Mean value for Gaussian distribution |
| | std | Standard deviation for Gaussian distribution |
| **post_processors** | type: "crop" | Crops the image to specified dimensions |
| | type: "elliptical_mask" | Adds random black ellipses to simulate contamination artifacts |
| | type: "gaussian_noise" | Adds Gaussian noise to images |
| | type: "perlin_noise" | Adds Perlin noise to simulate polishing artifacts |
| **datatype_info** | diagram_num | Number of Voronoi diagrams to generate per dataset |
| | seed | Random seed for reproducible generation |
| **split** | split_width | Width of each cropped image |
| | split_height | Height of each cropped image |



## Usage

To use a specific configuration:

```bash
python voronoi/main.py configs/sample_case_1.yaml
```

The generated images and labels will be saved in the specified output directory.
