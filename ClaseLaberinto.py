import random
from ClaseGrafoDirigido import Grafo

class Laberinto:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.grafo = Grafo()
        self.crear_laberinto()

    def crear_laberinto(self):
        total_celdas = self.filas * self.columnas
        for i in range(total_celdas):
            self.grafo.add_vertice()      #se crean los veritces pero no el como estan conectadas entre si
            

        self.generar_prim()  # Generar el laberinto usando el algoritmo de Prim
        # Conectar el nodo inicial a todos los demás nodos

        # Añadir conexiones adicionales aleatoriamente
        for i in range(self.filas):
            for j in range(self.columnas):
                celda_actual = i * self.columnas + j
                
                for di, dj in [(0, 1), (1, 0)]:  # Solo derecha y abajo
                    if (0 <= i + di < self.filas) and (0 <= j + dj < self.columnas):
                        celda_destino = (i + di) * self.columnas + (j + dj)
                        if random.random() < 0.3:  # 30% de probabilidad de añadir conexión
                            # peso = random.randint(1, 10)
                            peso = 1
                            self.grafo.add_arista(celda_actual, peso, celda_destino)
        self.verificar_conexiones()


    def verificar_conexiones(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                celda_actual = i * self.columnas + j
                if not self.grafo.tiene_conexiones_salientes(celda_actual) and not self.grafo.tiene_conexiones_entrantes(celda_actual):
                    raise ValueError(f"La celda {celda_actual} no tiene ninguna conexión entrante ni saliente.")                    

    def generar_prim(self):
        # Lista de celdas visitadas
        visitadas = set()
        # Cola de prioridad de aristas (peso, celda_origen, celda_destino)
        aristas = []
        # Celda inicial
        celda_inicial = 0
        visitadas.add(celda_inicial)

        # Añadir aristas de la celda inicial     # celdas a un movimiento mas cercana
        self.agregar_aristas(celda_inicial, aristas, visitadas)

        while aristas:
            #peso, u, v = min(aristas, key=lambda x: x[0])   # busca el minimo de peso de la lista de aristas del vertice( (u(0), costo(u(0)_v(0)), v(0); ...)
            # Encontrar el peso mínimo
            min_peso = min(aristas, key=lambda x: x[0])[0]
            # Filtrar todas las aristas con el peso mínimo
            min_aristas = [arista for arista in aristas if arista[0] == min_peso]
            # Elegir una arista aleatoria entre las de peso mínimo
            peso, u, v = random.choice(min_aristas)
            aristas.remove((peso, u, v))

            if v not in visitadas:
                visitadas.add(v)
                self.grafo.add_arista(u, peso, v)
                self.agregar_aristas(v, aristas, visitadas)

    def agregar_aristas(self, celda, aristas, visitadas):
        fila, columna = divmod(celda, self.columnas)    #divmod devuelve una tupla, descompone celda, en fila y columna
        direcciones = self.obtener_direcciones_validas(fila, columna)

        for di, dj in direcciones:   #di  y  dj , toman los valores de la la lista de tuplas (direcciones), se interara cuantas tuplas tenga
            nueva_fila = fila + di
            nueva_columna = columna + dj
            if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas:
                nueva_celda = nueva_fila * self.columnas + nueva_columna
                if nueva_celda not in visitadas:
                    # peso = random.randint(1, 10)
                    peso = 1
                    aristas.append((peso, celda, nueva_celda))

    def obtener_direcciones_validas(self, i, j):
        direcciones = []
        if j < self.columnas - 1:
            direcciones.append((0, 1))  # Derecha
        if i < self.filas - 1:
            direcciones.append((1, 0))  # Abajo
        if j > 0:
            direcciones.append((0, -1))  # Izquierda
        if i > 0:
            direcciones.append((-1, 0))  # Arriba
        return direcciones


    def obtener_matriz_laberinto_1_0(self):
        matriz = [[1 for _ in range(self.columnas * 2 + 1)] for _ in range(self.filas * 2 + 1)]  #se inicializa las paredes con 1
        
        for i in range(self.filas):   #i  y j comienza desde 0
            for j in range(self.columnas):
                celda_actual = i * self.columnas + j
                
                matriz[i*2+1][j*2+1] = 0
                
                if j < self.columnas - 1:
                    celda_derecha = i * self.columnas + (j + 1)
                    if self.grafo.costo(celda_actual, celda_derecha) > 0 or self.grafo.costo(celda_derecha, celda_actual) > 0:
                        matriz[i*2+1][j*2+2] = 0
                
                if i < self.filas - 1:
                    celda_abajo = (i + 1) * self.columnas + j
                    if self.grafo.costo(celda_actual, celda_abajo) > 0 or self.grafo.costo(celda_abajo, celda_actual) > 0:
                        matriz[i*2+2][j*2+1] = 0
        
        return matriz
    
    def obtener_matriz_laberinto(self):
        matrizNodo = [[-1 for _ in range(self.columnas * 2 + 1)] for _ in range(self.filas * 2 + 1)]
        
        for i in range(self.filas):
            for j in range(self.columnas):
                celda_actual = i * self.columnas + j
                matrizNodo[i*2+1][j*2+1] = celda_actual
                
                if j < self.columnas - 1:
                    celda_derecha = i * self.columnas + (j + 1)
                    if self.grafo.costo(celda_actual, celda_derecha) > 0 or self.grafo.costo(celda_derecha, celda_actual) > 0:
                        matrizNodo[i*2+1][j*2+2] = celda_derecha
                
                if i < self.filas - 1:
                    celda_abajo = (i + 1) * self.columnas + j
                    if self.grafo.costo(celda_actual, celda_abajo) > 0 or self.grafo.costo(celda_abajo, celda_actual) > 0:
                        matrizNodo[i*2+2][j*2+1] = celda_abajo
        
        return matrizNodo

    def obtener_solucion_completa(self):
        inicio = 0
        fin = self.filas * self.columnas - 1
        camino, pasos = self.grafo.camino_mas_corto_completo(inicio, fin)
        costo = self.calcular_costo(camino)
        return {"camino": camino, "costo": costo, "pasos": pasos}
    
    def calcular_costo(self, camino):
        costo = 0
        for i in range(len(camino) - 1):
            costo += self.grafo.costo(camino[i], camino[i+1])
        return costo
    