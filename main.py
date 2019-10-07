#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask_wtf import CSRFProtect

app = Flask(__name__, template_folder="templates")
app.secret_key = "estaeslaclavesecretadelgrupo8queobviamentenoeslamismaqueenelhosting"
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    titulo = "Título"
    if request.method == 'POST':
        print(request.form['usuario'])
        print(request.form['password'])
    return render_template('index.html', titulo=titulo)


if __name__ == '__main__':
    app.run(port=8000, threaded=True, debug=True)
