#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
	titulo = "Título"
	return render_template('index.html', titulo=titulo)


if __name__ == '__main__':
	app.run(port=8000, threaded=True, debug=True)
