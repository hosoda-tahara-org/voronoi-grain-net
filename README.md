# Transfer Learning Approach with Synthetic Data for High-Accuracy Segmentation of Equiaxed Grain Boundaries

This repository contains the official implementation of the paper:  
**_Transfer learning approach with synthetic data for high-accuracy segmentation of equiaxed grain boundaries_**.

### 🔗 [Project Page](https://hosoda-tahara-org.github.io/voronoi-grain-net/) | [Voronoi demo page](https://voronoi-web.streamlit.app/) | [Weights(Coming soon...)]() |

> ⚠️ You may need to click **"Yes, get this app back up!"** on the Voronoi demo page if it's temporarily inactive.


## Overview

Accurate segmentation of microstructural images is essential for quantitative materials characterization. However, traditional deep learning models often struggle due to limited annotated data and domain mismatch.

This project introduces a **transfer learning framework using synthetic Voronoi diagrams** to pretrain segmentation models. The approach is tailored for equiaxed grain boundary extraction in α-phase pure titanium SEM images, and achieves **higher accuracy than ImageNet-based models**.

### Key Features

- **🔧 Synthetic Data Generation**  
  Generate Voronoi diagrams with controllable parameters such as seed placement, grayscale variation, and noise.

- **📈 Improved Transfer Learning**  
  Pretraining on synthetic structures enhances generalization to real microstructures.

- **📊 High IoU Performance**  
  Outperforms ImageNet-pretrained models in grain boundary segmentation tasks.

- **🧠 Feature Awareness**  
  Captures microstructure-relevant features like **triple junctions**, enabling segmentation even in low-contrast regions.


## News

- [2025/07/17]: Code repository released


## Quick Start to Generate Voronoi Diagrams
1. **Clone the repository**
   ```bash
   git clone https://github.com/hosoda-tahara-org/voronoi-grain-net.git
   cd voronoi-grain-net
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample Voronoi image**
   ```bash
   python voronoi/main.py configs/sample_case_1.yaml 
   ```

👉 For more configuration options, see [configs/README.md](configs/README.md).


## Using Pretrained Models

*Pretrained weights will be available soon*


## Acknowledgement

This work was supported by the Japan Society for the Promotion of Science (JSPS) and conducted using the TSUBAME4.0 supercomputer at the Institute of Science Tokyo.

We also gratefully acknowledge the following open-source repositories that contributed to this work:
- [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet)
- [pvigier/perlin-numpy](https://github.com/pvigier/perlin-numpy)
- [qubvel-org/segmentation_models.pytorch](https://github.com/qubvel-org/segmentation_models.pytorch)
- [eliahuhorwitz/Academic-project-page-template](https://github.com/eliahuhorwitz/Academic-project-page-template)

## Citation

```bibtex
@unpublished{ozaki2025transfer,
  title={Transfer learning approach with synthetic data for high-accuracy segmentation of equiaxed grain boundaries},
  author={Ozaki, Koichi and Nohira, Naoki and Tahara, Masaki and Kumazawa, Itsuo and Hosoda, Hideki},
  year={2025},
  note={under review}
}
```
