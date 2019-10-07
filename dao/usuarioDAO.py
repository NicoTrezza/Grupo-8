from dao.conexion import Conexion
from mysql.connector import Error
from datos.usuario import Usuario


class UsuarioDAO(Conexion):
    def __init__(self):
        super(UsuarioDAO, self).__init__()

    def insertar(self, idUsuario, nombre, apellido, dni, email, esAdmGeneral, clave, validacion, validado, sesion):
        try:
            self.conectar()
            cursor = self.conexion.cursor()

            sql = 'insert into usuarios (idUsuarios, nombre, apellido, dni, email, esAdmGeneral, clave, validacion, validado, sesion) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            val = (idUsuario, nombre, apellido, dni, email, esAdmGeneral, clave, validacion, validado, sesion)

            cursor.execute(sql, val)
            self.conexion.commit()

            self.desconectar()
        except Error as e:
            print(e)

    def modificar(self, idUsuario, nombre, apellido, dni):
        try:
            self.conectar()
            cursor = self.conexion.cursor()

            sql = 'update usuarios set nombre = %s, apellido = %s, dni = %s where idUsuarios = %s'
            val = (nombre, apellido, dni, idUsuario)

            cursor.execute(sql, val)
            self.conexion.commit()

            self.desconectar()
        except Error as e:
            print(e)

    def eliminar(self, idUsuario):
        try:
            self.conectar()
            cursor = self.conexion.cursor()

            sql = 'delete from usuarios where idUsuarios = %s'
            val = (idUsuario,)

            cursor.execute(sql, val)
            self.conexion.commit()

            self.desconectar()
        except Error as e:
            print(e)

    def traer(self, idCarrera):
        try:
            self.conectar()
            cursor = self.conexion.cursor()

            sql = 'select * from usuarios where idUsuarios = %s'
            val = (idCarrera,)

            cursor.execute(sql, val)

            objeto = cursor.fetchone()

            self.desconectar()
        except Error as e:
            print(e)

        return Usuario(objeto)

    def listar(self):
        try:
            self.conectar()
            cursor = self.conexion.cursor()

            sql = 'select * from usuarios'

            cursor.execute(sql)

            lista = cursor.fetchall()

            self.desconectar()
        except Error as e:
            print(e)

        lis = []

        for objeto in lista:
            ob = Usuario(objeto)
            lis.append(ob)

        return lis