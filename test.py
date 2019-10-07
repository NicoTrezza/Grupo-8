#!/usr/bin/env python
# -*- coding: utf-8 -*-

from negocio.usuarioABM import UsuarioABM


def main():
    usuarioabm = UsuarioABM()
    usuarioabm.insertar(1, "nombre", "apelido", 12345, "mail", 1, "clave", 1, 1, 2)
    #  usuarioabm.eliminar(1)
    for usuario in usuarioabm.listar():
        print(usuario)
    usuarioabm.modificar(1, "nuevo nombre", "nuevo apellido", 123459)
    print(usuarioabm.traer(1))


if __name__ == '__main__':
    main()
