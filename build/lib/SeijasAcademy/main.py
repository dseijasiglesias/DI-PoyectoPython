#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import sqlite3 as dbapi
from panel import Panel

__author__ = 'Seijas'


class Login:
    """ Esta es la Clase principal

    Esta clase inicializa una pequeña interfaz, muy simple, realizada con glade,
    Tendremos dos text_fields para rellenar con un usuario y contraseña, si tras el boton de login
    no encuentra el usuario, saltará un aviso especifico conforme no ha encontrado a ese usuario,
    por el contrario, si lo encuentra pero la contraseña no coincide con la base de datos, devolverá
    un aviso en rojo avisando d que no coinciden. En el caso de que ninguna de las dos circunstancias
    anteriores ocuriensen, no dejaria acceder a la interfaz de administracion de la Academia Seijas
    """

    db = dbapi.connect("database.db")
    cursor = db.cursor()

    def __init__(self):
        """ Metodo inicializador

        Constructor que hace visualizar la interfaz realizada con glade
        añadimos las señales definiendolas en el parametro signals y se lo añadimos al builder
        por ultimo, traemos los objetos del xml que usemos
        """

        file = "./views/login.glade"
        builder = Gtk.Builder()
        builder.add_from_file(file)

        signals = {
            "button_login": self.button_login,
            "on_login_destroy": Gtk.main_quit
        }

        builder.connect_signals(signals)

        self.user = builder.get_object("entry_user")
        self.password = builder.get_object("entry_pass")
        self.button_login = builder.get_object("button_login")
        self.window = builder.get_object("window_login")
        self.error = builder.get_object("label_error")

    def button_login(self, control):
        """ Boton login
        Este metodo es llamado cuando se hace click en el boton con label "Login"

        Comprobaremos si el usuario existe en la base de datos (si no existe, se imprime un aviso en rjo en un label)
        Si existe, comprobamos si conciden las contraseñas (de no coincidir imprimimos un aviso en rojo)

        :param control: Parametro para llevar control
        :return: retorna un Panel
        """

        self.error.set_text("")
        writter = 1
        user = self.user.get_text()
        password = self.password.get_text()

        self.cursor.execute("select * from users where name='" + user + "';")

        for result in self.cursor:
            if result[1] == password:
                self.window.set_visible(False)
                Panel(user)
            else:
                self.error.set_text("Datos Incorrectos")
                writter = 0
        if writter:
            self.error.set_text("Usuario no encontrado")

Login()
Gtk.main()
