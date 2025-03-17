class Reactivo:
    def __init__(self,id, nombre, descripcion, costo, categoria, inventario_disponible, unidad_medida, fecha_caducidad, minimo_sugerido, conversiones_posibles):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.categoria = categoria
        self.inventario_disponible = inventario_disponible
        self.unidad_medida = unidad_medida
        self.fecha_caducidad = fecha_caducidad
        self.minimo_sugerido = minimo_sugerido
        self.conversiones_posibles = conversiones_posibles

    def show_attr(self):
   
        print('--- Atributos del Reactivo ---')
        print(f'ID: {self.id}')
        print(f'Nombre: {self.nombre}')
        print(f'Descripción: {self.descripcion}')
        print(f'Costo: {self.costo}')
        print(f'Categoría: {self.categoria}')
        print(f'Inventario Disponible: {self.inventario_disponible}')
        print(f'Unidad de Medida: {self.unidad_medida}')
        print(f'Fecha de Caducidad: {self.fecha_caducidad}')
        print(f'Mínimo Sugerido: {self.minimo_sugerido}')
        print()

    @staticmethod
    def crear_reactivos(app, reactivos_json):
        reactivos_objetos=[]
        for reactivo in reactivos_json:
            reactivos_objetos.append(Reactivo(reactivo['id'],reactivo['nombre'],reactivo['descripcion'],reactivo['costo'],reactivo['categoria'],reactivo['inventario_disponible'],reactivo['unidad_medida'],reactivo['fecha_caducidad'],reactivo['minimo_sugerido'],reactivo['conversiones_posibles']))
        app.reactivos=reactivos_objetos
        return reactivos_objetos
     
    @staticmethod
    def nuevo_reactivo(reactivos):
        print('Ingrese los datos del nuevo reactivo')
        id = len(reactivos) + 1
        nombre = input('Nombre: ')
        descripcion = input('Descripción: ')
        while True:
            try:
                costo = float(input('Costo: '))
                if costo >= 0:
                    break
                else:
                    print("El costo debe ser un número positivo. Intente nuevamente.")
            except ValueError:
                print("Entrada inválida. Ingrese un número válido.")

        categoria = input('Categoría: ')

        while True:
            try:
                inventario_disponible = int(input('Inventario disponible: '))
                if inventario_disponible >= 0:
                    break
                else:
                    print("El inventario debe ser un número entero positivo. Intente nuevamente.")
            except ValueError:
                print("Entrada inválida. Ingrese un número entero válido.")
        
        unidad_medida = input('Unidad de medida: ')
        
        while True:
            fecha_caducidad = input('Fecha de caducidad (YYYY-MM-DD): ')
            try:
                year, month, day = map(int, fecha_caducidad.split('-'))
                if year >= 2025 and 1 <= month <= 12 and 1 <= day <= 31:
                    break
                else:
                    print("ERROR Fecha inválida. Asegúrese de usar el formato YYYY-MM-DD.")
            except ValueError:
                print("ERROR Formato de fecha incorrecto. Use el formato YYYY-MM-DD.")
 
        while True:
            try:
                minimo_sugerido = int(input('Mínimo sugerido: '))
                if minimo_sugerido >= 0:
                    break
                else:
                    print("El mínimo sugerido debe ser un número entero positivo. Intente nuevamente.")
            except ValueError:
                print("Entrada inválida. Ingrese un número entero válido.")

        print('Conversiones posibles: ')
        conversiones_posibles = []
        while True:
            unidad_conversion = input('Ingrese la unidad de conversión (o "salir" para terminar): ')
            if unidad_conversion.lower() == 'salir':
                break
            
            while True:
                try:
                    factor_conversion = float(input(f'Ingrese el factor de conversión para la unidad "{unidad_conversion}": '))
                    if factor_conversion > 0:
                        break
                    else:
                        print("El factor de conversión debe ser un número positivo. Intente nuevamente.")
                except ValueError:
                    print("Entrada inválida. Ingrese un número válido.")
            
            conversion = {
                'unidad': unidad_conversion,
                'factor': factor_conversion
            }
            conversiones_posibles.append(conversion)
        
        reactivo_nuevo = Reactivo(
            id=id,
            nombre=nombre,
            descripcion=descripcion,
            costo=costo,
            categoria=categoria,
            inventario_disponible=inventario_disponible,
            unidad_medida=unidad_medida,
            fecha_caducidad=fecha_caducidad,
            minimo_sugerido=minimo_sugerido,
            conversiones_posibles=conversiones_posibles
        )
        
        print(f'Reactivo "{nombre}" creado exitosamente')
        reactivos.append(reactivo_nuevo)
        print()

    def eliminar_reactivo(reactivos):

        for reactivo in reactivos:
            print(f'#{reactivo.id}, {reactivo.nombre}')

        id = input('ID del reactivo a eliminar: ')
        for reactivo in reactivos:
            if reactivo.id == int(id):
                reactivos.remove(reactivo)
                print(f"Reactivo '{reactivo.nombre}' eliminado.")
                for r in reactivos:
                    if r.id > id:
                        r.id -= 1
                return
        print(f'No se encontró un reactivo con ID #{id}')
        print()

    def editar_reactivo(reactivos, id, atributo, nuevo_valor):

        for reactivo in reactivos:
            print(f'#{reactivo.id}, {reactivo.nombre}')

        id = input('Id del reactivo a editar: ')
        atributo = input('Atributo del reactivo a editar: ')
        nuevo_valor = input('Valor nuevo del atributo \n ---> ')

        for reactivo in reactivos:
            if reactivo.id == int(id):
                if hasattr(reactivo, atributo):
                    setattr(reactivo, atributo, nuevo_valor)
                    print(f'Atributo "{atributo}" del reactivo "{id}: {reactivo.nombre}" actualizado a "{nuevo_valor}"')
                else:
                    print(f'El atributo "{atributo}" no existe en el reactivo')
                return
        print(f'No se encontró un reactivo con el nombre: "{reactivo.id}: {reactivo.nombre}"')
        print()

    def verificar_minimo(reactivo):
        if reactivo.inventario_disponible == reactivo.minimo_sugerido:
            print(f'ALERTA! El stock del reactivo "{reactivo.nombre}" se esta agotando, se sugiere agregar mas inventario')
            print()

    def cambiar_unidades(reactivos):
        for reactivo in reactivos:
            print(f'#{reactivo.id}, {reactivo.nombre}')
        try:
            reactivo_cambiar_unidades = int(input('Seleccione el ID del reactivo al cual se le cambiarán las unidades: '))
        except ValueError:
            print('ERROR -> Debe ingresar un número válido')
            return
        
        reactivo_seleccionado = None
        for reactivo in reactivos:
            if reactivo.id == reactivo_cambiar_unidades:
                reactivo_seleccionado = reactivo
                break
        if not reactivo_seleccionado:
            print('ERROR -> No se encontró un reactivo con el ID proporcionado')
            return
        print('Conversiones posibles:')
        for conversion in reactivo_seleccionado.conversiones_posibles:
            print(f'Unidad: {conversion["unidad"]}, Factor: {conversion["factor"]}')
        conversion_elegida = input('Seleccione la unidad a la que se desea cambiar: ')
        conversion_encontrada = None
        for conversion in reactivo_seleccionado.conversiones_posibles:
            if conversion['unidad'] == conversion_elegida:
                conversion_encontrada = conversion
                break
        if not conversion_encontrada:
            print('ERROR -> Unidad no válida.')
            return
        unidad_convertida = reactivo_seleccionado.inventario_disponible * conversion_encontrada['factor']
        reactivo_seleccionado.unidad_medida = conversion_elegida
        reactivo_seleccionado.inventario_disponible = unidad_convertida
        nueva_conversion = {
            'unidad': reactivo_seleccionado.unidad_medida,
            'factor': 1 / conversion_encontrada['factor']
            }
        reactivo_seleccionado.conversiones_posibles.append(nueva_conversion)
        reactivo_seleccionado.conversiones_posibles.remove(conversion_encontrada)
        print(f'Se cambió la unidad del "{reactivo_seleccionado.nombre}" exitosamente a "{conversion_elegida}".')

    def show(reactivos):
        for reactivo in reactivos:
            print(f'#{reactivo.id}, {reactivo.nombre}')