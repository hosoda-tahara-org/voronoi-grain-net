# Voronoi Diagram Generator

## Structure

```
voronoi/
├── main.py                     # Main script to run the program
├── sample.py                   # Sample usage script
├── splitters.py                # Image splitting utilities
├── validation.py               # Config validation logic
└── utils/                      # Utility modules
    ├── __init__.py
    ├── generator.py            # Core Voronoi diagram generator
    ├── point_generators.py     # Point generation strategies
    ├── gray_generators.py      # Grayscale value generators
    ├── calculators.py          # Voronoi computation logic
    ├── renderers.py            # Image rendering functions
    ├── processors.py           # Post-processing pipeline
    └── base.py                 # Base class definitions
```