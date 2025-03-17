import requests
import random
from datetime import datetime
from Experimento import Experimento
from Reactivo import Reactivo
from Receta import Receta
from Indicadores_gestion import IndicadoresGestion

class App:
    def obtener_json_desde_api(self, url, params=None):
        try:
            response = requests.get(url, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a la API: {e}")
            return None
        
    def start(self):
        self.reactivos_json = self.obtener_json_desde_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/reactivos.json")
        self.recetas_json = self.obtener_json_desde_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/recetas.json")
        self.experimentos_json = self.obtener_json_desde_api("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/experimentos.json")

        self.reactivos = Reactivo.crear_reactivos(self, self.reactivos_json)
        self.recetas = Receta.crear_recetas(self, self.recetas_json)
        self.experimentos = Experimento.crear_experimentos(self, self.experimentos_json)

    def menu(self):
        self.start()
        while True:
            menu = input('Bienvenido al Laboratorio de Quimica de la Universidad Metropolitana.\n Seleccione: \n\t 1. Para gestionar los reactivos \n\t 2. Para gestionar los experimentos \n\t 3. Para realizar un experimento \n\t 4. Para acceder a las estadisticas \n ---> ')
            if menu == "1":
                choose_1 = input('Que accion desea realizar? \n\t 1. Crear un nuevo reactivo \n\t 2. Eliminar un reactivo \n\t 3. Editar un reactivo \n\t 4. Mostrar Reactivos \n ---> ')
                if choose_1 == "1":
                    Reactivo.nuevo_reactivo(self)
                elif choose_1 == "2":
                    Reactivo.eliminar_reactivo(self, None)
                elif choose_1 == "3":
                    Reactivo.editar_reactivo(self, None)
                elif choose_1 == "4":
                    for reactivo in self.reactivos:
                        reactivo.show_attr()
            elif menu == "2":
                choose_2 = input('Que accion desea realizar? \n\t 1. Crear un nuevo experimento \n\t 2. Eliminar un experimento \n\t 3. Editar un experimento \n ---> ')
                if choose_2 == "1":
                    Experimento.nuevo_experimento(self)
                elif choose_2 == "2":
                    id = input('Ingrese el ID del ezperimento a eliminar: ')
                    Experimento.eliminar_experimento(self, id)
                elif choose_2 == "3":
                    Experimento.editar_experimento(self, None)
                elif choose_2 == "4":
                    for experimento in self.experimentos:
                        experimento.show_attr()
            elif menu == "3":
                self.realizar_experimento()
            elif menu == "4":
                choose_3 = input('Que accion desea realizar? \n\t 1. Ver investigadores que mas utilizan el laboratorio \n\t 2. Ver el experimentos más hecho y el menos hecho \n\t 3. Ver los 5 reactivos con mayor rotacion \n\t 4. Ver los 3 reactivos con mayor desperdicio \n\t 5. Ver los reactivos que más se vencen \n\t 6. Ver cuántas veces no se logró hacer un experimento por falta de reactivos \n\t 7. Ver los graficos \n ---> ')
                indicadores = IndicadoresGestion(self.experimentos, self.reactivos)
                if choose_3 == "1":
                    print(indicadores.investigadores_mas_utilizan_laboratorio())
                elif choose_3 == "2":
                    print(indicadores.experimento_mas_y_menos_hecho())
                elif choose_3 == "3":
                    print(indicadores.reactivos_mas_alta_rotacion())
                elif choose_3 == "4":
                    print(indicadores.reactivos_mayor_desperdicio())
                elif choose_3 == "5":
                    print(indicadores.reactivos_mas_vencen())
                elif choose_3 == "6":
                    print(indicadores.experimentos_fallidos_por_falta_reactivos())
                elif choose_3 == "7":
                    indicadores.generar_graficos()
                else:
                    print('ERROR -> Ingrese un numero valido (1-7)')
            else:
                print('El numero ingresado es invalido, por favor ingrese un numero valido')
    
    def realizar_experimento(self):
        id_experimento_hacer = input('Ingrese el ID del experimento a realizar: ')

        try:
            id_experimento_hacer = int(id_experimento_hacer)
        except ValueError:
            print('ERROR -> El ID debe ser un número entero.')
            return

        experimento_encontrado = None
        for experimento in self.experimentos_json:
            if experimento['id'] == id_experimento_hacer:
                experimento_encontrado = experimento
                break
        
        if not experimento_encontrado:
            print(f'ERROR: No se encontró un experimento con ID {id_experimento_hacer}.')
            return

        experimento_encontrado['veces_hecho'] += 1

        receta_encontrada = None
        for receta in self.recetas_json:
            if receta['id'] == experimento_encontrado['receta_id']:
                receta_encontrada = receta
                break

        if not receta_encontrada:
            print(f'ERROR: No se encontró una receta con ID {experimento_encontrado["receta_id"]}.')
            return

        for reactivo_usado in receta_encontrada['reactivos_utilizados']:
            reactivo_id = reactivo_usado['reactivo_id']
            cantidad_necesaria = reactivo_usado['cantidad_necesaria']
            unidad_medida = reactivo_usado['unidad_medida']
            reactivo_encontrado = None
            for reactivo in self.reactivos_json:
                if reactivo['id'] == reactivo_id:
                    reactivo_encontrado = reactivo
                    if not self.validar_fecha_caducidad(reactivo_encontrado['fecha']):
                        print('ERROR: La fecha de caducidad del reactivo ya ha pasado. No se puede proseguir.')
                        return
                    break

            if not reactivo_encontrado:
                print(f'ERROR: No se encontró un reactivo con ID {reactivo_id}.')
                continue
            
            error = random.uniform(0.001, 0.225)
            cantidad_errada = cantidad_necesaria * error

            if reactivo_encontrado['unidad_medida'] == unidad_medida:
                reactivo_encontrado['inventario_disponible'] -= (cantidad_necesaria + cantidad_errada)
            else:
                conversion_encontrada = None
                for conversion in reactivo_encontrado['conversiones_posibles']:
                    if conversion['unidad'] == unidad_medida:
                        conversion_encontrada = conversion
                        break
                if not conversion_encontrada:
                    print(f'ERROR: No se encontró una conversión para la unidad {unidad_medida}.')
                    continue
                cantidad_convertida = cantidad_necesaria / conversion_encontrada['factor']
                reactivo_encontrado['inventario_disponible'] -= (cantidad_convertida + cantidad_errada)

        print('Experimento realizado exitosamente')

    def validar_fecha_caducidad(self, fecha_caducidad):
            fecha_caducidad = datetime.strptime(fecha_caducidad, '%Y-%m-%d')
            fecha_actual = datetime.now()
            if fecha_caducidad >= fecha_actual:
                return True 
            else:
                return False
