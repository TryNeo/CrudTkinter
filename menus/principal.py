import tkinter as tk
from tkinter import ttk, messagebox
from menus.categoria import MainWindowC

class MainWindowP:
    def __init__(self, root):
        root.title('Menu')
        root.geometry("500x400")
        root.resizable(0, 0)

        #########centered screen##############
        root.update_idletasks()
        width = root.winfo_width()
        frm_width = root.winfo_rootx() - root.winfo_x()
        win_width = width + 2 * frm_width
        height = root.winfo_height()
        titlebar_height = root.winfo_rooty() - root.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = root.winfo_screenwidth() // 2 - win_width // 2
        y = root.winfo_screenheight() // 2 - win_height // 2
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        root.deiconify()

        button_categoria = tk.Button(root, text="Categoria",\
            height=2, width=10,font=("Arial", 12), \
            command=self.open_categoria).place(x=50,y=50)

                                                                                    
    def open_categoria(self):
        main_c = tk.Tk()
        window_c = MainWindowC(main_c)
        main_c.mainloop()
