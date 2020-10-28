class Usuario:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

class Categoria:
    def __init__(self,nombre,descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

class Producto(Categoria):
    def __init__(self,nombre,descripcion,precio,categoria,cantidad):
        Categoria.__init__(self, nombre,descripcion)
        self.precio = precio
        self.categoria = categoria
        self.cantidad = cantidad
    
    