# voronoi-grain-net

This repository contains the official implementation of the paper:  
**_Transfer learning approach with synthetic data for high-accuracy segmentation of equiaxed grain boundaries_**.

### 🔗 [Project Page](https://hosoda-tahara-org.github.io/voronoi-grain-net/) | [Voronoi demo page](https://voronoi-web.streamlit.app/) | [Weights(Coming soon...)]() |

> ⚠️ You may need to click **"Yes, get this app back up!"** on the Voronoi demo page if it's temporarily inactive.


## Overview

This repository provides:

1. 🧪 A **synthetic dataset generator** using Voronoi diagrams for microstructure-like segmentation tasks.
2. 🧠 Pretrained U-Net weights trained on synthetic Voronoi images, ready to be fine-tuned on SEM data.

⚠️ Note: We do not provide a full training pipeline or U-Net implementation here. Please refer to [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet) for the base architecture.


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
