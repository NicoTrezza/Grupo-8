#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask_wtf import CSRFProtect
from modelo.models import *

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
            return redirect(url_for('menuestudiante'))  # me lleva a la vista del estudiante
        elif usuario is not None and usuario.esAdmGeneral:
            return redirect(url_for('menuadmin'))  # me lleva a la vista del administrador
        else:
            return redirect(url_for('error'))
    return render_template('index.html', titulo=titulo)


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


if __name__ == '__main__':
    app.run(port=8000, threaded=True, debug=True)
