import tkinter as tk
from tkinter import ttk, messagebox
from dominio.entidades import Categoria

class MainWindowC(Categoria):
    def __init__(self, root):
        root.title('Categoria')
        root.geometry("800x700")
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

        self.list_category(root)
        

    #########Connection Mysql###########
    def connecting(self):
        try:
            self.mydb = mysql.connector.connect(host='localhost',
                                                user='root',
                                                passwd='admin',
                                                db='crudTk')
            self.mysqlcursor = self.mydb.cursor()
        except mysql.connector.errors.ProgrammingError as error:
            print("Review the Error -->", error)
        finally:
            print("connection successfully")

    def list_category(self,root):
        self.connecting()
        my_tree_cate  = ttk.Treeview(root, columns = ("ID","NOMBRE","DESCRIPCION"),selectmode="extended", height=200    )
        my_tree_cate.heading('ID', text="ID",anchor=tk.W)
        my_tree_cate.heading('NOMBRE', text="NOMBRE",anchor=tk.W)
        my_tree_cate.heading('DESCRIPCION', text="DESCRIPCION",anchor=tk.W)
        my_tree_cate.column('#0',stretch=tk.NO,minwidth=0, width=0)
        my_tree_cate.column('#1',stretch=tk.NO,minwidth=0, width=0)
        my_tree_cate.column('#2',stretch=tk.NO,minwidth=0, width=80)
        my_tree_cate.pack()