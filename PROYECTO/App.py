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
                choose_1 = input('Que accion desea realizar? \n\t 1. Crear un nuevo reactivo \n\t 2. Eliminar un reactivo \n\t 3. Editar un reactivo \n\t 4. Cambiar unidades de un Reactivo \n\t 5. Mostrar Reactivos \n ---> ')
                if choose_1 == "1":
                    Reactivo.nuevo_reactivo(self.reactivos)
                    print()
                elif choose_1 == "2":
                    Reactivo.eliminar_reactivo(self.reactivos)
                    print()
                elif choose_1 == "3":
                    Reactivo.editar_reactivo(self.reactivos, None, None, None)
                    print()
                elif choose_1 == "4":
                    Reactivo.cambiar_unidades(self.reactivos)
                    print()
                elif choose_1 == "5":
                    Reactivo.show(self.reactivos)
                    print()
            elif menu == "2":
                choose_2 = input('Que accion desea realizar? \n\t 1. Crear un nuevo experimento \n\t 2. Eliminar un experimento \n\t 3. Editar un experimento \n\t 4. Mostrar expeirmentos \n ---> ')
                if choose_2 == "1":
                    Experimento.nuevo_experimento(self.experimentos, self.recetas)
                    print()
                elif choose_2 == "2":
                    Experimento.eliminar_experimento(self.experimentos, self.recetas)
                    print()
                elif choose_2 == "3":
                    Experimento.editar_experimento(self.experimentos)
                    print()
                elif choose_2 == "4":
                    Experimento.show(self.experimentos)
            elif menu == "3":
                App.realizar_experimento(self.experimentos, self.recetas, self.reactivos)
            elif menu == "4":
                choose_3 = input('Que accion desea realizar? \n\t 1. Ver investigadores que mas utilizan el laboratorio \n\t 2. Ver el experimentos más hecho y el menos hecho \n\t 3. Ver los 5 reactivos con mayor rotacion \n\t 4. Ver los 3 reactivos con mayor desperdicio \n\t 5. Ver los reactivos que más se vencen \n\t 6. Ver cuántas veces no se logró hacer un experimento por falta de reactivos \n\t 7. Ver los graficos \n ---> ')
                
                if choose_3 == "1":
                    print(IndicadoresGestion.investigadores_mas_utilizan_laboratorio(self.experimentos))
                elif choose_3 == "2":
                    print(IndicadoresGestion.experimento_mas_y_menos_hecho(self.experimentos))
                elif choose_3 == "3":
                    print(IndicadoresGestion.reactivos_mas_alta_rotacion(self.experimentos, self.recetas, self.reactivos))
                elif choose_3 == "4":
                    print(IndicadoresGestion.reactivos_mayor_desperdicio(self.experimentos))
                elif choose_3 == "5":
                    print(IndicadoresGestion.reactivos_mas_vencen(self.experimentos, self.recetas, self.reactivos))
                elif choose_3 == "6":
                    print(IndicadoresGestion.experimentos_fallidos_por_falta_reactivos(self.experimentos, self.reactivos))
                elif choose_3 == "7":
                    print(IndicadoresGestion.generar_graficos())
                else:
                    print('ERROR -> Ingrese un numero valido (1-7)')
            else:
                print('El numero ingresado es invalido, por favor ingrese un numero valido')
    
    def realizar_experimento(experimentos, recetas, reactivos):
     
        id_experimento_hacer = input(f'Ingrese el ID del experimento a realizar (1 - {len(experimentos)}): ')

        try:
            id_experimento_hacer = int(id_experimento_hacer)
        except ValueError:
            print('ERROR -> El ID debe ser un número entero.')
            return

        experimento_encontrado = None
        for experimento in experimentos:
            if experimento.id == id_experimento_hacer:
                experimento_encontrado = experimento
                experimento.veces_hecho += 1
                break
        
        if not experimento_encontrado:
            print(f'ERROR: No se encontró un experimento con ID {id_experimento_hacer}.')
            return

        receta_encontrada = None
        for receta in recetas:
            if receta.id == experimento_encontrado.receta_id:
                receta_encontrada = receta
                break

        if not receta_encontrada:
            print(f'ERROR: No se encontró una receta con ID {experimento_encontrado.receta_id}.')
            return

        for reactivo_usado in receta_encontrada.reactivos_utilizados:
            reactivo_id = reactivo_usado['reactivo_id']
            cantidad_necesaria = reactivo_usado['cantidad_necesaria']
            unidad_medida = reactivo_usado['unidad_medida']

            reactivo_encontrado = None
            for reactivo in reactivos:
                if reactivo.id == reactivo_id:
                    reactivo_encontrado = reactivo
                    fecha_reactivo = reactivo_encontrado.fecha_caducidad
                    if not App.validar_fecha_caducidad(fecha_reactivo):
                        print('ERROR: La fecha de CADUCIDAD del reactivo ya ha pasado. No se puede proseguir.')
                        return
                    break

            if not reactivo_encontrado:
                print(f'ERROR: No se encontro un reactivo con ID {reactivo_id}.')
                continue
            
            error = random.uniform(0.001, 0.225)
            cantidad_errada = reactivo_encontrado.inventario_disponible * error

            if reactivo_encontrado.unidad_medida == unidad_medida:
                reactivo_encontrado.inventario_disponible -= (cantidad_necesaria + cantidad_errada)
            else:
                conversion_encontrada = None
                for conversion in reactivo_encontrado.conversiones_posibles:
                    if conversion.unidad == unidad_medida:
                        conversion_encontrada = conversion
                        break
                if not conversion_encontrada:
                    print(f'ERROR: No se encontró una conversión para la unidad {unidad_medida}.')
                    continue
                cantidad_convertida = cantidad_necesaria / conversion_encontrada.factor
                reactivo_encontrado.inventario_disponible -= (cantidad_convertida + cantidad_errada)
        Reactivo.verificar_minimo(reactivo_encontrado)
        print()
        print(f'Experimento realizado EXITOSAMENTE: \n{receta_encontrada.nombre} -> {experimento_encontrado.resultado}')
        print()

    def validar_fecha_caducidad(fecha_caducidad):
            fecha_caducidad = datetime.strptime(fecha_caducidad, '%Y-%m-%d')
            fecha_actual = datetime.now()
            if fecha_caducidad >= fecha_actual:
                return True 
            else:
                return False
