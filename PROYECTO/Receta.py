class Receta:
    def __init__(self, id, nombre: str, objetivo: str, reactivos_utilizados: list, procedimiento: list, valores_a_medir: list):
        self.id = id
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos_utilizados = reactivos_utilizados
        self.procedimiento = procedimiento        
        self.valores_a_medir = valores_a_medir

    def show_attr(self):
        print('--- Atributos de la Receta ---')
        print(f'ID: {self.id}')
        print(f'Nombre: {self.nombre}')
        print(f'Objetivo: {self.objetivo}')
        print(f'Reactivos Usados: {self.reactivos_utilizados}')
        print(f'Procedimiento: {self.procedimiento}')
        print(f'Resultados Numéricos: {self.valores_a_medir}')

    def crear_recetas(app, recetas_json):
        recetas_objetos = []
        for receta in recetas_json:
            recetas_objetos.append(Receta(receta['id'], receta['nombre'], receta['objetivo'], receta['reactivos_utilizados'], receta['procedimiento'], receta['valores_a_medir']))
        app.recetas = recetas_objetos
        return recetas_objetos