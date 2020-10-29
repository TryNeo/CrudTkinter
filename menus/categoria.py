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
        self.treeXScroll = ttk.Scrollbar(wrapper_category,orient ="vertical")
        self.treeXScroll.pack( side = tk.RIGHT, fill =  tk.Y )

        self.my_tree_cate  = ttk.Treeview(wrapper_category,columns=(1,2,3),show="headings",height="10",yscrollcommand= self.treeXScroll.set)
        self.my_tree_cate.pack(fill = tk.BOTH )
        self.treeXScroll.config(command=self.my_tree_cate.yview)

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
        query = "SELECT id_categoria,nombre,descripcion FROM categoria WHERE nombre='%s'"
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
        button_list_clear = tk.Button(root, text="recargar", font=("Arial", 12),command=self.list_clear).place(x=370, y=15)
        button_register = tk.Button(root, text="registro", font=("Arial", 12),command=self.register_category).place(x=20, y=55)
        button_edit = tk.Button(root, text="editar", font=("Arial", 12),command=self.list_clear).place(x=120, y=55)
        button_eliminar = tk.Button(root, text="eliminar", font=("Arial", 12),command=self.list_clear).place(x=210, y=55)
        self.list_clear()


    def register_category(self):
        self.registry_win = tk.Toplevel()
        self.registry_win.title('Registro de Categoria')
        self.registry_win.geometry("440x250")
        self.registry_win.resizable(0, 0)

        self.registry_win.update_idletasks()
        width = self.registry_win.winfo_width()
        frm_width = self.registry_win.winfo_rootx() - self.registry_win.winfo_x()
        win_width = width + 2 * frm_width
        height = self.registry_win.winfo_height()
        titlebar_height = self.registry_win.winfo_rooty() - self.registry_win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = self.registry_win.winfo_screenwidth() // 2 - win_width // 2
        y = self.registry_win.winfo_screenheight() // 2 - win_height // 2
        self.registry_win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.registry_win.deiconify()

        title_label = tk.Label(self.registry_win, text="Registro de Categorias", font=("Arial", 20), fg="black").place(x=90,y=0)
        
        self.nombre_c = tk.StringVar()
        label_nombre_c = tk.Label(self.registry_win, text="Nombre:", font=("Arial", 12)).place(x=20, y=50)
        entry_nombre_c = tk.Entry(self.registry_win, width=30, textvariable=self.nombre_c).place(x=120, y=51)

        self.descripcion_c = tk.StringVar()
        label_descripcion_c = tk.Label(self.registry_win, text="Descripcion:", font=("Arial", 12)).place(x=20, y=90)
        entry_descripcion_c = tk.Entry(self.registry_win, width=30, textvariable=self.descripcion_c).place(x=120, y=91)

        button_new = tk.Button(self.registry_win, text="Limpiar", font=("Arial", 12), command=self.clear_category).place(x=20, y=150)
        
        button_registry_sql_category = tk.Button(self.registry_win, text="Registrar", font=("Arial", 12),
                                        command=self.register_sql_category).place(x=280,
                                                                         y=150)
    def clear_category(self):
        self.nombre_c.set("")
        self.descripcion_c.set("")
    
    def register_sql_category(self):        
        self.connecting()
        nombre_c = self.nombre_c.get()
        descripcion_c = self.descripcion_c.get()
        query = "INSERT INTO categoria (nombre,descripcion) values (%s, %s)"
        get_data = (nombre_c,descripcion_c)
        if nombre_c == "" and descripcion_c == "":
            messagebox.showerror(title="Incomplete data", message="Faltan datos")
        else:
            self.mysqlcursor.execute(query, get_data)
            self.mydb.commit()
            messagebox.showinfo(title="Registration completed", message='Correcto nombre y descripcion')
            self.list_clear()