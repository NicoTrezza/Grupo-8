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
    u = Usuario()
    titulo = "Título"
    if request.method == 'POST':
        mail = request.form['usuario']
        password = request.form['password']
        print(mail)
        print(password)

        #  acá necesitaría traer a el usuario para poder saber si es admgeneral

        if u.autenticar(mail, password) is not None and not u.esAdmGeneral:
            return redirect(url_for('menuestudiante'))
        elif u.autenticar(mail, password) is not None and u.esAdmGeneral:
            return redirect(url_for('menuadmin'))
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
