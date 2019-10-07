class Usuario(object):

    def __init__(self, dao):
        self.idUsuario = int(dao[0])
        self.nombre = str(dao[1])
        self.apellido = str(dao[2])
        self.dni = int(dao[3])
        self.email = str(dao[4])
        self.esAdmGeneral = str(dao[5])
        self.clave = str(dao[6])
        self.validacion = str(dao[7])
        self.validado = str(dao[8])
        self.sesion = str(dao[9])

    def __str__(self):
        return 'id: {}, nombre: {} '.format(self.idUsuario, self.nombre)