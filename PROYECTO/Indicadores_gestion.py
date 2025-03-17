#import matplotlib.pyplot as plt
from datetime import datetime

class IndicadoresGestion:
    
    def investigadores_mas_utilizan_laboratorio(experimentos):
        investigadores = {}
        for experimento in experimentos:
            for investigador in experimento.personas_responsables:
                if investigador in investigadores:
                    investigadores[investigador] += (1 + experimento.veces_hecho)
                else:
                    investigadores[investigador] = (1 + experimento.veces_hecho)
        return sorted(investigadores.items(), key=lambda x: x[1], reverse=True)[:5]

    def experimento_mas_y_menos_hecho(experimentos):
        conteo_experimentos = {}
        for experimento in experimentos:
            id = experimento.id
            if id in conteo_experimentos:
                conteo_experimentos[id] += (1 + experimento.veces_hecho)
            else:
                conteo_experimentos[id] = (1 + experimento.veces_hecho)
        mas_hecho = max(conteo_experimentos.items(), key=lambda x: x[1])
        menos_hecho = min(conteo_experimentos.items(), key=lambda x: x[1])
        return mas_hecho, menos_hecho

    def reactivos_mas_alta_rotacion(experimentos, recetas, reactivos):
        rotacion = {}
        for experimento in experimentos:
            for receta in recetas:
                if receta.id == experimento.receta_id:
                    for reactivo_usado in receta.reactivos_utilizados:
                        for reactivo in reactivos:
                            if reactivo.id == reactivo_usado['reactivo_id']:
                                nombre = reactivo.nombre
                                cantidad = reactivo_usado['cantidad_necesaria']
                                if nombre in rotacion:
                                    rotacion[nombre] += (cantidad+experimento.veces_hecho)
                                else:
                                    rotacion[nombre] = (cantidad+experimento.veces_hecho)
        return sorted(rotacion.items(), key=lambda x: x[1], reverse=True)[:5]

#    def reactivos_mayor_desperdicio(experimentos, recetas, reactivos):
        desperdicio = {}
        for experimento in experimentos:
            for receta in recetas:
                if receta.id == experimento.receta_id:
                    pass
            for reactivo in experimento.receta_id.reactivos_utilizados:
                nombre = reactivo.nombre
                cantidad = reactivo.cantidad * (experimento['error_simulado'] / 100)
                if nombre in desperdicio:
                    desperdicio[nombre] += cantidad
                else:
                    desperdicio[nombre] = cantidad
        return sorted(desperdicio.items(), key=lambda x: x[1], reverse=True)[:3]

    def reactivos_mas_vencen(experimentos, recetas, reactivos):
        vencidos = {}
        fecha_actual = datetime.now()
        
        for experimento in experimentos:
            for receta in recetas:
                if receta.id == experimento.receta_id:
                    for reactivo_usado in receta.reactivos_utilizados:
                        for reactivo in reactivos:
                            if reactivo.id == reactivo_usado['id']:
                                fecha_caducidad = datetime.strptime(reactivo.recha_caducidad, '%Y-%m-%d')
                            if fecha_caducidad >= fecha_actual:
                                nombre = reactivo.nombre
                                if nombre in vencidos:
                                    vencidos[nombre] += 1
                                else:
                                    vencidos[nombre] = 1
        return sorted(vencidos.items(), key=lambda x: x[1], reverse=True)

    def experimentos_fallidos_por_falta_reactivos(experimentos, recetas, reactivos):
        fallidos = 0
        for experimento in experimentos:
            for receta in recetas:
                if experimento.receta_id == receta.id:
                    for reactivo_usado in receta.reactivos_utilizados:
                        for reactivo in reactivos:
                            if reactivo.id == reactivo_usado['reactivo_id']:
                                if reactivo_usado['cantidad_necesaria'] > reactivo.inventario_disponible:
                                    fallidos += 1
        return fallidos

    #def generar_graficos(self):
        investigadores = self.investigadores_mas_utilizan_laboratorio()
        nombres, frecuencias = zip(*investigadores)
        plt.bar(nombres, frecuencias)
        plt.title('Investigadores que más utilizan el laboratorio')
        plt.xlabel('Investigadores')
        plt.ylabel('Número de experimentos')
        plt.show()

        rotacion = self.reactivos_mas_alta_rotacion()
        nombres, cantidades = zip(*rotacion)
        plt.bar(nombres, cantidades)
        plt.title('Reactivos con más alta rotación')
        plt.xlabel('Reactivos')
        plt.ylabel('Cantidad utilizada')
        plt.show()

        desperdicio = self.reactivos_mayor_desperdicio()
        nombres, cantidades = zip(*desperdicio)
        plt.bar(nombres, cantidades)
        plt.title('Reactivos con mayor desperdicio')
        plt.xlabel('Reactivos')
        plt.ylabel('Cantidad desperdiciada')
        plt.show()