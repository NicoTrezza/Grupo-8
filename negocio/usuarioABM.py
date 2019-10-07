from dao.usuarioDAO import UsuarioDAO


class UsuarioABM (object):
    def __init__(self):
        self.dao = UsuarioDAO()

    def insertar (self, idUsuario, nombre, apellido, dni, email, esAdmGeneral, clave, validacion, validado, sesion):
        self.dao.insertar(idUsuario, nombre, apellido, dni, email, esAdmGeneral, clave, validacion, validado, sesion)

    def modificar (self, idUsuario, nombre, apellido, dni):
        self.dao.modificar(idUsuario, nombre, apellido, dni)

    def eliminar(self, idUsuario):
        self.dao.eliminar(idUsuario)

    def traer(self, idUsuario):
        return self.dao.traer(idUsuario)

    def listar(self):
        return self.dao.listar()

