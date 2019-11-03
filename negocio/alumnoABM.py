from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
from peewee import JOIN
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



def editarEliminarAlumnosGet(request):
    alumnos = Usuario.select().join(Pais,JOIN.LEFT_OUTER).where((Pais.administrador==None) & (Usuario.esAdmGeneral == False))
    return render_template('editar_eliminar_alumnos.html',alumnos = alumnos)


def editarEliminarAlumnosPost(request):

    listaId = request.form.getlist('id')
    listaEliminar = request.form.getlist('eliminar')
    listaNombre = request.form.getlist('nombre')
    ListaApellido = request.form.getlist('apellido')
    listaDni = request.form.getlist('dni')
    listaClave = request.form.getlist('clave')

    i = -1
    for id in listaId:
        i = i+1
        usuario = Usuario.get(id = int(id))
        if(listaEliminar[i] == '1'):
            usuario.delete_instance()
            continue

        usuario.nombre = listaNombre[i]
        usuario.apellido = ListaApellido[i]
        usuario.dni = listaDni[i]
        usuario.clave = listaClave[i]
        usuario.save()


    return redirect("/editareliminaralumnos", code=302)


def validarAlumnoGet(request):
    validacion = request.args.get("validacion")
    usuario = Usuario.get(validacion = validacion)
    usuario.save()
    return usuario.email + " validado"