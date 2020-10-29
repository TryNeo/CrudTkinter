import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox

class MainWindowC:
    def __init__(self, root):
        root.title('Categoria')
        root.geometry("700x450")
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
        
        wrapper_category = tk.LabelFrame(root,text="Listado de Categoria")
        wrapper_category.pack(fill="both",expand="yes",padx=20,pady=100)
        self.my_tree_cate  = ttk.Treeview(wrapper_category,columns=(1,2,3),show="headings",height="10")
        self.my_tree_cate.pack()
        self.my_tree_cate.heading(1,text="ID")
        self.my_tree_cate.heading(2,text="NOMBRE")
        self.my_tree_cate.heading(3,text="DESCRIPCION")

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
        self.connecting()
        search_list = self.search.get()
        query = "SELECT id_categoria,nombre,descripcion FROM categoria WHERE nombre=%s"
        parameters=(search_list)
        self.mysqlcursor.execute(query,parameters)
        rows = self.mysqlcursor.fetchall()
        print(rows)
        self.list_update(rows)
    
    def list_update(self,rows):
        self.my_tree_cate.delete(*self.my_tree_cate.get_children())
        for i in rows:
            self.my_tree_cate.insert('','end',values=i)
    
    def list_clear(self):
        query = "SELECT id_categoria,nombre,descripcion FROM categoria"
        self.mysqlcursor.execute(query)
        rows = self.mysqlcursor.fetchall()
        self.list_update(rows)

    
    def list_category(self,root):
        self.connecting()
        label_search = tk.Label(root, text="Buscador:", font=("Arial", 12)).place(x=15, y=20)
        entry_search = tk.Entry(root, width=20, textvariable=self.search).place(x=100, y=20)
        button_search = tk.Button(root, text="Buscar", font=("Arial", 12),command=self.list_search).place(x=280, y=15)
        button_list_clear = tk.Button(root, text="restaurar listado", font=("Arial", 12),command=self.list_clear).place(x=370, y=15)
        button_register = tk.Button(root, text="registro", font=("Arial", 12),command=self.list_clear).place(x=20, y=55)
        button_edit = tk.Button(root, text="editar", font=("Arial", 12),command=self.list_clear).place(x=120, y=55)
        button_eliminar = tk.Button(root, text="editar", font=("Arial", 12),command=self.list_clear).place(x=210, y=55)

        query = "SELECT id_categoria,nombre,descripcion FROM categoria"
        self.mysqlcursor.execute(query)
        rows = self.mysqlcursor.fetchall()
        self.list_update(rows)
