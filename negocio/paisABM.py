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



def altaPaisGet(request):
    return render_template('alta_pais.html')


def altaPaisPost(request):

    nombre = request.form["nombre"]
    emailAdministrador = request.form["administrador"]

    try:
        administrador = Usuario.get(email = emailAdministrador)
    except  Usuario.DoesNotExist:
        return  "El usuario " + emailAdministrador + " no existe"


    pais = Pais.create(nombre = nombre, administrador = administrador)
    pais.save()

    return render_template('alta_pais.html')



def editarEliminarPaisesGet(request):
    paises = Pais.select()
    return render_template('editar_eliminar_paises.html',paises = paises)


def editarEliminarPaisesPost(request):

    listaId = request.form.getlist('id')
    listaEliminar = request.form.getlist('eliminar')
    listaNombre = request.form.getlist('nombre')
    listaAdministrador = request.form.getlist('administrador')

    i = -1
    for id in listaId:
        i = i+1
        
        try:
            administrador = Usuario.get(email = listaAdministrador[i])
        except  Usuario.DoesNotExist:
            return  "El usuario " + listaAdministrador[i] + " no existe"
        pais = Pais.get(id = int(id))
        if(listaEliminar[i] == '1'):
            pais.delete_instance()
            continue
        pais.administrador = administrador
        pais.nombre = listaNombre[i]

        pais.save()


    return redirect("/editareliminarpaises", code=302)

