from Nodo import Nodo

class Lista:
    def __init__(self):
        self.L = None   # Lista inicia apuntando a vacio  , luego siempre apuntara al primera nodo de la lista de adyancecia de un vertive V    
        self.n = 0      #cantidad de nodos en dicha lista de de adyacencia V

    #recordemos que la lista de adyacencia son los nodos que estan conectados directamente a otro NODO, asi que en teoria
    # el orden de su adhesion a la lista de dayacencia no importa, pero para este caso, se hara en orden ascendente
    def add(self, data, peso):    #con esto self.V = [Lista() for _ in range(self.MAXVERTEX + 1)] ya se creo para cada lista de adyacencia su primer nodo, o nodo principal l
        Ant = None  
        p = self.L  
        while p is not None and data >= p.get_data():   #recorre la lista para insertar el nodo en el lugar correcto para seguir con el orden ascendente
            Ant = p
            p = p.get_link()  #p se mueve al siguiente Nodo de la lista, en caso de que se haga p.get_link(), estando en e ultimo nodo, p sera None
        if Ant is None:    #condicion if para la incercion del primer nodo de la lista de adyacencia
            nuevo = Nodo(data, peso)
            nuevo.set_link(self.L)   #unidireccional  #en la primer iteracion nuevo estaria apuntando a None
            self.L = nuevo            #desde este punto self.L siempre apuntara al nodo del principio de la lista, no se modificara
            self.n += 1
        elif Ant.get_data() != data:   #linea para evitar duplicados
            nuevo = Nodo(data, peso)
            Ant.set_link(nuevo)
            nuevo.set_link(p)
            self.n += 1

    def get(self, k):   #meotodo para obetener el dato de una posicion K , de dicha lista de adyacencia
        p = self.L
        i = 0
        while p is not None:
            if i == k:
                return p.get_data()

            p = p.get_link()   #avanza al siguiente ndo
            i += 1

        print("Lista.get: Fuera de rango")
        return -1

    def get_peso(self, data):  
        p = self.exist(data)
        if p is not None:
            return p.get_peso()

        return 0

    def length(self):   #metodo para obetener la lonigtud de la Lista
        return self.n

    def existe(self, data):    
        return self.exist(data) is not None   #devuelve un Booleano
    
    def exist(self, data): 
        p = self.L

        while p is not None and data > p.get_data():
            p = p.get_link()

        if p is not None and p.get_data() == data:
            return p       #p que ya esta apuntando al dato

        return None  