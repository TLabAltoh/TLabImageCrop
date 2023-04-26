# TLabImageCrop
Pythonを使った画像のマスク切り抜きを実行するプログラム  

## スクリーンショット
![UI_Image](https://user-images.githubusercontent.com/121733943/213375713-eb072071-d181-4572-b934-282436bb0543.png)  
![exprein_Image](https://user-images.githubusercontent.com/121733943/213297583-60b8a58e-1b32-4e3e-a0de-b9ef9ee1bd57.png)  

## スタートガイド
1. コマンドラインからプログラムを実行(パスは英数字のみ)
```
python ${YOUR_PATH}\TLabImageCrop.py  
```  
2. 切り抜きたいもとの画像(org_image)と，切り抜きたい箇所のみピクセルを白にした画像(mask_image)の2つを用意する  
3. パネルのOrgImage, MaskImageそれぞれに切り抜きたい画像とマスク画像を選択(画像のサイズを合わせること)
4. save resolutionに切り抜いた画像を保存するサイズを指定
5. Processから切り抜きを実行(しばらく待つ)

## 動作環境
Python: 3.9.7  
OS: Windows 10

## Note
- 高い解像度の画像を用意すれば，切り抜いた結果がきれいになる
