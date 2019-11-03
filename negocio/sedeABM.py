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



def altaSedeGet(request):
    paises =  Pais.select()
    return render_template('alta_sede.html', paises = paises)


def altaSedePost(request):

    nombre = request.form["nombre"]
    emailAdministrador = request.form["administrador"]
    idPais = request.form["pais"]

    try:
        administrador = Usuario.get(email = emailAdministrador)
    except  Usuario.DoesNotExist:
        return  "El usuario " + emailAdministrador + " no existe"

    pais = Pais.get(id = int(idPais))

    sede = Sede.create(nombre = nombre, administrador = administrador,pais = pais)
    sede.save()

    return render_template('alta_sede.html')



def editarEliminarSedesGet(request):
    sedes = Sede.select()
    paises = Pais.select()
    return render_template('editar_eliminar_sedes.html',sedes = sedes , paises=paises)


def editarEliminarSedesPost(request):

    listaId = request.form.getlist('id')
    listaEliminar = request.form.getlist('eliminar')
    listaNombre = request.form.getlist('nombre')
    listaPais= request.form.getlist('pais')
    listaAdministrador = request.form.getlist('administrador')

    i = -1
    for id in listaId:
        i = i+1
        
        try:
            administrador = Usuario.get(email = listaAdministrador[i])
        except  Usuario.DoesNotExist:
            return  "El usuario " + listaAdministrador[i] + " no existe"


        pais = Pais.get(id = int(listaPais[i]))
        sede = Sede.get(id = int(id))

        if(listaEliminar[i] == '1'):
            sede.delete_instance()
            continue
        sede.administrador = administrador
        sede.nombre = listaNombre[i]
        sede.pais = pais
        sede.save()

    return redirect("/editareliminarsedes", code=302)

