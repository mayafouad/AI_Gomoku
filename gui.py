"""
        GUI
"""
import tkinter as tk
from PIL import Image, ImageTk
import math
import csv

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600, bg='#E6B88C')
canvas.pack()  

stone_images = {} 



def DrawGrid():
    for i in range(15):
       canvas.create_line(0, 40 * i, 600, 40 * i)
       canvas.create_line(40 * i, 0, 40 * i, 600)

def InitializeGrid(fileName):
    lis = []
    with open(fileName, 'r') as file:
         for row in file:
             lis.append(row)
    return lis

def PutInitialTiles():
    global stone_images  
    try:
        initial_grid = InitializeGrid("initialGrid.txt")
        for y in range(15):
          for x in range(15):
            cell = initial_grid[y][x] 
            image = None
            if cell == 'b':
                image = Image.open("black_gm.jpg")
            elif cell == 'w':
                image = Image.open("white_gm.png")
            if image:
                resized_image = image.resize((36, 36))  
                stone_key = f"{y}_{x}_{cell}"
                stone_images[stone_key] = ImageTk.PhotoImage(resized_image)
                canvas.create_image(x * 40 + 5, y * 40 + 5, anchor=tk.CENTER, image=stone_images[stone_key])

    except Exception as e:
        print(f"Error: {e}")


def GetHumanMove(event):
    global stone_images  
    
    col = math.ceil(event.x / 40)
    row = math.ceil(event.y / 40) 
    x = col * 40
    y = row * 40
    
    print(f"Placing stone at grid position ({row}, {col})")
    
    try:
        
        clicked_img = Image.open(r"D:\AI-Gumko\AI-Gumko\black_gm.jpg")
        clicked_resized = clicked_img.resize((36, 36))  
        stone_key = f"{row}_{col}_b"  
        stone_images[stone_key] = ImageTk.PhotoImage(clicked_resized)
        
        canvas.create_image(x + 5, y + 5, 
                          anchor=tk.CENTER, image=stone_images[stone_key])
    except Exception as e:
        print(f"Error: {e}")
canvas.bind("<Button-1>", GetHumanMove)


def launch_game(mode) :
    DrawGrid()
    PutInitialTiles()
    canvas.pack()
    root.mainloop()

