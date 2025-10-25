# voronoi-grain-net

This repository contains the official implementation of the paper:  
**_Transfer learning approach with Voronoi-based synthetic data for high-accuracy segmentation of equiaxed grain boundaries_**.

### 🔗 [Project Page](https://hosoda-tahara-org.github.io/voronoi-grain-net/) | [Voronoi demo page](https://voronoi-web.streamlit.app/) | [Weights(Google drive)](https://drive.google.com/drive/folders/1LeuwNjhs0DscPj5WA_630ilwzXm3i521?usp=sharing) |


## ⚠️ IMPORTANT: About the Demo Page

**If you see this screen when accessing the demo, the app is NOT broken:**

<img src="sleep.png" alt="App sleep screen" width="500"/>

**This is normal!** The free hosting service puts the app to sleep when inactive.

### 🔄 How to wake it up:
1. **Click the blue button** that says **"Yes, get this app back up!"**
2. **Wait 30-60 seconds** for the app to start (first load is slow)
3. The app will then work normally

**The app is working, just sleeping. Please be patient!**


## Overview

This repository provides:

1. 🧪 A **synthetic dataset generator** using Voronoi diagrams for microstructure-like segmentation tasks.
2. 🧠 Pretrained U-Net weights trained on synthetic Voronoi images, ready to be fine-tuned on SEM data.

> ⚠️ We do not provide a full training pipeline or U-Net implementation here. Please refer to [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet) for the base architecture.


## News

- [2025/07/19]: Pretrained models released
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

This section explains how to load and use the pretrained model weights with an existing U-Net implementation. **This repository does not provide a full U-Net training pipeline or inference script.** For the base U-Net architecture, please refer to [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet).


1.  **Download Pretrained Models**  
   Download the pretrained model weights [from here](https://drive.google.com/drive/folders/1LeuwNjhs0DscPj5WA_630ilwzXm3i521?usp=sharing).

2. **Set up Pytorch-UNet**
   ```bash
   git clone https://github.com/milesial/Pytorch-UNet.git
   cd Pytorch-UNet
   # If necessary, install dependencies following the instructions in the Pytorch-UNet repository's README.
   ```

3. **Instantiate and Parameterize the U-Net Model**  
   In your own inference script, instantiate the U-Net model using the Pytorch-UNet codebase with the following parameters:

   ```python
   import torch
   from unet import UNet # Import the UNet class from Pytorch-UNet repository

   model = UNet(n_channels=1, n_classes=1, bilinear=False)
   ```

4. **Load the pretrained model**
   ```python
   # Replace 'path/to/pretrained/weights.pth' with the actual path to your downloaded weights file.
   model.load_state_dict(torch.load('path/to/pretrained/weights.pth'))
   ```

> ⚠️ The pretrained model weights provided (or referenced) were trained using the implementation from [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet), which is licensed under the GNU General Public License v3.0 (GPL-3.0). Therefore, these weights are subject to the terms of the GPL-3.0 license. For more details, please refer to the [License](#license) section of this README.

## Acknowledgement

This work was supported by the Japan Society for the Promotion of Science (JSPS) and conducted using the TSUBAME4.0 supercomputer at the Institute of Science Tokyo.

We also gratefully acknowledge the following open-source repositories that contributed to this work:
- [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet)
- [pvigier/perlin-numpy](https://github.com/pvigier/perlin-numpy)
- [qubvel-org/segmentation_models.pytorch](https://github.com/qubvel-org/segmentation_models.pytorch)
- [eliahuhorwitz/Academic-project-page-template](https://github.com/eliahuhorwitz/Academic-project-page-template)


## License

This repository is licensed under the [MIT License](./LICENSE).

However, please note the following:

- The pretrained U-Net weights provided (or referenced) in this repository were trained using the implementation from [milesial/Pytorch-UNet](https://github.com/milesial/Pytorch-UNet), which is licensed under the GNU General Public License v3.0 (GPL-3.0).
- As a result, these weights are considered derivative works of GPL-3.0 code, and **are therefore subject to the terms of the GPL-3.0 license**.
- Redistribution or use of these pretrained weights must comply with the GPL-3.0 license. The rest of the code in this repository remains under the MIT License.

We encourage users to review both licenses if they plan to reuse or redistribute any parts of this project.


## Citation

```bibtex
@unpublished{ozaki2025transfer,
  title={Transfer learning approach with Voronoi-based synthetic data for high-accuracy segmentation of equiaxed grain boundaries},
  author={Ozaki, Koichi and Nohira, Naoki and Tahara, Masaki and Kumazawa, Itsuo and Hosoda, Hideki},
  year={2025},
  note={under review}
}
```
