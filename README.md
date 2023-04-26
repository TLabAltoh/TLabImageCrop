# TLabImageCrop

[日本語版READMEはこちら](README-ja.md)

Program to perform mask cropping of images using Python  

## Screenshot
![UI_Image](https://user-images.githubusercontent.com/121733943/213375713-eb072071-d181-4572-b934-282436bb0543.png)  
![exprein_Image](https://user-images.githubusercontent.com/121733943/213297583-60b8a58e-1b32-4e3e-a0de-b9ef9ee1bd57.png)  

## Getting Started
1. Run the program from the command line (path must be alphanumeric)
```
python ${YOUR_PATH}\TLabImageCrop.py  
```  
2. Prepare two images: the original image to be clipped (org_image) and an image with white pixels only in the area to be clipped (mask_image)  
3. Select the image to be cropped and the mask image for each OrgImage and MaskImage in the panel (the size of the images must be matched)
4. Specify the size to save the cropped image in save resolution.
5. Execute clipping from Process (wait for a while)

## Operating Environment
Python: 3.9.7  
OS: Windows 10

## Note
- Higher-resolution images will produce a better cropped result
