from dao.DAOe import Manager

Db = Manager()

def User_get_Prestamos_y_detalles(sesion, consulta):
    detalles = []
    # PRIMERO, SE OBTIENEN LOS ID'S DE
    # LOS PRESTAMOS HECHOS POR EL USUARIO
    idPrestamo = Db.idPrestamo_From_Prestamo(sesion)
    idPrestamo = list(idPrestamo)

    # VERIFICACION
    #print('Lista:', idPrestamo)
    #print('Longitud: ', len(idPrestamo))

    len_idPrestamo = len(idPrestamo)
    #print(idPrestamo)
    if len_idPrestamo > 0:
        for i in range(len_idPrestamo):
            idPrestamo[i] = (idPrestamo[i])[0]

        # SEGUNDO, SE OBTIENEN LOS DETALLES DE
        # PRESTAMO RELACIONADOS A ESOS PRESTAMOS OBTENIDOS
        idPrestamo=tuple(idPrestamo)
        #print(idPrestamo)
        # Se buscan prestamos pendientes pero sin mora
        for i in range(len_idPrestamo):
            #print('idPrestamo en bucle:',idPrestamo[i])
            detalle = Db.idLibro_From_detallePrestamo(idPrestamo[i], consulta)
            #print('Información recogida:', detalle)
            if len(detalle) != 0:
                for j in range(len(detalle)):
                    detalles.append(detalle[j])
            #print('Tupla:', detalles)
        # Se buscan prestamos con mora

        # PRINT DETALLES -> Tupla detalles:  (((1,), (2,), (3,)), ())    
        # detalles = detalles[0]
        detalles = list(detalles)
        len_detalles = len(detalles)
        #print('Nueva lista detalles:', detalles)
        #print('Longitud lista Detalles:', len_detalles)
        
        if len_detalles > 0:
            for i in range(len_detalles):
                detalles[i] = (detalles[i])[0]

            # PARA RECUPERAR LOS DATOS DE LOS LIBROS, ES NECESARIO
            # CONVERTIR 'DETALLES' A UNA TUPLA
            #print('detalles', detalles)
            detalles = tuple(detalles)

            return detalles, tuple(idPrestamo)

        else:
            return tuple(detalles), tuple(idPrestamo)
    else:
        return tuple(detalles), tuple(idPrestamo)

def User_verLibros(tupla_detalles):
    Libros=[]
    len_detalles = len(tupla_detalles)
    #print('Longitud de la tupla enviada:',len_detalles)
    if len_detalles > 0:
        for i in range(len_detalles):
            #print('Elemento de Detalles:', tupla_detalles[i])
            libro = Db.get_Libros(tupla_detalles[i])
            #print('Info de libro:', libro)
            if len(libro) != 0:
                Libros.append(libro[0])
        Libros = tuple(Libros)
        return Libros
    else:
        return tuple(Libros)

def User_registrar_devolucion(sesion, idLibro, fecha):
    detalles = []
    # PRIMERO, SE OBTIENEN LOS ID'S DE
    # LOS PRESTAMOS HECHOS POR EL USUARIO
    idPrestamo = Db.idPrestamo_From_Prestamo(sesion)
    idPrestamo = list(idPrestamo)

    # VERIFICACION
    #print('Lista:', idPrestamo)
    #print('Longitud: ', len(idPrestamo))

    len_idPrestamo = len(idPrestamo)
    print(idPrestamo)
    for i in range(len_idPrestamo):
        idPrestamo[i] = (idPrestamo[i])[0]

    # SEGUNDO, SE OBTIENEN LOS DETALLES DE
    # PRESTAMO RELACIONADOS A ESOS PRESTAMOS OBTENIDOS
    # idPrestamo=tuple(idPrestamo)
    ids_detalle=[]
    for i in range(len_idPrestamo):
        detalle = Db.giveBack_Book(idLibro, idPrestamo[i])
        if len(detalle) != 0:
            ids_detalle.append(detalle[0])

    # Registro de la devolucion
    # if Db.registrar_devolucion(fecha, ids_detalle[0]):
        
    # else:
    #     return 'ERROR. No se pudo hacer la devolución.'


def existenPrestamosAsociados(id_Libro):
    ids_detallePrestamo = Db.iddetallePrestamo_from_detallePrestamo(id_Libro)
    # print('IDs de detallePrestamo:', ids_detallePrestamo)
    # ID's de detallePrestamo: ((12,), (15,))
    if len(ids_detallePrestamo) > 0:
        ids_detallePrestamo = list(ids_detallePrestamo)
        for i in range(len(ids_detallePrestamo)):
            ids_detallePrestamo[i] = (ids_detallePrestamo[i])[0]
            # ((12,), (15,))
            #  (12,) = 12
        print('IDs de detallePrestamo:', ids_detallePrestamo)

    return ids_detallePrestamo

def eliminar_Prestamos_y_detalles(tupla_detalles, tupla_prestamos):
    len_detalles = len(tupla_detalles)
    if len_detalles > 0:
        for i in range(len_detalles):
            Db.delete_detallePrestamo(tupla_detalles[i], 0)
    
    len_prestamos = len(tupla_prestamos)
    if len_prestamos > 0:
        for i in range(len_prestamos):
            Db.delete_Prestamo(tupla_prestamos[i])