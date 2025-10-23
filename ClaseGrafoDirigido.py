from ListaSimple import Lista
from collections import deque

class Grafo:
    MAXVERTEX = 100   #segun la teoria deber ser de 49 nodos maximo para ser optimo
    def __init__(self):
        #los vertices(nodos principales) seran los indices de self.V[...]
        self.V = [Lista() for _ in range(self.MAXVERTEX + 1)]    # "_" es equivalente a "i", es mejor cuando dentro de nuestro bucle no reutilizaremos la varibale "i"
        self.num_vertices = -1   # se inicializa con -1 ya que es una manera de representar el Grafo vacio
        self.marca = [False for _ in range(self.MAXVERTEX + 1)]    

    def add_vertice(self):
        if self.num_vertices == self.MAXVERTEX:
            print("Grafo.addVertice: Demasiados vértices (solo se permiten {})".format(self.MAXVERTEX + 1))
            return
        self.num_vertices += 1
        self.V[self.num_vertices] = Lista()

    def cant_vertices(self):
        return self.num_vertices + 1

    def is_vertice_valido(self, v):
        valido = (0 <= v) and (v <= self.num_vertices)   
        if valido==False :
            print("Grafo.{}: {} no es un vértice del Grafo {}".format( v, self.get_indicacion()))
        return valido

    def tiene_conexiones_salientes(self, u):
        if not self.is_vertice_valido(u):
            return False
        return self.V[u].length() > 0
    
    def tiene_conexiones_entrantes(self, v):
        if not self.is_vertice_valido(v):
            return False
        for u in range(self.cant_vertices()):   #cant_vertices en todo el Grafo
            if self.costo(u, v) > 0:
                return True
        return False
    
    def add_arista(self, u, peso, v):  
        if peso <= 0:
            print("Grafo.addArista: El peso debe ser mayor que cero")
            return
        if not self.is_vertice_valido(u) or not self.is_vertice_valido(v):
            return ("error vertice no valido")
        self.V[u].add(v, peso)     

    def costo(self, u, v):
        if not self.is_vertice_valido(u) or not self.is_vertice_valido(v):
            return 0
        return self.V[u].get_peso(v)

    def desmarcar_todos(self):
        for i in range(self.num_vertices + 1):
            self.marca[i] = False

    def marcar(self, u):
        if self.is_vertice_valido(u):
            self.marca[u] = True

    def desmarcar(self, u):
        if self.is_vertice_valido(u):
            self.marca[u] = False

    def is_marcado(self, u):
        return self.marca[u]

    def costo_peso_minimo(self, peso):         #como todos los peso son 1, costo_peso_minimo siempre seleccionará el nodo
                                                 # no visitado más cercano al inicio en términos de número de pasos.
                                                    #El camino más corto será aquel que llegue al nodo final utilizando el menor número de nodos intermedios.
        i = 0                                                 
        while self.is_marcado(i):
            i += 1
        menor = peso[i]
        posicion = i
        for j in range(i + 1, len(peso)):
            if not self.is_marcado(j) and peso[j] < menor:
                menor = peso[j]
                posicion = j
        return posicion
    #como el peso es igual a 1, esto xe covierte en un recorrido BFS
    def camino_mas_corto_completo(self, a, z):
        peso = [float('inf')] * (self.num_vertices + 1)    #creacion de una lista de pesos inicializados en + infinito cada uno
        anterior = [-1] * (self.num_vertices + 1)     #creacion de lista  de vertice anterior, en el camino mas corto
        peso[a] = 0
        self.desmarcar_todos()
        pasos = []                                   #inicializacion de una lisa para almacenar los paso del algoritmo

        while not self.is_marcado(z):
            u = self.costo_peso_minimo(peso)
            self.marcar(u)

            for i in range(self.V[u].length()):
                w = self.V[u].get(i)
                if not self.is_marcado(w):
                    s = peso[u] + self.costo(u, w)    #para este caso donde el peso es 1 ; self.costo(u,w) siempre valdra 1
                    if peso[w] > s:
                        peso[w] = s
                        anterior[w] = u
                        pasos.append({
                            'nodo_actual': u,
                            'nodo_siguiente': w,
                            'peso_actual': s,
                            'camino_actual': self.reconstruir_camino(anterior, w)
                        })

        camino_final = self.reconstruir_camino(anterior, z)
        return camino_final, pasos

    def reconstruir_camino(self, anterior, u):
        camino = []
        while u != -1:
            camino.append(u)
            u = anterior[u]
        return list(reversed(camino))
