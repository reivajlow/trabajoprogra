from tkinter import ttk
from tkinter import *

import sqlite3


class Product:
    # conectar db
    db_name = 'database2.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Biblioteca')

        # frame ingreso
        frame = LabelFrame(self.wind, text='Registrar nuevo libro')
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # nombre input
        Label(frame, text='Nombre: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # estado Input
        Label(frame, text='estado: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Button add libro
        ttk.Button(frame, text='agregar libro', command=self.add_product).grid(row=3, columnspan=2, sticky=W + E)

        # mensaje
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Tabla
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='estado', anchor=CENTER)

        # Buttons
        ttk.Button(text='Eliminar', command=self.delete_product).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='Editar', command=self.edit_product).grid(row=5, column=1, sticky=W + E)

        self.get_products()

    # Funcion consulta
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            resu = cursor.execute(query, parameters)
            conn.commit()
        return resu

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # get data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # print data
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    # validacion de texto ingresado
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Libro {} agregado correctamente'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Nombre y estado es necesario'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccione un libro'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Libro {} eliminado correctamente'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor seleccione un libro'
            return
        name = self.tree.item(self.tree.selection())['text']
        estado = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar libro'

        Label(self.edit_wind, text='nombre:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly').grid(row=0,
                                                                                                         column=2)
        Label(self.edit_wind, text='Nuevo nombre:').grid(row=1, column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1, column=2)

        Label(self.edit_wind, text='estado:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=estado), state='readonly').grid(row=2,
                                                                                                              column=2)
        Label(self.edit_wind, text='nuevo estado:').grid(row=3, column=1)
        nuevo_estado = Entry(self.edit_wind)
        nuevo_estado.grid(row=3, column=2)

        Button(self.edit_wind, text='Actualizar',
               command=lambda: self.edit_records(new_name.get(), name, nuevo_estado.get(), estado)).grid(row=4,
                                                                                                         column=2,
                                                                                                         sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_estado, estado):
        if len(new_name) != 0 and len(new_estado) != 0:
            query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
            parameters = (new_name, new_estado, name, estado)
            self.run_query(query, parameters)
            self.edit_wind.destroy()
            self.message['text'] = 'Libro {} actualizado correctamente'.format(new_name)
            self.get_products()
        else:
            self.edit_wind.destroy()
            self.message['text'] = 'ingrese nombre y estado'.format(name)
            self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()
