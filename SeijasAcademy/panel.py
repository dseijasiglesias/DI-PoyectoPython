#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import sqlite3 as dbapi
from informes import Informes

__author__ = 'Seijas'


class Panel:
    """ Clase Panel
    clase principal que visualiza el usuario con todos los datos necesarios para la administracion de la cademia
    Esta clase se conecta a la base de datos para aministrar la academia, buscando, insertando, borrando los
    estudiantes que se registren a traves de formularios generados con el propio software
    """

    db = dbapi.connect("database.db")
    cursor = db.cursor()
    last_id = 0

    def __init__(self, user):
        """ metodo __init__
        Construcotr de la clase que hace visualizar la interfaz realizada con glade
        añadimos las señales definiendolas en el parametro signals y se lo añadimos al builder
        por ultimo, traemos los objetos del xml que usemos
        :param user: usuario que con el que se ha aceptado la entrada
        """

        file = "./views/panel.glade"
        builder = Gtk.Builder()
        builder.add_from_file(file)

        signals = {
            "b_borrar": self.b_borrar,
            "b_insertar": self.b_insertar,
            "b_buscar": self.b_buscar,
            "on_MainPanel_destroy": Gtk.main_quit
        }

        builder.connect_signals(signals)

        self.ide = builder.get_object("entry_id")
        self.nome = builder.get_object("entry_nombre")
        self.idade = builder.get_object("entry_edad")
        self.b_borrar = builder.get_object("button_borrar")
        self.b_insertar = builder.get_object("button_insertar")
        self.b_buscar = builder.get_object("button_buscar")
        self.view = builder.get_object("students")
        self.error = builder.get_object("label_error")
        self.menu_bar = builder.get_object("menu_bar")

        render = Gtk.CellRendererText()

        columna1 = Gtk.TreeViewColumn("ID", render, text=0)
        columna2 = Gtk.TreeViewColumn("Nombre", render, text=1)
        columna3 = Gtk.TreeViewColumn("Edad", render, text=2)

        self.view.append_column(columna1)
        self.view.append_column(columna2)
        self.view.append_column(columna3)

        self.menu_bar.set_hexpand(True)

        menuitem = Gtk.MenuItem(label="File")
        self.menu_bar.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="Said 'Hola'")
        menuitem.connect_object("activate", self.menu_warning, ["Seijas Academy", "Hello " + user + "!"])
        menu.append(menuitem)
        menuitem = Gtk.SeparatorMenuItem()
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="Exit")
        menuitem.connect_object("activate", Gtk.main_quit, "close")
        menu.append(menuitem)

        menuitem = Gtk.MenuItem(label="Informes")
        self.menu_bar.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="new registration")
        menuitem.connect_object("activate", self.print_new_registration, None)
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="monthly bill")
        menuitem.connect_object("activate", self.print_monthly_bill, None)
        menu.append(menuitem)

        menuitem = Gtk.MenuItem(label="Ayuda")
        self.menu_bar.append(menuitem)
        menu = Gtk.Menu()
        menuitem.set_submenu(menu)
        menuitem = Gtk.MenuItem(label="Acerca de")
        menuitem.connect_object("activate", self.menu_warning, ["Acerca de...", "Created by Seijas"])
        menu.append(menuitem)

        self.menu_bar.show_all()

        self.update_list()
        self.view.get_selection().connect("changed", self.on_changed)

    def on_changed(self, selection):
        """ metodo on_changed
        metodo para detectar los cambios de selecion en el treeview
        Asigna en los EditText los parametros correspondientes con el elemento selecionado
        :param selection: parametro con la fila del treeview selecionada
        :return: retorna la id del elemento selecionado en la variable de clase last_id
        """
        try:
            (model, iter) = selection.get_selected()
            self.last_id = model[iter][0]

            self.ide.set_text(model[iter][0])
            self.nome.set_text(model[iter][1])
            self.idade.set_text(str(model[iter][2]))
        except:
            self

        return True

    def menu_warning(self, text):
        """ Metodo menu_warning
        Metodo para crear menus emergentes completamente personalizados
        :param text: tubla con disintos parametros texto
        :return: retorna una ventana emergente con los textos dados en la tupla text
        """
        window = Gtk.Window(title=text[0])
        label = Gtk.Label(text[1])
        label.set_padding(100, 30)
        window.add(label)
        window.connect("delete-event", self.close)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

    def close(self, widget, none):
        """ metodo close
        Metodo para cerrar el widget abierto
        :param widget: parametro imprescindible
        :param none: parametro imprescindible, no lo suo
        :return: detruye la ventana
        """
        widget.destroy()

    @staticmethod
    def print_new_registration(control):
        """ metodo print_new_registration
        imprime un pequeño formulario para que los estudiantes se registren en la academia a traves de papel
        :param control: parametro para llevar el control del metodo
        :return: retorna un informe
        """
        Informes(1, control)

    def print_monthly_bill(self, control):
        """ metodo print_monthly_bill
        metodo para generar un informe si esta selecionado una fila en el treeview
        :param control: parametro para llevar el control del metodo
        :return: retorna un informe
        """
        Informes(0, self.last_id)

    def update_list(self):
        """ Metodo update_list
        metodo para imprimir en el treeview con todos datos de la base de datos
        :return: retorna un treeview
        """
        lista = Gtk.ListStore(str, str, int)
        self.cursor.execute("select * from students order by id")

        for fila in self.cursor:
            lista.append(fila)

        self.view.set_model(lista)
        self.view.show()

    def clean_inserts(self):
        """ Metodo clean_inserts
        Metodo para limpiar los tres text fields
        :return: retorna los tres textfields en blanco
        """
        self.ide.set_text("")
        self.nome.set_text("")
        self.idade.set_text("")

    def raise_error(self, string=""):
        """ Metodo raise_error
        metodo usado para insertar un string dado en el label con color rojo raise_error
        :param string: Texto para introducir en el label
        :return: retorna el label con el mensaje introducido
        """
        self.error.set_text(string)

    def b_borrar(self, control):
        """ Metodo borrar
        dependiendo de los parametros que hayamos introducido en los textfields, borramos los elementos, o elemento
        que coincida exactamente con lo deseado
        :param control: parametro para llevar el control del metodo
        :return: retorna la lista del treeview sin el elemento borrado
        """
        self.raise_error()
        id = self.ide.get_text()
        name = self.nome.get_text()
        age = self.idade.get_text()

        if id != "":
            if name == "" and age == "":
                self.cursor.execute("delete from students where id='" + id + "';")
            elif name == "" and age != "":
                self.cursor.execute("delete from students where id='" + id + "' and age=" + age + ";")
            elif name != "" and age == "":
                self.cursor.execute("delete from students where id='" + id + "' and name=" + name + ";")
            elif name != "" and age != "":
                self.cursor.execute("delete from students where id='" + id + "' and age=" + age + " and name='" + name + "';")

        elif name != "":
            if id == "" and age == "":
                self.cursor.execute("delete from students where name='" + name + "';")
            elif id != "" and age == "":
                self.cursor.execute("delete from students where name='" + name + "' and id='" + id + "';")
            elif id == "" and age != "":
                self.cursor.execute("delete from students where name='" + name + "' and age=" + age + ";")

        elif age != "":
            if id == "" and name == "":
                self.cursor.execute("delete from students where age=" + age + ";")
            elif id != "" and name == "":
                self.cursor.execute("delete from students where age=" + age + " and id='" + id + ";")
            elif id == "" and name != "":
                self.cursor.execute("delete from students where age=" + age + " and name='" + name + "';")

        self.db.commit()
        self.clean_inserts()
        self.update_list()

    def b_insertar(self, control):
        """ Metodo insertar
        Lo primero es comprobar que no existe la id introducida, y en su defecto, guardar la ultima id para asignarsela
        a la nueva inserción (si la id insertada manualmente ya existe se rompe el metodo despues de insertar
        un aviso en el label
        Si todo esta bien, dependiendo de los parametros que se hayan introducido en los treeview hacemos una insercion
        u otra
        :param control: parametros para llevar el control del metodo
        :return: vuelve a retornar un treeview con todos los elementos de la base de datos
        """
        id = self.ide.get_text()
        name = self.nome.get_text()
        age = self.idade.get_text()

        self.cursor.execute("select id from students order by id")

        tupla_id = []
        for fila in self.cursor:
            tupla_id.append(int(fila[0]))

        is_ok = False
        is_repead = False
        if id != "":
            for j in tupla_id:
                if j == int(id):
                    is_repead = True
                    break

        if is_repead:
            self.raise_error("Error: ID repetida")
        elif id != "":
            if name == "" and age == "":
                self.raise_error("Error: nombre requerido para la insercion")
            elif name == "" and age != "":
                self.raise_error("Error: nombre requerido para la insercion")
            elif name != "" and age == "":
                self.cursor.execute("insert into students values('" + id + "', '" + name + "', null)")
                is_ok = True
            elif name != "" and age != "":
                self.cursor.execute("insert into students values('" + id + "', '" + name + "', " + age + ")")
                is_ok = True
        else:
            new_id = 1
            for x in tupla_id:
                if x == new_id:
                    new_id += 1
                else:
                    break

            if name != "" and age == "":
                self.cursor.execute("insert into students values('" + str(new_id) + "', '" + name + "', null)")
                is_ok = True
            elif name != "" and age != "":
                self.cursor.execute("insert into students values('" + str(new_id) + "', '" + name + "', " + age + ")")
                is_ok = True
            else:
                self.raise_error("Error: nombre requerido para la inserción")

        self.db.commit()
        if is_ok:
            self.update_list()
            self.clean_inserts()
            self.raise_error()

    def b_buscar(self, control):
        """ Metodo buscar
        Dependiendo del texto que rellenemos en los textfields hacemos un select u otro para mostrar los
        resultados en el treeview
        :param control: parametro para llevar control
        :return: retorna la lista para el treeview con los parametros que coinciden en la base de datos
        """
        self.raise_error()
        id = self.ide.get_text()
        name = self.nome.get_text()
        age = self.idade.get_text()

        if id != "":
            if name == "" and age == "":
                self.cursor.execute("select * from students where id='" + id + "';")
            elif name == "" and age != "":
                self.cursor.execute("select * from students where id='" + id + "' and age=" + age + ";")
            elif name != "" and age == "":
                self.cursor.execute("select * from students where id='" + id + "' and name=" + name + ";")
            elif name != "" and age != "":
                self.cursor.execute("select * from students where id='" + id + "' and age=" + age + " and name='" + name + "';")

        elif name != "":
            if id == "" and age == "":
                self.cursor.execute("select * from students where name='" + name + "';")
            elif id != "" and age == "":
                self.cursor.execute("select * from students where name='" + name + "' and id='" + id + "';")
            elif id == "" and age != "":
                self.cursor.execute("select * from students where name='" + name + "' and age=" + age + ";")

        elif age != "":
            if id == "" and name == "":
                self.cursor.execute("select * from students where age=" + age + ";")
            elif id != "" and name == "":
                self.cursor.execute("select * from students where age=" + age + " and id='" + id + ";")
            elif id == "" and name != "":
                self.cursor.execute("select * from students where age=" + age + " and name='" + name + "';")

        elif id == "" and age == "" and name == "":
            self.cursor.execute("select * from students order by id")
        else:
            self.raise_error("Error: Búsqueda no contemplada en código")

        lista = Gtk.ListStore(str, str, int)

        for fila in self.cursor:
            lista.append(fila)

        self.view.set_model(lista)
        self.view.show()
        self.clean_inserts()
