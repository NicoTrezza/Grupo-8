from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
from modelo.models import *
from flask import session
import sys


def armarPregunta(examen,codigoPregunta,form):
    
    pregunta = Pregunta.create(examen = examen, texto = "", esChoice = False , esVerdadera = False)
    for item in form.items():
        partes = item[0].split('-')
        if(len(partes) == 2 and int(partes[0]) == codigoPregunta and partes[1] == 'texto'):
            pregunta.texto = item[1]

        if(len(partes) == 2 and int(partes[0]) == codigoPregunta and partes[1] == 'tipo'):
            if(item[1] == 'verdadera'): pregunta.esVerdadera = True
            if(item[1] == 'choice'): pregunta.esChoice = True

    pregunta.save()


    if(pregunta.esChoice):
        for item in form.items():
            partes = item[0].split('-')
            if(len(partes) == 3 and int(partes[0]) == codigoPregunta and partes[2] == 'texto'):
                armarRespuesta(pregunta,codigoPregunta,int(partes[1]),form)

    
    

def armarRespuesta(pregunta,codigoPregunta,codigoRespuesta,form):
    respuesta = Respuesta.create(pregunta = pregunta, texto = "", esCorrecta = False)
    for item in form.items():
        partes = item[0].split('-')
        if(len(partes) == 3 and int(partes[0]) == codigoPregunta and int(partes[1]) == codigoRespuesta ):
            respuesta.texto = item[1]

        if(len(partes) == 2 and int(partes[0]) == codigoPregunta and partes[1] == 'correcta' and int(item[1])==codigoRespuesta):
            respuesta.esCorrecta=True
    respuesta.save()


def crearExamenGet(request):
    usuario = Usuario.traerPorSesion(session)
    if(usuario == None or not usuario.esAdmGeneral):
        return "permiso no valido"
    cursos = Curso.select()
    return render_template('crear_examen.html', cursos = cursos)



def crearExamenPost(request):
    cursos = Curso.select()
    curso = Curso.get(id = int(request.form['curso'] ))
    titulo = request.form['titulo']
    notaMinima =  float(request.form['nota_minima'])
    examen = Examen.create(curso = curso, titulo = titulo, notaMinima = notaMinima)
    examen.save()
    
    for item in request.form.items():
        partes = item[0].split('-')
        if(len(partes) == 2 and  partes[1] == 'texto'):
            armarPregunta(examen,int(partes[0]),request.form)
    return render_template('crear_examen.html', cursos = cursos)