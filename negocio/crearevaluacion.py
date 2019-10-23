from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
from modelo.models import *
from peewee import fn
import sys


cantidadPreguntasRequeridas = 10


def crearEvaluacionGet(request):

    idExamen = 0
    idCursada = 0
    preguntas = None
    examenes = None

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
    evaluacion = Evaluacion.create(examen = examen,titulo = request.form["titulo"], cursada = cursada, fecha = datetime.date(2019, 10, 20))
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