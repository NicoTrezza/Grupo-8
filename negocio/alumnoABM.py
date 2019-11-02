from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
import dateparser
import flask
from modelo.models import *
from peewee import fn
import sys



def altaAlumnonGet(request):
    return render_template('alta_alumno.html')


def altaAlumnonPost(request):

    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    dni = request.form["dni"]
    email = request.form["email"]
    clave = request.form["clave"]


    usuario = Usuario.create(nombre = nombre, apellido = apellido, dni = dni, email = email, clave = clave)
    usuario.generarValidacion()
    usuario.save()


    return flask.url_for("validarAlumno" , validacion = usuario.validacion, _external=True )




def validarAlumnoGet(request):
    validacion = request.args.get("validacion")
    usuario = Usuario.get(validacion = validacion)
    usuario.save()
    return usuario.email + " validado"