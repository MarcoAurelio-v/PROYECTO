class Experimento():
    def __init__(self, id, receta_id, personas_responsables: str, fecha: str, costo_asociado: float, resultado: str, veces_hecho: int):
        self.id = id
        self.receta_id = receta_id
        self.personas_responsables = personas_responsables
        self.fecha = fecha
        self.costo_asociado = costo_asociado
        self.resultado = resultado
        self.veces_hecho = 0
    
    def show_attr(self):
        print('--- Atributos del Experimento ---')
        print(f'ID: {self.id}')
        print(f'Receta ID: {self.receta_id}')
        print(f'Personas Responsables: {self.personas_responsables}')
        print(f'Fecha: {self.fecha}')
        print(f'Costo Asociado: {self.costo_asociado}')
        print(f'Resultado: {self.resultado}')        
        print(f'Veces hecho: {self.veces_hecho}')

    @staticmethod
    def crear_experimentos(app,experimentos_json):
        experimentos_objetos = []
        for experimento in experimentos_json:
            experimentos_objetos.append(Experimento(experimento['id'], experimento['receta_id'], experimento['personas_responsables'], experimento['fecha'], experimento['costo_asociado'], experimento['resultado'], veces_hecho=0))
        app.experimentos = experimentos_objetos
        return experimentos_objetos

    @staticmethod
    def nuevo_experimento(app):
        print('Ingrese los datos del nuevo experimento')
        id = len(app.experimentos) + 1
        
        while True:
            try:
                receta_id = int(input('ID de la receta: '))
                if receta_id >= 0:
                    break
                elif receta_id != 0 and receta_id not in [receta.id for receta in app.recetas]:
                    print('ERROR: El ID de la receta no existe.')
                    return
            except ValueError:
                print('Entrada inválida. Ingrese un número válido.')
        
        personas_responsables = input('Personas responsables (separadas por comas): ').split(',')
        
        while True:
            fecha = input('Fecha del experimento (YYYY-MM-DD): ')
            try:
                year, month, day = map(int, fecha.split('-'))
                if 1 <= day <= 31 and 1 <= month <= 12 and year >= 2025:
                    break
                else:
                    print('ERROR Fecha inválida. Asegúrese de usar el formato DD-MM-YYYY.')
            except ValueError:
                print('ERROR Formato de fecha incorrecto. Use el formato DD-MM-YYYY.')
        
        while True:
            try:
                costo_asociado = float(input('Costo asociado: '))
                if costo_asociado >= 0:
                    break
                else:
                    print('El costo debe ser un número positivo. Intente nuevamente.')
            except ValueError:
                print('Entrada inválida. Ingrese un número válido.')
        
        resultado = input('Resultado del experimento: ')
        
        nuevo_experimento = Experimento(
            id=id,
            receta_id=receta_id,
            personas_responsables=personas_responsables,
            fecha=fecha,
            costo_asociado=costo_asociado,
            resultado=resultado,
            veces_hecho=0
        )
        
        print(f'Experimento creado exitosamente')
        app.experimentos.append(nuevo_experimento)
    
    def eliminar_experimento(self, id):
        for experimento in self.experimentos:
            if experimento.id == id:
                self.experimentos.remove(experimento)
                print(f'Experimento "{id}" eliminado')
                return
        print(f'No se encontró un experimento con el id "{id}"')

    def editar_experimento(self, id, atributo, nuevo_valor):
        for experimento in self.experimentos:
            if experimento.id == id:
                if hasattr(experimento, atributo):
                    setattr(experimento, atributo, nuevo_valor)
                    print(f'Atributo "{atributo}" del experimento "{id}" actualizado a "{nuevo_valor}"')
                else:
                    print(f'El atributo "{atributo}" no existe en el experimento "{id}"')
                return
        print(f'No se encontró un experimento con el id "{id}"')

    def exp_mas_hecho(self):
        info = {}
        for experimento in self.experimentos:
            if experimento.receta in info:
                info[experimento.receta] += 1
            else:
                info[experimento.receta] = 1
            print(info)