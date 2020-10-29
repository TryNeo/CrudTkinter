from tkinter import ttk
from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector


class Usuario:

    def __init__(self, window):
        self.wind = window
        self.wind.title("Usuarios")


        #crear contenedor
        frame = LabelFrame(self.wind, text='Registrar un nuevo Usuarios')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Name_imput
        Label(frame, text="Usuario_id: ").grid(row=1, column=0)
        self.usuario = Entry(frame)
        self.usuario.focus()
        self.usuario.grid(row=1, column=1)

        Label(frame, text="Nombre: ").grid(row=2, column=0)
        self.name = Entry(frame)
        self.name.grid(row=2, column=1)

        Label(frame, text="Apellido: ").grid(row=3, column=0)
        self.apellido = Entry(frame)
        self.apellido.grid(row=3, column=1)

        Label(frame, text="Edad: ").grid(row=4, column=0)
        self.edad = Entry(frame)
        self.edad.grid(row=4, column=1)

        Label(frame, text="Correo: ").grid(row=5, column=0)
        self.correo = Entry(frame)
        self.correo.grid(row=5, column=1)

        #boton
        ttk.Button(frame, text='Guardar Usuario', command=self.add_user).grid(row=6, columnspan=2, sticky=W + E)
        ttk.Button(text='DELETE', command= self.delete_user).grid(row=7, column=0, sticky= W + E)
        ttk.Button(text='UPDATE', command= self.edit_user).grid(row=7, column=1, sticky=W + E)


        #Tabla para listar
        self.tree = ttk.Treeview(height=10, columns=('0', '1', '2','3'))
        self.tree.grid(row=6, column=0, columnspan=2)
        self.tree.heading('#0', text='Usuario_id', anchor=CENTER)
        self.tree.heading('#1', text='Nombre', anchor=CENTER)
        self.tree.heading('#2', text='Apellido', anchor=CENTER)
        self.tree.heading('#3', text='Edad', anchor=CENTER)
        self.tree.heading('#4', text='Correo', anchor=CENTER)

        #llenar filas
        self.get_usuarios()

    def get_usuarios(self):
        self.connecting()
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        self.cursor=self.mydb.cursor()
        self.cursor.execute("Select * from usuario order by idusuario desc ")
        rows=self.cursor.fetchall()
        for row in rows:
            self.tree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]))

    def validation(self):
        return len(self.usuario.get()) != 0 and len(self.name.get()) != 0

    def add_user(self):
        self.connecting()
        if self.validation():
            query = "INSERT INTO usuario (idusuario,nombre,apellido,edad,correo) values (%s, %s, %s, %s, %s)"
            parameters=(self.usuario.get(), self.name.get(), self.apellido.get(), self.edad.get(), self.correo.get())
            self.cursor.execute(query, parameters)
            self.cursor.execute('commit')
            MessageBox.showinfo('Data Saved', 'Usuario {} guardado correctamente'.format(self.name.get()))
            self.usuario.delete(0, END)
            self.name.delete(0, END)
            self.apellido.delete(0, END)
            self.edad.delete(0, END)
            self.correo.delete(0, END)
        else:
            MessageBox.showerror('Error', 'Campos Requeridos')

        self.get_usuarios()

    def delete_user(self):
        self.connecting()

        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            MessageBox.showerror("Error", 'Por favor, seleccione un registro')
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        query = "DELETE FROM usuario WHERE (nombre) = (%s)"
        self.cursor.execute(query, (name, ))
        self.cursor.execute('commit')
        MessageBox.showinfo("Data saved", "Registro {} eliminado satisfactoriamente".format(name))
        self.get_usuarios()

    def edit_user(self):
        self.connecting()

        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            MessageBox.showerror("Error", 'Por favor, seleccione un registro')
            return
        name = self.tree.item(self.tree.selection())['values'][3]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar usuario'

        Label(self.edit_wind, text='Old_email:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value= name), state='readonly').grid(row=0, column=2)

        Label(self.edit_wind, text='New_email:').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        Button(self.edit_wind, text='Update', command=lambda: self.edit_records(new_name.get(), name)).grid(row=4, column=2, sticky=W)

    def edit_records(self, new_name, name):
        self.connecting()
        query = "UPDATE usuario SET correo = (%s) where correo = (%s)"
        parameters=(new_name, name)
        self.cursor.execute(query, parameters)
        self.cursor.execute('commit')
        self.edit_wind.destroy()
        MessageBox.showinfo('Data saved', 'Usuario {} actualizado correctamente'.format(name))
        self.get_usuarios()

      #Connection Mysql#
    def connecting(self):
        try:
            self.mydb = mysql.connector.connect(host='localhost',
                                           user='root',
                                           password='admin',
                                           db='pro_belen')
            self.cursor = self.mydb.cursor()
        except mysql.connector.errors.ProgrammingError as error:
            print("Review the Error -->", error)
        finally:
            print("connection successfully")


if __name__ == '__main__':
    window = Tk()
    aplicacion = Usuario(window)
    window.mainloop()


