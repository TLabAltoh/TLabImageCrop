import cv2
import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


button_width = 10
button_height = 1

failed_str = "Nothing"

# whether the file is selected.
flag_mask = False
flag_org = False

mask_path = ""
org_path = ""


def select_from_explorer():
    typ = [("", "*")]
    initial_dir = "C:\\"
    file = filedialog.askopenfilenames(filetypes = typ, initialdir = initial_dir)
    
    if(len(file) == 0):
        return failed_str
    else:
        return file[0]


def select_mask_image(event):
    global mask_path_label
    global mask_path
    global flag_mask
    
    img_path = select_from_explorer()
    if(img_path != failed_str):
        flag_mask = True
        mask_path_label["text"] = img_path
        mask_path = img_path


def select_org_image(event):
    global org_path_label
    global org_path
    global flag_org
    
    img_path = select_from_explorer()
    if(img_path != failed_str):
        flag_org = True
        org_path_label["text"] = img_path
        org_path = img_path
    

def crop(event):
    global org_path
    global mask_path
    global flag_org
    global flag_mask
    global save_width_text
    global save_height_text
    global state
    global root

    # ------------------------------------------------------------------------------
    # source img file check
    #
    
    if(flag_org == False or flag_mask == False):
        messagebox.showerror("TLabImageCrop", "source_img not selected")
        return

    print("org_path: ", org_path.replace("/", "\\"))
    print("mask_path: ", mask_path.replace("/", "\\"))

    # load the foreground image
    org_img = cv2.imread(org_path.replace("/", "\\"), cv2.IMREAD_UNCHANGED)

    # load mask image
    mask_img = cv2.imread(mask_path.replace("/", "\\"), cv2.IMREAD_UNCHANGED)

    org_height = len(org_img)
    org_width = len(org_img[0])
    org_channel = len(org_img[0][0])

    mask_height = len(mask_img)
    mask_width = len(mask_img[0])
    mask_channel = len(mask_img[0][0])

    if(mask_height != org_height):
        messagebox.showerror("TLabImageCrop", "Image height mismatch")
        return
    
    if(mask_width != org_width):
        messagebox.showerror("TLabImageCrop", "Image width mismatch")
        return

    if(mask_channel != org_channel):
        messagebox.showerror("TLabImageCrop", "Image channel mismatch")
        return

    # ------------------------------------------------------------------------------
    # save resolution check
    #

    save_width_get = save_width_text.get()
    save_height_get = save_height_text.get()
    if(save_width_get.isdecimal() == False or save_height_get.isdecimal() == False):
        messagebox.showerror("TLabImageCrop", "invalid save resolution")
        return

    # ------------------------------------------------------------------------------
    # clipping process
    #

    state["text"] = "state: during clipping"
    root.update_idletasks()
    
    # Make the black part of the mask image transparent
    for i in range(mask_height):
        for j in range(mask_width):
            if(mask_img[i][j][0] < 10 and mask_img[i][j][1] < 10 and mask_img[i][j][2] < 10):
                mask_img[i][j][3] = 0
                
    # Swap the texels in the masked part with the original
    for i in range(mask_height):
        for j in range(mask_width):
            if(mask_img[i][j][3] > 250):
                mask_img[i][j][0] = org_img[i][j][0]
                mask_img[i][j][1] = org_img[i][j][1]
                mask_img[i][j][2] = org_img[i][j][2]

    state["text"] = "state: done"
    cv2.imshow("Result", mask_img)

    # ------------------------------------------------------------------------------
    # Saving cropped results
    #
    
    # Resize and save the clipped image
    save_path = os.path.dirname(org_path.replace("/", "\\")) + "\\" + "croped_" + os.path.basename(org_path.replace("/", "\\"))
    
    cv2.imwrite(save_path, cv2.resize(mask_img, (int(save_width_get), int(save_height_get))))


# create canvas root
root = tk.Tk()
root.title(u"TLabImageCrop")
root.geometry("400x275")

# create canvas
select_button_area = tk.Canvas(root, width=400, height=275)
select_button_area.place(x = 0, y = 0)
select_button_area.create_text(200, 40, text = "Choose an image to crop and a mask")

ui_pos_x = 40
ui_pos_x_1 = 140

# ----------------------------------------------------------------------------------------
# add button
#

button = tk.Button(text=u"OrgImage", width=button_width, height=button_height)
button.bind("<Button-1>", select_org_image)
button.place(x=ui_pos_x, y=80)

button1 = tk.Button(text=u"MaskImage", width=button_width, height=button_height)
button1.bind("<Button-1>", select_mask_image)
button1.place(x=ui_pos_x, y=120)

button2 = tk.Button(text=u"Process", width=button_width, height=button_height)
button2.bind("<Button-1>", crop)
button2.place(x=ui_pos_x, y=200)

# ----------------------------------------------------------------------------------------
# add text box
#

save_width_text = tk.Entry(width=5)
save_width_text.place(x=ui_pos_x, y=160)

save_height_text = tk.Entry(width=5)
save_height_text.place(x=ui_pos_x + 40, y=160)

# ----------------------------------------------------------------------------------------
# add label
#

org_path_label = tk.Label(text=u"***", font=("", 12), justify=tk.LEFT)
org_path_label.place(x=ui_pos_x_1, y=80)

mask_path_label = tk.Label(text=u"***", font=("", 12), justify=tk.LEFT)
mask_path_label.place(x=ui_pos_x_1, y=120)

save_resolution_label = tk.Label(text=u"save resolution (width, height)", font=("", 12), justify=tk.LEFT)
save_resolution_label.place(x=ui_pos_x_1, y=160)

final_path_label = tk.Label(text=u"***", font=("", 12), justify=tk.LEFT)
final_path_label.place(x=ui_pos_x_1, y=200)

state = tk.Label(text=u"state: ...", font=("", 12), justify=tk.LEFT)
state.place(x=ui_pos_x, y = 240)

# ----------------------------------------------------------------------------------------
# start GUI
#

root.mainloop()
