# BV-format-compatibility

## Overview

**Integration of  BV format into Napari and Fiji, more details about BV format can be seen in [BioimageVision](https://github.com/Quanlab-Bioimage/BioimageVision)**

## Environmental requirements

* Operating system: windows
* python==3.9

## Hardware Requirements
**The library requires only about 16 GB of RAW computer for minimum performance, and the following specifications are recommended for best performance**

* RAM: 128+ GB
* CPU: 8+ cores, over 3.50 GHz/core

## napari-BVdata

### Install:

1. Create a virtual environment. If you have a python environment with napari, you can activate the environment and skip this step.

   ``` python -m venv napari_env``` 

   ``` .\napari_env\Scripts\activate``` 

2. unzip */napari-BVdata/napari-BVdata/BVMoudle.zip directly .

3. cd */napari-BVdata and run following code in terminal:

   ``` python -m pip install -e .```

### Usage:

Run following code in terminal:

``` python script.py```

<img src="./imgs/1.JPG" alt="1" style="zoom:80%;" />

Click ```Load(napari-BVdata)``` in ```Plugins``` :

![](./imgs/2.JPG)

Click ```Browse``` to choose BV data in computer.  Input region of interests and scale level in ```Setting ROI```:

<img src="./imgs/4.jpg" style="zoom:80%;" />

click ``` OK``` :

<img src="./imgs/5.JPG" style="zoom:80%;" />

## Fiji-BVdata

### Install:

1. Create a virtual environment.

   ``` python -m venv fiji_env``` 

   ``` .\fiji_env\Scripts\activate``` 

2. cd */Fiji-BVdata and run following code in terminal:

   ```pip install -r requirements```

3. unzip Fiji-BVdata/BVMoudle.zip directly

4. Run following code in terminal:

   ``` python script.py```

   ![6](./imgs/6.JPG)

## Usage:

Some parameters have to be set in script.py

` fiji_path(optional):  path for installed fiji.` 

`BV_config_path:       path for config file of BV data.`

`level:                scale level for loaded BV data.`

`{min_x, max_x, min_y, max_y, min_z, max_z}: parameters for ROI`



## Technique Help

[cailin0227@hust.edu.cn](cailin0227@hust.edu.cn)























