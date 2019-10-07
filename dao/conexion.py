import mysql.connector
from mysql.connector import Error


class Conexion(object):

	def __init__(self):
		self.conexion = None

	def conectar(self):
		try:
			self.conexion = mysql.connector.connect(host='localhost', database='mydb', user='root',
													password='root')
		except Error as e:
			print(e)

	def desconectar(self):
		self.conexion.close()