
# HyperRes
Assaf keller & Ariel Yifee based on Shai Aharon and Dr. Gil Ben-Artzi work

## Requirements

### Dependency

Our code is based on the PyTorch library
* PyTorch 1.5.11+

Run the following command line to install all the dependencies


    pip install -r requirements.txt
    

## Live Demo
```shell
python live_demo.py                                       \
        --input [Path to image folder or image]           \
        --data_type [n,sr,j]                              \
        --checkpoint [Path to weights file (*.pth)]       \ 
   
```

## Example
go to Edit Configurations
in "Parameters" line  add this 
```shell
--input Set5/ --checkpoint Dej/model_best.pth --data_type j
```
![image](https://user-images.githubusercontent.com/77589405/210429028-a4d32bca-1de0-4a62-b5f2-26bf833c90b8.png)

