from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
import dateparser
from modelo.models import *
from peewee import fn
from flask import session
import sys


cantidadPreguntasRequeridas = 10


def crearEvaluacionGet(request):

    idExamen = 0
    idCursada = 0
    preguntas = None
    examenes = None

    usuario = Usuario.traerPorSesion(session)
    if(usuario == None or not usuario.esAdmGeneral):
        return "permiso no valido"


    cursadas = Cursada.select()
    if(request.args.get("cursada") != None):
        idCursada = int(request.args.get("cursada"))
    else:
        if(len(cursadas)>0): idCursada = cursadas[0].id


    examenes = Cursada.get(id=idCursada).curso.examenes

    if(request.args.get("examen") != None):
        idExamen = int(request.args.get("examen"))
    else:
        if(len(examenes)>0): idExamen = examenes[0].id


    if(len(examenes)>0): preguntas = Examen.get(id=idExamen).preguntas

    return render_template('crear_evaluacion.html',cursadas = cursadas,idCursada = idCursada, examenes = examenes,idExamen = idExamen , preguntas = preguntas)



def crearEvaluacionPost(request):

    cursada = Cursada.get(id = request.form["cursada"])
    examen = Examen.get(id = request.form["examen"])
    titulo = request.form["titulo"]
    fecha = dateparser.parse(request.form['fecha']).date()
    evaluacion = Evaluacion.create(examen = examen,titulo = titulo, cursada = cursada, fecha = fecha)
    evaluacion.save()
    idsSeleccionadas = []


    for item in request.form.items():
        partes = item[0].split('-')
        if(len(partes) == 2 and  partes[0] == 'pregunta'):
            idsSeleccionadas.append(int(partes[1]))

    preguntas = Pregunta.select().where(Pregunta.id << idsSeleccionadas)

    evaluacion.preguntas.add(preguntas)

    if(len(idsSeleccionadas) < cantidadPreguntasRequeridas):
        preguntas = Pregunta.select().where((Pregunta.examen == examen) & ~(Pregunta.id << idsSeleccionadas))
        preguntas = preguntas.order_by(fn.Random()).limit(cantidadPreguntasRequeridas - len(idsSeleccionadas))


    evaluacion.preguntas.add(preguntas)
    evaluacion.save()
    return redirect("/crearevaluacion")