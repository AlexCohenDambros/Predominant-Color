from sys import flags
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter.messagebox import showinfo


# criando a janela
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def CreateBarColor(height, width, color):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)


def Select_file():
    filename = fd.askopenfilename(
        title='Select',
        initialdir='/'
        )
    
    if not filename:
        messagebox.showwarning("Alert!", "Image not selected")

    else:
        # mostrar a imagem
        img = cv2.imread(filename)

        # dimensões
        height, width, _ = np.shape(img)

        print(f"altura em pixels: {height}, largura em pixels: {width}")
        
        # Pegando todos os valores de pixel colocando em uma lista 
        data = np.reshape(img, (height * width, 3))
        data = np.float32(data)

        number_clusters = 3
        stop_criterion = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        compactness, labels, centers = cv2.kmeans(data, number_clusters, None, stop_criterion, 10, flags)

        print(centers) 

        bars = []
        rgb_values = []

        for index, row in enumerate(centers):
            bar, rgb = CreateBarColor(200, 200, row)
            bars.append(bar)
            rgb_values.append(rgb)
        
        img_bar = np.hstack(bars)


        cv2.imshow("Image", img)
        cv2.imshow("Dominant Colors", img_bar)
        cv2.waitKey(0)

# Botão
open_button = ttk.Button(
    root,
    text='Select an Image',
    command= Select_file
)

open_button.pack(expand=True)

root.mainloop()