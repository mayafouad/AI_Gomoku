import tkinter as tk
import gui   

def start_game(mode):
    root.destroy()   
    gui.launch_game(mode)   

root = tk.Tk()
root.title("Gumko - Select Game Mode")
root.geometry("600x600") 

 
canvas = tk.Canvas(root, width=600, height=600, bg='#E6B88C')
canvas.pack()

 
frame = tk.Frame(root, bg='#E6B88C')
frame.place(relx=0.5, rely=0.5, anchor='center')

 
title = tk.Label(frame, text="Select Game Mode", font=("Arial", 28, "bold"), bg='#E6B88C', fg="#2F2F2F")
title.pack(pady=40)


btn_style = {
    "font": ("Arial", 16, "bold"),
    "bg": "#A0522D",
    "fg": "white",
    "activebackground": "#8B4513",
    "activeforeground": "white",
    "width": 20,
    "height": 2,
    "bd": 0
}

tk.Button(frame, text="Human vs AI", command=lambda: start_game("Human vs AI"), **btn_style).pack(pady=20)
tk.Button(frame, text="AI vs AI", command=lambda: start_game("AI vs AI"), **btn_style).pack(pady=10)

root.mainloop()
