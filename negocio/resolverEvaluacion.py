from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
from flask import session
import dateparser
from modelo.models import *
from peewee import fn
import sys



def evaluacionesPendientesGet(request):
    usuario = Usuario.traerPorSesion(session)
    if(usuario == None):
        return "permiso no valido"

    evaluaciones= Evaluacion.select().where(~(Evaluacion.id << Nota.select().where(Nota.alumno == usuario)))
    return render_template('evaluaciones_pendientes.html',evaluaciones = evaluaciones)


def resolverEvaluacionGet(request):
    usuario = Usuario.traerPorSesion(session)
    if(usuario == None):
        return "permiso no valido"

    idEvaluacion = int(request.args.get("evaluacion"))
    evaluacion = Evaluacion.get(id = idEvaluacion)


    if(Nota.select().where((Nota.alumno == usuario) & (Nota.evaluacion==evaluacion)).count()>0): return "evaluacion ya resuelta"


    return render_template('resolver_evaluacion.html',idEvaluacion = idEvaluacion,preguntas = evaluacion.preguntas)


def resolverEvaluacionPost(request): 
    idEvaluacion = int(request.args.get("evaluacion"))
    evaluacion = Evaluacion.get(id = idEvaluacion)
    alumno = Usuario.get(id=1) #a modo de prueba de momento
    preguntasQueRespondioVerdaderas = []

    for item in request.form.items():
        partes = item[0].split('-')
        if(len(partes) == 2 and  partes[0] == 'pregunta'):
            pregunta = Pregunta.get(id=int(partes[1]))
            respuestaDelAlumno = RespuestaDelAlumno.create(alumno = alumno, evaluacion = evaluacion, pregunta = pregunta,respondioVerdadera = True)
            if(not pregunta.esChoice):
                preguntasQueRespondioVerdaderas.append(pregunta)
            else:
                respuesta = Respuesta.get(id= int(request.form[item[0]]))
                respuestaDelAlumno.respuesta = respuesta
            respuestaDelAlumno.save()


    preguntasQueRespondioFalsas = evaluacion.preguntas.where((Pregunta.esChoice == False) & ~(Pregunta.id << preguntasQueRespondioVerdaderas) )

    for pregunta in preguntasQueRespondioFalsas:
        respuestaDelAlumno = RespuestaDelAlumno.create(alumno = alumno, evaluacion = evaluacion, pregunta = pregunta,respondioVerdadera = False)
        respuestaDelAlumno.save()

    ############ CALIFICACION SEGURO DESPUES VA EN OTRA VISTA ############

    respuestaDelAlumno = RespuestaDelAlumno.select().where(RespuestaDelAlumno.evaluacion == evaluacion & RespuestaDelAlumno.alumno == alumno)

    cantidadCorrectas  = 0
    for respuestaDelalumno in respuestaDelAlumno:
        if(respuestaDelalumno.pregunta.esChoice):
            if(respuestaDelalumno.respuesta.esCorrecta): 
                cantidadCorrectas = cantidadCorrectas + 1
        else:
            if(respuestaDelalumno.pregunta.esVerdadera == respuestaDelalumno.respondioVerdadera):
                cantidadCorrectas = cantidadCorrectas + 1

    nota = Nota.create(evaluacion = evaluacion ,alumno = alumno , nota = cantidadCorrectas)
    nota.save()

    return str(cantidadCorrectas) + " respuestas correctas"
