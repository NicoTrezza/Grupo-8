#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import session
from flask_wtf import CSRFProtect
from modelo.models import *
from negocio.crearExamen import crearExamenGet
from negocio.crearExamen import crearExamenPost
from negocio.crearevaluacion import crearEvaluacionGet
from negocio.crearevaluacion import crearEvaluacionPost
from negocio.resolverEvaluacion import evaluacionesPendientesGet
from negocio.resolverEvaluacion import resolverEvaluacionGet
from negocio.resolverEvaluacion import resolverEvaluacionPost
from negocio.alumnoABM import altaAlumnoGet
from negocio.alumnoABM import altaAlumnoPost
from negocio.alumnoABM import validarAlumnoGet
from negocio.alumnoABM import editarEliminarAlumnosGet
from negocio.alumnoABM import editarEliminarAlumnosPost
from negocio.paisABM import altaPaisGet
from negocio.paisABM import altaPaisPost
from negocio.paisABM import editarEliminarPaisesGet
from negocio.paisABM import editarEliminarPaisesPost
from negocio.sedeABM import altaSedeGet
from negocio.sedeABM import altaSedePost
from negocio.sedeABM import editarEliminarSedesGet
from negocio.sedeABM import editarEliminarSedesPost

import sys




app = Flask(__name__, template_folder="templates")
app.secret_key = "estaeslaclavesecretadelgrupo8queobviamentenoeslamismaqueenelhosting"
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    titulo = "Título"
    if request.method == 'POST':
        if 'usuario' in session:
            session.pop('usuario')

        mail = request.form['usuario']  # tomo el imput por name
        password = request.form['password']  # tomo el imput por name
        usuario = Usuario.autenticar(mail, password)
        if usuario is not None:
            if(not usuario.validado):
                return "cuenta no validada" 
            usuario.generarSesion()
            session['usuario'] = usuario.sesion
            usuario.save()
            if(usuario.esAdmGeneral):
                return redirect(url_for('menuadmin'))  # me lleva a la vista del estudiante
            else:
                return redirect(url_for('menuestudiante'))  # me lleva a la vista del administrador
        else:
            return redirect(url_for('error'))
    return render_template('index.html', titulo=titulo)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'usuario' in session:
        session.pop('usuario')
    return redirect(url_for('index'))


@app.route('/error', methods=['GET', 'POST'])
def error():
    titulo = "Título"
    return render_template('error.html', titulo=titulo)


@app.route('/menuadmin', methods=['GET', 'POST'])
def menuadmin():
    titulo = "Título"
    return render_template('menuadmin.html', titulo=titulo)


@app.route('/menuestudiante', methods=['GET', 'POST'])
def menuestudiante():
    titulo = "Título"
    return render_template('menuestudiante.html', titulo=titulo)


@app.route('/menuexamenes', methods=['GET', 'POST'])
def menuexamenes():
    titulo = "Título"
    return render_template('admin/menuexamenes.html', titulo=titulo)


@app.route('/crearexamen', methods=['GET', 'POST'])
def crearExamen():
    if request.method == 'GET': return crearExamenGet(request)
    else: return crearExamenPost(request)


@app.route('/crearevaluacion', methods=['GET', 'POST'])
def crearEvaluacion():
    if request.method == 'GET': return crearEvaluacionGet(request)
    else: return crearEvaluacionPost(request)



@app.route('/evaluacionespendientes', methods=['GET'])
def evaluacionesPendientes():
    return evaluacionesPendientesGet(request)



@app.route('/resolverevaluacion', methods=['GET', 'POST'])
def resolverEvaluacion():
    if request.method == 'GET': return resolverEvaluacionGet(request)
    else: return resolverEvaluacionPost(request)


"""
@app.route('/hacer_examen', methods=['GET', 'POST'])
def agregarpregunta():
    titulo = "Título"
    return render_template('estudiante/hacer_examen.html', titulo=titulo)
"""


@app.route('/altaalumno', methods=['GET', 'POST'])
def altaAlumno():
    if request.method == 'GET': return altaAlumnoGet(request)
    else: return altaAlumnoPost(request)

@app.route('/validaralumno', methods=['GET'])
def validarAlumno():
    return validarAlumnoGet(request)

@app.route('/editareliminaralumnos', methods=['GET', 'POST'])
def editarEliminarAlumnos():
    if request.method == 'GET': return editarEliminarAlumnosGet(request)
    else: return editarEliminarAlumnosPost(request)



@app.route('/altapais', methods=['GET', 'POST'])
def altaPais():
    if request.method == 'GET': return altaPaisGet(request)
    else: return altaPaisPost(request)


@app.route('/editareliminarpaises', methods=['GET', 'POST'])
def editarEliminarPaises():
    if request.method == 'GET': return editarEliminarPaisesGet(request)
    else: return editarEliminarPaisesPost(request)



@app.route('/altasede', methods=['GET', 'POST'])
def altaSede():
    if request.method == 'GET': return altaSedeGet(request)
    else: return altaSedePost(request)


@app.route('/editareliminarsedes', methods=['GET', 'POST'])
def editarEliminarSedes():
    if request.method == 'GET': return editarEliminarSedesGet(request)
    else: return editarEliminarSedesPost(request)





if __name__ == '__main__':
    app.run(port=8000, threaded=True, debug=True)
