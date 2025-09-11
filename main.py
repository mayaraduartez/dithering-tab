from PIL import Image 
import numpy as np 
import matplotlib.pyplot as plt 
import tkinter as tk 
from tkinter import filedialog

# Abrindo a imagem BMP e convertendo para um array NumPy
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
img = Image.open(file_path)
arr = np.array(img, dtype=np.float64) #original
bin_arr = arr.copy() #copia 
threshold = 117 #limiarizacao
                 
mode = img.mode

if mode == 'L':  
    lin, col = bin_arr.shape
elif mode == 'RGB':  
    lin, col, channels = bin_arr.shape

# ditherizacao 
for y in range(lin):
    for x in range(col):
        if mode == 'L':
            old_pixel = bin_arr[y, x]   
            new_pixel = 0 if old_pixel <= threshold else 255
            erro = old_pixel - new_pixel
            bin_arr[y, x] = new_pixel  

            if x < col -1:
                bin_arr[y, x+1] += erro * 7/16
            if y < lin-1:
                if x > 0:
                    bin_arr[y+1, x-1] += erro * 3/16
                bin_arr[y+1, x] += erro * 5/16
                if x < col -1:
                    bin_arr[y+1, x+1] += erro * 1/16
        elif mode == 'RGB':
            for c in range(3): 
                old_pixel = bin_arr[y, x, c]   
                new_pixel = 0 if old_pixel <= threshold else 255
                erro = old_pixel - new_pixel
                bin_arr[y, x, c] = new_pixel  

                if x < col -1:
                    bin_arr[y, x+1, c] += erro * 7/16
                if y < lin-1:
                    if x > 0:
                        bin_arr[y+1, x-1, c] += erro * 3/16
                    bin_arr[y+1, x, c] += erro * 5/16
                    if x < col -1:
                        bin_arr[y+1, x+1, c] += erro * 1/16


bin_arr = np.clip(bin_arr, 0, 255).astype(np.uint8)
arr = np.clip(arr, 0, 255).astype(np.uint8)


# exibindo as imagens lado a lado
fig, axs = plt.subplots(1, 3 if mode == "RGB" else 2, figsize=(10, 5))
if mode == 'RGB':
    axs[0].imshow(arr)
elif mode == 'L':
    axs[0].imshow(arr, cmap='gray')
axs[0].set_title('Original')
axs[0].axis('off')

axs[1].imshow(bin_arr,cmap='gray' )
axs[1].set_title('Ditherizada')
axs[1].axis('off')

Image.fromarray(bin_arr.astype(np.uint8)).save("saida1.jpeg")

if mode == 'RGB':
    gray_img = img.convert("L")
    bin_arr = np.array(gray_img, dtype=np.float64)
    lin, col = bin_arr.shape
    for y in range(lin):
        for x in range(col):
                old_pixel = bin_arr[y, x]   
                new_pixel = 0 if old_pixel <= threshold else 255
                erro = old_pixel - new_pixel
                bin_arr[y, x] = new_pixel  

                if x < col -1:
                    bin_arr[y, x+1] += erro * 7/16
                if y < lin-1:
                    if x > 0:
                        bin_arr[y+1, x-1] += erro * 3/16
                    bin_arr[y+1, x] += erro * 5/16
                    if x < col -1:
                        bin_arr[y+1, x+1] += erro * 1/16
    axs[2].imshow(bin_arr, cmap='gray')
    axs[2].set_title('Ditherizada em escalas de cinza')
    axs[2].axis('off')

Image.fromarray(bin_arr.astype(np.uint8)).save("saida2.jpeg")

plt.tight_layout()
plt.show()

        