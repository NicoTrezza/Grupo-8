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
import sys




app = Flask(__name__, template_folder="templates")
app.secret_key = "estaeslaclavesecretadelgrupo8queobviamentenoeslamismaqueenelhosting"
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    titulo = "Título"
    if request.method == 'POST':
        mail = request.form['usuario']  # tomo el imput por name
        password = request.form['password']  # tomo el imput por name
        print(mail)
        print(password)

        usuario = Usuario.autenticar(mail, password)

        if usuario is not None and not usuario.esAdmGeneral:
            session['usuario'] = mail
            return redirect(url_for('menuestudiante'))  # me lleva a la vista del estudiante
        elif usuario is not None and usuario.esAdmGeneral:
            session['usuario'] = mail
            return redirect(url_for('menuadmin'))  # me lleva a la vista del administrador
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


@app.route('/hacer_examen', methods=['GET', 'POST'])
def agregarpregunta():
    titulo = "Título"
    return render_template('estudiante/hacer_examen.html', titulo=titulo)


if __name__ == '__main__':
    app.run(port=8000, threaded=True, debug=True)
