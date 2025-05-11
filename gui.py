# """
#         GUI
# """
# import tkinter as tk
# from PIL import Image, ImageTk
# import math
import MinMax
# import AlphaBeta


# stone_images = {} 



# def DrawGrid():
#     for i in range(15):
#        canvas.create_line(0, 40 * i, 600, 40 * i)
#        canvas.create_line(40 * i, 0, 40 * i, 600)

# def InitializeGrid(fileName):
#     lis = []
#     with open(fileName, 'r') as file:
#          for row in file:
#              lis.append(row)
#     return lis

# def PutInitialTiles():
#     global stone_images  
#     try:
#         initial_grid = InitializeGrid("initialGrid.txt")
#         for y in range(15):
#           for x in range(15):
#             cell = initial_grid[y][x] 
#             image = None
#             if cell == 'b':
#                 image = Image.open("black_gm.jpg")
#             elif cell == 'w':
#                 image = Image.open("white_gm.png")
#             if image:
#                 resized_image = image.resize((36, 36))  
#                 stone_key = f"{y}_{x}_{cell}"
#                 stone_images[stone_key] = ImageTk.PhotoImage(resized_image)
#                 canvas.create_image(x * 40 + 5, y * 40 + 5, anchor=tk.CENTER, image=stone_images[stone_key])

#     except Exception as e:
#         print(f"Error: {e}")




def launch_game(mode) :
    MinMax.select_mode(mode)

