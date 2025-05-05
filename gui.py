"""
        GUI
"""
import tkinter as tk
from PIL import Image, ImageTk
import math

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600, bg='#E6B88C')
canvas.pack()  
root.resizable(False, False)


for i in range(15):
    canvas.create_line(0, 40 * i, 600, 40 * i)
    canvas.create_line(40 * i, 0, 40 * i, 600)

def click(event):
   
    col = math.ceil(event.x / 40)
    row = math.ceil(event.y / 40) 
    x = col * 40
    y = row * 40
    
    print(f"Placing stone at grid position ({row}, {col})")
    
    try:
        
        image = Image.open("C:\\Users\\lojay\\Downloads\\black_gm.jpg")
        resized_image = image.resize((36, 36))  
        global stone_img  
        stone_img = ImageTk.PhotoImage(resized_image)
        
        canvas.create_image(x + 5, y + 5, anchor=tk.CENTER, image=stone_img)
    except Exception as e:
        print(f"Error: {e}")

canvas.bind("<Button-1>", click)
root.mainloop()





canvas.pack()
root.mainloop()
