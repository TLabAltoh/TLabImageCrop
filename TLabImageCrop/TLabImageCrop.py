import cv2
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

button_width = 10
button_height = 1

flag_mask = False
flag_org = False

mask_path = ""
org_path = ""

failed_str = "Nothing"


def select_from_explorer():
    typ = [("", "*")]
    dir = "C:\\pg"
    file = filedialog.askopenfilenames(filetypes = typ, initialdir = dir)
    
    if(len(file) == 0):
        return failed_str
    else:
        return file[0]


def select_mask_image(event):
    global mask_path_label
    global mask_path
    
    img_path = select_from_explorer()
    if(img_path != failed_str):
        flag_mask = True
        mask_path_label["text"] = img_path
        mask_path = img_path
        print(img_path)


def select_org_image(event):
    global org_path_label
    global org_path
    
    img_path = select_from_explorer()
    if(img_path != failed_str):
        flag_org = True
        org_path_label["text"] = img_path
        org_path = img_path
        print(img_path)


def crop(event):
    global org_path
    global mask_path
    
    print(org_path.replace("/", "\\"))
    print(mask_path.replace("/", "\\"))
    
    # 前景画像を読み込む
    org_img = cv2.imread(org_path.replace("/", "\\"), cv2.IMREAD_UNCHANGED)

    # マスク画像を読み込む
    mask_img = cv2.imread(mask_path.replace("/", "\\"), cv2.IMREAD_UNCHANGED)
    
    cv2.imshow("Test", mask_img)
    
    height = len(mask_img)
    width = len(mask_img[0])
    channel = len(mask_img[0][0])
    
    # マスク画像の黒い部分を透明にする
    for i in range(height):
        for j in range(width):
            if(mask_img[i][j][0] < 10 and mask_img[i][j][1] < 10 and mask_img[i][j][2] < 10):
                mask_img[i][j][3] = 0
                
    # マスク部分のテクセルをオリジナルと入れ替える
    for i in range(height):
        for j in range(width):
            if(mask_img[i][j][3] > 250):
                mask_img[i][j][0] = org_img[i][j][0]
                mask_img[i][j][1] = org_img[i][j][1]
                mask_img[i][j][2] = org_img[i][j][2]
                
    cv2.imshow("Test", mask_img)
    
    print(org_img)
    print(mask_img)
    
    # 切り抜いた画像をリサイズ保存
    save_path = os.path.dirname(org_path.replace("/", "\\")) + "\\" + "croped_" + os.path.basename(org_path.replace("/", "\\"))
    cv2.imwrite(save_path, cv2.resize(mask_img, (1024, 500)))


# キャンバスを作成
root = tk.Tk()
root.title(u"TLabImageCrop")
root.geometry("400x200")
select_button_area = tk.Canvas(root, width=400, height=200)
select_button_area.place(x = 0, y = 0)
select_button_area.create_text(200, 40, text = "切り抜きする画像とマスクを選択してください")

button = tk.Button(text=u"OrgImage", width=button_width, height= button_height)
button.bind("<Button-1>", select_org_image)
button.place(x=80, y=80)

button2 = tk.Button(text=u"MaskImage", width=button_width, height=button_height)
button2.bind("<Button-1>", select_mask_image)
button2.place(x=80, y=120)

button3 = tk.Button(text=u"Process", width=button_width, height=button_height)
button3.bind("<Button-1>", crop)
button3.place(x=80, y=160)

org_path_label = tk.Label(text=u"***", font=("", 12), justify=tk.LEFT)
org_path_label.place(x=170, y=80)

mask_path_label = tk.Label(text=u"***", font=("", 12), justify=tk.LEFT)
mask_path_label.place(x=170, y=120)

final_path_label = tk.Label(text=u"***", font=("", 12), justify=tk.LEFT)
final_path_label.place(x=170, y=160)

# GUIを開始
root.mainloop()
