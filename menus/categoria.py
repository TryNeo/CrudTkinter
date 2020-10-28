import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox

class MainWindowC:
    def __init__(self, root):
        root.title('Categoria')
        root.geometry("700x800")
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

        self.search = tk.StringVar()
        label_search = tk.Label(root, text="Buscador:", font=("Arial", 12)).place(x=15, y=50)
        entry_search = tk.Entry(root, width=30, textvariable=self.search).place(x=100, y=50)
        button_search = tk.Button(root, text="Buscar", font=("Arial", 12),command=self.list_search).place(x=350, y=45)

        self.registry_category(root)
        self.list_category(root)

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
    
    def list_search(self):
        search = self.search.get()
        print(search)

    def list_update(self,my_tree_cate=None):
        self.connecting()
        search = self.search.get()
        if search:
            query =  "SELECT id_categoria,nombre,descripcion FROM categoria WHERE nombre = %s"
            get_data = (search,)
            self.mysqlcursor.execute(query,get_data)
            rows = self.mysqlcursor.fetchall()
        else:
            query = "SELECT id_categoria,nombre,descripcion FROM categoria"
            self.mysqlcursor.execute(query)
            rows = self.mysqlcursor.fetchall()
        my_tree_cate.delete(*my_tree_cate.get_children())
        for i in rows:
            my_tree_cate.insert('','end',values=i)


    def registry_category(self,root):
        wrapper_category_reg = tk.LabelFrame(root,text="Categoria")
        wrapper_category_reg.pack(fill="both",expand="yes",padx=20,pady=100)
        title_label = tk.Label(wrapper_category_reg, text="Registro de usuarios", font=("Arial", 10), fg="black").place(x=90,
                                                                                                         y=0)


    def list_category(self,root):
        wrapper_category = tk.LabelFrame(root,text="Listado de Categoria")
        wrapper_category.pack(fill="both",expand="yes",padx=20,pady=100)
        my_tree_cate  = ttk.Treeview(wrapper_category,columns=(1,2,3),show="headings",height="6")
        my_tree_cate.pack()
        my_tree_cate.heading(1,text="ID")
        my_tree_cate.heading(2,text="NOMBRE")
        my_tree_cate.heading(3,text="DESCRIPCION")
        self.list_update(my_tree_cate)
