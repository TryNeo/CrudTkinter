import tkinter as tk
import mysql.connector
from tkinter import *
import tkinter.messagebox as MessageBox
from menus.principal import *

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
        self.my_tree_cate.bind('<Double 1>',self.list_get)

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
        query = "SELECT id_categoria,nombre,descripcion FROM categoria where nombre =%s" #BUG 
        get_data = (search_list,)
        self.mysqlcursor.execute(query,get_data)
        rows = self.mysqlcursor.fetchall()
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
        self.search = tk.StringVar()
        label_search = tk.Label(root, text="Buscador:", font=("Arial", 12)).place(x=15, y=20)
        entry_search = tk.Entry(root, width=20, textvariable=self.search).place(x=100, y=20)
        button_search = tk.Button(root, text="Buscar", font=("Arial", 12),command=self.list_search).place(x=280, y=15)
        button_list_clear = tk.Button(root, text="recargar", font=("Arial", 12),command=self.list_clear).place(x=370, y=15)
        button_register = tk.Button(root, text="registro", font=("Arial", 12),command=self.register_category).place(x=20, y=55)
        button_edit = tk.Button(root, text="editar", font=("Arial", 12),command=self.edit_category).place(x=120, y=55)
        button_eliminar = tk.Button(root, text="eliminar", font=("Arial", 12),command=self.delete_category).place(x=210, y=55)

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

        self.nombre_c = tk.StringVar()
        self.descripcion_c = tk.StringVar()

        title_label = tk.Label(self.registry_win, text="Registro de Categorias", font=("Arial", 20), fg="black").place(x=90,y=0)
        
        label_nombre_c = tk.Label(self.registry_win, text="Nombre:", font=("Arial", 12)).place(x=20, y=50)
        entry_nombre_c = tk.Entry(self.registry_win, width=30, textvariable=self.nombre_c).place(x=120, y=51)

        label_descripcion_c = tk.Label(self.registry_win, text="Descripcion:", font=("Arial", 12)).place(x=20, y=90)
        entry_descripcion_c = tk.Entry(self.registry_win, width=30, textvariable=self.descripcion_c).place(x=120, y=91)

        button_new = tk.Button(self.registry_win, text="Limpiar", font=("Arial", 12), command=self.clear_category).place(x=20, y=150)
        
        button_registry_sql_category = tk.Button(self.registry_win, text="Registrar", font=("Arial", 12),
                                        command=self.register_sql_category).place(x=280,
                                                                         y=150)
    def clear_category(self):
        if self.nombre_edit_c:
            self.nombre_edit_c.set("")
            self.descripcion_edit_c.set("")
        else:
            self.nombre_c.set("")
            self.descripcion_c.set("")

    def list_get(self,event):
        row_id = self.my_tree_cate.identify_row(event.y)
        item =  self.my_tree_cate.item(self.my_tree_cate.focus())
        self.id_categoria_edit_c.set(item['values'][0])
        self.nombre_edit_c.set(item['values'][1])
        self.descripcion_edit_c.set(item['values'][2])
    
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
    
    def edit_category(self):
        try:
            self.my_tree_cate.item(self.my_tree_cate.selection())['values'][0]

            self.edit_win = tk.Toplevel()
            self.edit_win.title('Editar de Categoria')
            self.edit_win.geometry("440x250")
            self.edit_win.resizable(0, 0)
            
            #########centered screen##############
            self.edit_win.update_idletasks()
            width = self.edit_win.winfo_width()
            frm_width = self.edit_win.winfo_rootx() - self.edit_win.winfo_x()
            win_width = width + 2 * frm_width
            height = self.edit_win.winfo_height()
            titlebar_height = self.edit_win.winfo_rooty() - self.edit_win.winfo_y()
            win_height = height + titlebar_height + frm_width
            x = self.edit_win.winfo_screenwidth() // 2 - win_width // 2
            y = self.edit_win.winfo_screenheight() // 2 - win_height // 2
            self.edit_win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            self.edit_win.deiconify()
            
            self.id_categoria_edit_c = tk.StringVar()
            self.nombre_edit_c = tk.StringVar() 
            self.descripcion_edit_c =  tk.StringVar()
            self.id_categoria_edit_c.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][0])
            self.nombre_edit_c.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][1])
            self.descripcion_edit_c.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][2])

            title_label = tk.Label(self.edit_win, text="Editar Categoria", font=("Arial", 20), fg="black").place(x=90,y=0)
            label_nombre_c = tk.Label(self.edit_win, text="Nombre:", font=("Arial", 12)).place(x=20, y=50)
            entry_nombre_c = tk.Entry(self.edit_win, width=30, textvariable=self.nombre_edit_c).place(x=120, y=51)

            label_descripcion_c = tk.Label(self.edit_win, text="Descripcion:", font=("Arial", 12)).place(x=20, y=90)
            entry_descripcion_c = tk.Entry(self.edit_win, width=30,textvariable=self.descripcion_edit_c).place(x=120, y=91)

            button_new = tk.Button(self.edit_win, text="Limpiar", font=("Arial", 12), command=self.clear_category).place(x=20, y=150)

            button_edit_sql_category = tk.Button(self.edit_win, text="Editar", font=("Arial", 12),
                                        command=self.edit_sql_category).place(x=280,
                                                                         y=150)
        except IndexError as e:
            MessageBox.showerror("Error", 'Por favor, seleccione un registro')

    def edit_sql_category(self):
        self.connecting()
        id_categoria_edit_c = int(self.id_categoria_edit_c.get())
        nombre_edit_c = self.nombre_edit_c.get()
        descripcion_edit_c = self.descripcion_edit_c.get()
        query = "UPDATE categoria SET nombre = (%s), descripcion = (%s) WHERE id_categoria = (%s)"
        get_data = (nombre_edit_c,descripcion_edit_c,id_categoria_edit_c)
        if nombre_edit_c == "" and descripcion_edit_c == "":
            messagebox.showerror(title="Incomplete data", message="Faltan datos")
        else:
            self.mysqlcursor.execute(query, get_data)
            self.mydb.commit()
            messagebox.showinfo(title="Edit Completed", message='Nombre y descripcion editado Correctamente')
            self.list_clear()
    
    def delete_category(self):
        try:
            self.my_tree_cate.item(self.my_tree_cate.selection())['values'][0]

            self.del_win = tk.Toplevel()
            self.del_win.title('Eliminar Categoria')
            self.del_win.geometry("440x150")
            self.del_win.resizable(0, 0)
            
            #########centered screen##############
            self.del_win.update_idletasks()
            width = self.del_win.winfo_width()
            frm_width = self.del_win.winfo_rootx() - self.del_win.winfo_x()
            win_width = width + 2 * frm_width
            height = self.del_win.winfo_height()
            titlebar_height = self.del_win.winfo_rooty() - self.del_win.winfo_y()
            win_height = height + titlebar_height + frm_width
            x = self.del_win.winfo_screenwidth() // 2 - win_width // 2
            y = self.del_win.winfo_screenheight() // 2 - win_height // 2
            self.del_win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            self.del_win.deiconify()

            self.id_categoria_del_c = tk.StringVar()
            self.id_categoria_del_c.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][0])

            self.nombre_del_c = tk.StringVar() 
            self.nombre_del_c.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][1])

            title_label = tk.Label(self.del_win, text="Eliminar Categoria", font=("Arial", 20), fg="black").place(x=100,y=0)
            
            button_new = tk.Button(self.del_win, text="Si", font=("Arial", 12)).place(x=120, y=70)

            button_del_sql_category = tk.Button(self.del_win, text="No", font=("Arial", 12),
                                        command=self.destroy_ven).place(x=260,
                                                                         y=70)
        except IndexError as e:
            MessageBox.showerror("Error", 'Por favor, seleccione un registro')

    def destroy_ven(self):
        self.del_win.destroy()

    def delete_sql_category(self):
        self.connecting()
        id_categoria_del_c = int(self.id_categoria_del_c.get())
        query = "DELETE FROM categoria WHERE id_categoria = %s"
        if id_categoria_del_c:
            self.mysqlcursor.execute(query,(id_categoria_del_c))
            self.mydb.commit()
            messagebox.showinfo(title="Delete Completed", message='Registro Eliminado correctamente')
            self.list_clear()
        else:
            messagebox.showerror(title="Incomplete data", message="No existe ese dato")
