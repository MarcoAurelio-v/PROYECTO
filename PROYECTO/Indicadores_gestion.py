#import matplotlib.pyplot as plt

class IndicadoresGestion:
    def __init__(self, experimentos, reactivos):
        self.experimentos = experimentos
        self.reactivos = reactivos

    def investigadores_mas_utilizan_laboratorio(self):
        investigadores = {}
        for experimento in self.experimentos:
            for investigador in experimento['personas_responsables']:
                if investigador in investigadores:
                    investigadores[investigador] += 1
                else:
                    investigadores[investigador] = 1
        return sorted(investigadores.items(), key=lambda x: x[1], reverse=True)[:5]

    def experimento_mas_y_menos_hecho(self):
        conteo_experimentos = {}
        for experimento in self.experimentos:
            nombre = experimento['receta']['nombre']
            if nombre in conteo_experimentos:
                conteo_experimentos[nombre] += 1
            else:
                conteo_experimentos[nombre] = 1
        mas_hecho = max(conteo_experimentos.items(), key=lambda x: x[1])
        menos_hecho = min(conteo_experimentos.items(), key=lambda x: x[1])
        return mas_hecho, menos_hecho

    def reactivos_mas_alta_rotacion(self):
        rotacion = {}
        for experimento in self.experimentos:
            for reactivo in experimento['receta']['reactivos_utilizados']:
                nombre = reactivo['nombre']
                cantidad = reactivo['cantidad']
                if nombre in rotacion:
                    rotacion[nombre] += cantidad
                else:
                    rotacion[nombre] = cantidad
        return sorted(rotacion.items(), key=lambda x: x[1], reverse=True)[:5]

    def reactivos_mayor_desperdicio(self):
        desperdicio = {}
        for experimento in self.experimentos:
            for reactivo in experimento['receta']['reactivos_utilizados']:
                nombre = reactivo['nombre']
                cantidad = reactivo['cantidad'] * (experimento['error_simulado'] / 100)
                if nombre in desperdicio:
                    desperdicio[nombre] += cantidad
                else:
                    desperdicio[nombre] = cantidad
        return sorted(desperdicio.items(), key=lambda x: x[1], reverse=True)[:3]

    def reactivos_mas_vencen(self):
        vencidos = {}
        for reactivo in self.reactivos():
            if reactivo['fecha_caducidad']:
                nombre = reactivo['nombre']
                if nombre in vencidos:
                    vencidos[nombre] += 1
                else:
                    vencidos[nombre] = 1
        return sorted(vencidos.items(), key=lambda x: x[1], reverse=True)

    def experimentos_fallidos_por_falta_reactivos(self):
        fallidos = 0
        for experimento in self.experimentos:
            for reactivo in experimento['receta']['reactivos_utilizados']:
                if reactivo['cantidad'] > self.reactivos[reactivo['nombre']]['inventario_disponible']:
                    fallidos += 1
                    break
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