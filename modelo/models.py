# -*- coding: utf-8 -*-

import peewee
import datetime
import os


db = peewee.SqliteDatabase(os.path.dirname(os.path.abspath(__file__))+'\\test.db')


class BaseModel(peewee.Model):
	class Meta:
		database = db


class Usuario(BaseModel):
	nombre = peewee.CharField()
	apellido = peewee.CharField()
	dni = peewee.CharField()
	email = peewee.CharField(unique=True)
	clave = peewee.CharField()
	esAdmGeneral = peewee.BooleanField(default=False)
	validacion = peewee.CharField()
	validado = peewee.BooleanField(default=False)
	sesion = peewee.CharField()


	@staticmethod
	def autenticar(email,clave):
		try:
			return Usuario.get(email = email, clave = clave )
		except  Usuario.DoesNotExist:
			return None


	@staticmethod
	def traerPorSesion(sesion):
		try:
			return Usuario.get(sesion = sesion)
		except  Usuario.DoesNotExist:
			return None


class Pais(BaseModel):
	administrador = peewee.ForeignKeyField(Usuario, backref='PaisesQueAdministra')
	nombre = peewee.CharField()


class Sede(BaseModel):
	administrador = peewee.ForeignKeyField(Usuario, backref='SedesQueAdministra')
	pais = peewee.ForeignKeyField(Pais, backref='sedes')
	nombre = peewee.CharField()

class Curso(BaseModel):
	sede = peewee.ForeignKeyField(Sede, backref='cursos')
	nombre = peewee.CharField()


ProfesorThroughDeferred = peewee.DeferredThroughModel()
AlumnoThroughDeferred = peewee.DeferredThroughModel()

class Cursada(BaseModel):
	curso = peewee.ForeignKeyField(Curso, backref='cursadas')
	profesores = peewee.ManyToManyField(Usuario,through_model= ProfesorThroughDeferred, backref='cursadasEnLasQueEsProfesor')
	alumnos = peewee.ManyToManyField(Usuario,through_model= AlumnoThroughDeferred, backref='cursadasEnLasQueEsAlumno')
	inicio = peewee.DateTimeField()


class Profesor(BaseModel):
	usuario = peewee.ForeignKeyField(Usuario)
	cursada = peewee.ForeignKeyField(Cursada)


class Alumno(BaseModel):
	usuario = peewee.ForeignKeyField(Usuario)
	cursada = peewee.ForeignKeyField(Cursada)


ProfesorThroughDeferred.set_model(Profesor)
AlumnoThroughDeferred.set_model(Alumno)


class Examen(BaseModel):
	curso = peewee.ForeignKeyField(Curso, backref='examenes')
	titulo = peewee.CharField()
	notaMinima = peewee.DecimalField()


class Pregunta(BaseModel):
	examen = peewee.ForeignKeyField(Examen, backref='preguntas')
	texto = peewee.CharField()
	esChoice = peewee.BooleanField()
	esVerdadera = peewee.BooleanField()


class Respuesta(BaseModel):
	pregunta = peewee.ForeignKeyField(Pregunta, backref='respuestas')
	texto = peewee.CharField()
	esCorrecta = peewee.BooleanField()


class Evaluacion(BaseModel):
	examen = peewee.ForeignKeyField(Examen, backref='evaluaciones',null = False) #una evaluacion con examen null es para cargar notas de practicos
	preguntas = peewee.ManyToManyField(Pregunta, backref='evaluaciones')
	cursada = peewee.ForeignKeyField(Cursada, backref='evaluaciones')
	fecha = peewee.DateTimeField()


class RespuestaDelAlumno(BaseModel):
	alumno = peewee.ForeignKeyField(Usuario, backref='respuestas')
	evaluacion = peewee.ForeignKeyField(Evaluacion, backref='respuestasElegidas')
	pregunta = peewee.ForeignKeyField(Pregunta) #ni idea que nombre poner en backref si lo necesitamos pienso uno
	respuesta = peewee.ForeignKeyField(Respuesta, null = False) #ni idea que nombre poner en backref si lo necesitamos pienso uno
	respondioVerdadera = peewee.BooleanField()

class Nota(BaseModel):
	evaluacion = peewee.ForeignKeyField(Evaluacion, backref='notas')
	alumno = peewee.ForeignKeyField(Usuario, backref='notas')
	nota = peewee.DecimalField()


def crearTablas():

	cursadaProfesores = Cursada.profesores.get_through_model()
	cursadaAlumnos = Cursada.alumnos.get_through_model()
	evaluacionPreguntas = Evaluacion.preguntas.get_through_model()

	
	Usuario.drop_table()
	Pais.drop_table()
	Sede.drop_table()
	Curso.drop_table()
	Cursada.drop_table()
	Examen.drop_table()
	Pregunta.drop_table()
	Respuesta.drop_table()
	Evaluacion.drop_table()
	RespuestaDelAlumno.drop_table()
	Nota.drop_table()

	cursadaProfesores.drop_table()
	cursadaAlumnos.drop_table()
	evaluacionPreguntas.drop_table()



	Usuario.create_table()
	Pais.create_table()
	Sede.create_table()
	Curso.create_table()
	Cursada.create_table()
	Examen.create_table()
	Pregunta.create_table()
	Respuesta.create_table()
	Evaluacion.create_table()
	RespuestaDelAlumno.create_table()
	Nota.create_table()

	cursadaProfesores.create_table()
	cursadaAlumnos.create_table()
	evaluacionPreguntas.create_table()



def cargarDatosDePrueba():
	admin = Usuario.create(nombre = "Cosme", apellido = "Fulanito", dni = "123", email="cosme@fulanito.com",clave="123",validacion="",sesion="" , esAdmGeneral = True)
	admin.save()
	profesor = Usuario.create(nombre = "profesor", apellido = "", dni = "", email="profesor@prueba.com",clave="123",validacion="",sesion="")
	profesor.save()
	alumno = Usuario.create(nombre = "alumno", apellido = "", dni = "", email="alumno@prueba.com",clave="123",validacion="",sesion="")
	alumno.save()

	pais = Pais.create(nombre = "Argentina",administrador = admin)
	pais.save()

	sede = Sede.create(nombre = "Sede Argentina", pais = pais,administrador = admin)
	sede.save()

	curso = Curso.create(nombre = "curso 1", sede = sede)
	curso.save()

	curso = Curso.create(nombre = "curso 2", sede = sede)
	curso.save()

	curso = Curso.create(nombre = "fisica", sede = sede)
	curso.save()

	cursada = Cursada.create(curso = curso, inicio = datetime.date(2019, 10, 20))
	cursada.profesores.add(profesor)
	cursada.alumnos.add(alumno)
	cursada.save()

	examen = Examen.create(curso = curso, titulo = "examen 1", notaMinima = 4)
	examen.save()


	pregunta = Pregunta.create(examen = examen, texto = "¿A nivel del mar el agua hierve a?", esChoice = True , esVerdadera=False)
	pregunta.save()


	respuesta = Respuesta.create(pregunta = pregunta, texto = "100 grados centigrados", esCorrecta = True)
	respuesta.save()

	respuesta = Respuesta.create(pregunta = pregunta, texto = "80 grados centigrados", esCorrecta = False)
	respuesta.save()

	respuesta = Respuesta.create(pregunta = pregunta, texto = "120 grados centigrados", esCorrecta = False)
	respuesta.save()

	evaluacion = Evaluacion.create(examen = examen, cursada = cursada, fecha = datetime.date(2019, 10, 20))
	evaluacion.preguntas.add(pregunta)
	evaluacion.save()


	respuestaDelAlumno = RespuestaDelAlumno.create(alumno = alumno, evaluacion = evaluacion,pregunta = pregunta , respuesta = respuesta, respondioVerdadera = False)
	respuestaDelAlumno.save()

	nota = Nota.create(alumno = alumno, evaluacion = evaluacion, nota = 9)
	nota.save()

