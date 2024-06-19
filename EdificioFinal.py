import pandas as pd
import math
import matplotlib.pyplot as plt
import networkx as nx

#Materiales = pd.read_csv("G:\Proyectos Python\Materiales.txt")
datos = pd.read_excel('Materiales.xlsx', index_col=False)
df = pd.DataFrame(datos)

G={'a':['b','c'] ,'b':['d'],'c':['e'],'d':['f'],'e':['f'],'f':[]  }
visitado=set()
visitado2=set()


class Grafo_Dirigido:
    def __init__(self):
        self.dicc_grafo = {}
    
    def agregar_nodo(self,nodo):
        self.dicc_grafo[nodo] = []
        if nodo in self.dicc_grafo:
            return "El Nodo ya existe en el grafo"
        self.dicc_grafo[nodo] = []
    
    def agregar_arista(self,arista):
        nodo_origen = arista.get_nodo_origen()
        nodo_destino = arista.get_nodo_destino()
        if nodo_origen not in self.dicc_grafo:
            raise ValueError(f' El Nodo{nodo_origen.get_nombre()} no esta en el grafo')
        if nodo_destino not in self.dicc_grafo:
             raise ValueError(f' El Nodo{nodo_destino.get_nombre()} no esta en el grafo')
        self.dicc_grafo[nodo_origen].append(nodo_destino)

    def comprobar_nodo(self,nodo):
        return nodo in self.dicc_grafo

    def get_nodo(self,nombre_nodo):
        for n in self.dicc_grafo:
            if nombre_nodo == n.get_nombre() : return n
        print(f'El Nodo {nombre_nodo} no existe')

    def get_vecinos(self,nodo):
        return self.dicc_grafo[nodo]

    def __str__(self):
        todos_vertices = ''
        for nodo_origen in self.dicc_grafo:
            for nodo_destino in self.dicc_grafo[nodo_origen]:
                todos_vertices += nodo_origen.get_nombre() + '---->' + nodo_destino.get_nombre() + '\n'
        return todos_vertices

class Grafo_No_Dirigido (Grafo_Dirigido):
    def agregar_arista(self, arista):
        Grafo_Dirigido.agregar_arista(self, arista)
        arista_viceversa = Arista(arista.get_nodo_destino(), arista.get_nodo_origen())
        Grafo_Dirigido.agregar_arista(self, arista_viceversa)
     

class Arista:
    def __init__(self,nodo_origen,nodo_destino):
        self.nodo_origen = nodo_origen
        self.nodo_destino = nodo_destino
    
    def get_nodo_origen(self):
        return self.nodo_origen
    def get_nodo_destino(self):
        return self.nodo_destino
    def __str__(self):
        return self.nodo_origen.get_nombre() + '---->' + self.nodo_destino.get_nombre() 
        
class Nodo:
    def __init__(self,nombre, ruido, resistividad, piso ,transmision, mensaje):
        self.nombre = nombre
        self.ruido = ruido
        self.resistividad = resistividad
        self.piso = piso
        self.transmision=transmision
        self.mensaje = mensaje
    def set_transmision(self, ruido):
        self.ruido = ruido
    def get_nombre(self):
        return self.nombre
    def get_ruido(self):
        return self.ruido
    def get_mensaje(self):
        return self.mensaje
    
    def set_mensaje(self,mensaje):
        self.mensaje = mensaje
    def __str__(self):
        return self.nombre + '  =   ' + str(self.ruido)
    def set_resistividad(self, resistividad):
        self.resistividad = resistividad
    def get_resistividad(self):
        return self.resistividad
    def get_piso(self):
        return self.piso
    def get_transmision(self):
        return self.transmision
    def set_transmision(self,transmision):
        self.transmision = transmision

    def agregar_arista(self,arista):
        Grafo_Dirigido.agregar_arista(self,arista)
        arista_vuelta = Arista(arista.get_nodo_destino(),arista.get_nodo_origen())
        Grafo_Dirigido.agregar_arista(self,arista_vuelta)
    

def crear_grafo(grafo):
    g=grafo()
    for n in ( 'a','b','c','d','e','f'):
        g.agregar_nodo(Nodo(n,0,0,0,0,''))

    g.agregar_arista(Arista(g.get_nodo('a'),g.get_nodo('b')))
    g.agregar_arista(Arista(g.get_nodo('a'),g.get_nodo('f')))
    g.agregar_arista(Arista(g.get_nodo('b'),g.get_nodo('c')))
    g.agregar_arista(Arista(g.get_nodo('c'),g.get_nodo('d')))
    g.agregar_arista(Arista(g.get_nodo('c'),g.get_nodo('f')))
    g.agregar_arista(Arista(g.get_nodo('d'),g.get_nodo('e')))
    g.agregar_arista(Arista(g.get_nodo('e'),g.get_nodo('f')))

    return g

def calcular_resistividad(material:str, frecuencia:str):
    return (df[df['Material'] == material] [frecuencia]).values[0]


def busqueda_prof_imp_transmision(visitado,grafo:Grafo_No_Dirigido,diccionario,raiz):
    if raiz not in visitado:
        print(raiz)
        visitado.add(raiz)
        for vecinos in diccionario[raiz]:
            nodo_vecino:Nodo = grafo.get_nodo(vecinos)
            #nodo_vecino.set_transmision(10*math.log((100/2),10))
            print(nodo_vecino.get_transmision())
            busqueda_prof_imp_transmision(visitado,grafo,diccionario,vecinos)



def busqueda_prof_habitabilidad(visitado2,grafo:Grafo_No_Dirigido,diccionario,raiz):
    habitabilidad = 0
    if raiz not in visitado2:
        print(raiz)
        visitado2.add(raiz)
        nodo_raiz:Nodo = grafo.get_nodo(raiz)
        habitabilidad = nodo_raiz.get_resistividad() - nodo_raiz.get_transmision()
        nodo_raiz.set_mensaje(ver_habitabilidad(habitabilidad))        
        for vecinos in diccionario[raiz]:
            busqueda_prof_habitabilidad(visitado2,grafo,diccionario,vecinos)           

def determinar_transmision(calle,G1:Grafo_No_Dirigido):
    
    if calle is False:
        print('No hay ruido en la calle')
    else:
        primer_piso_izq:Nodo = G1.get_nodo('a')
        primer_piso_izq.set_transmision(100)
        G1.get_vecinos(primer_piso_izq)[1].set_transmision(50)
        #print(G1.get_vecinos(primer_piso_izq)[1])

        primer_piso_der:Nodo = G1.get_nodo('b')
        primer_piso_der.set_transmision(60)
        G1.get_vecinos(primer_piso_der)[1].set_transmision(20)
        #print(G1.get_vecinos(primer_piso_der)[1])

#FUNCION QUE DEPENDIENDO EL RESULTADO EN busqueda_prof_habitabilidad COMPARE SI ES <0 EL NODO NO ES HABITABLE --> SUGERENCIA
def ver_habitabilidad(habitabilidad):
    mensaje= ""
    if(habitabilidad <= -70):
        mensaje = "No habitable, sólo para usos comerciales cómo gimnasios, bares, discotecas" 
        return mensaje
    elif(habitabilidad <= -50):
        mensaje = "No habitable, sólo para uso social o comercial como restaurantes, tiendas" 
        return mensaje
    elif(habitabilidad <= -30):
        mensaje = "Habitable pero se aconseja material aislante para actividades cómo dormir o estudiar" 
        return mensaje
    elif(habitabilidad >= -29):
        mensaje = "Habitable" 
        return mensaje

def obtener_mensaje(grafo:Grafo_No_Dirigido, strNodo):
    grafo.get_nodo(strNodo).get_mensaje()

print("Grafo No dirigido")
G1 = crear_grafo(Grafo_No_Dirigido)
print(G1)

#Dada una frecunecia cualquiera muestra la resistividad del material
G1.get_nodo('a').set_resistividad(calcular_resistividad ('Ladrillo', 500) + calcular_resistividad ('Vidrio simple', 500) + calcular_resistividad ('Puerta de madera', 500))
print ("La resistividad de los materiales del apartamento A es: " + str(G1.get_nodo('a').get_resistividad()))
G1.get_nodo('b').set_resistividad(calcular_resistividad ('Ladrillo', 250) + calcular_resistividad ('Bloque de concreto', 250) + calcular_resistividad ('Vidrio laminado', 250))
print ("La resistividad de los materiales del apartamento B es: " + str(G1.get_nodo('b').get_resistividad()))
G1.get_nodo('c').set_resistividad(calcular_resistividad ('Bloque de concreto', 125) + calcular_resistividad ('Vidrio simple', 125) + calcular_resistividad ('Hormigon', 125))
print ("La resistividad de los materiales del apartamento C es: " + str(G1.get_nodo('c').get_resistividad()))
G1.get_nodo('d').set_resistividad(calcular_resistividad ('Hormigon', 1000) + calcular_resistividad ('Vidrio laminado', 1000) + calcular_resistividad ('Puerta de madera', 1000))
print ("La resistividad de los materiales del apartamento D es: " + str(G1.get_nodo('d').get_resistividad()))
G1.get_nodo('e').set_resistividad(calcular_resistividad ('Ladrillo', 2000) + calcular_resistividad ('Vidrio simple', 2000))
print ("La resistividad de los materiales del apartamento E es: " + str(G1.get_nodo('e').get_resistividad()))
G1.get_nodo('f').set_resistividad(calcular_resistividad ('Ladrillo', 4000) + calcular_resistividad ('Vidrio laminado', 4000) + calcular_resistividad ('Puerta de madera', 4000))
print ("La resistividad de los materiales del apartamento F es: " + str(G1.get_nodo('f').get_resistividad()))



#calcular_resistividad(G1)


calle = True

print("Resistividad")
print(G1.get_nodo('a').get_resistividad())

print("Ruido en la calle")
determinar_transmision(calle,G1)
busqueda_prof_imp_transmision(visitado,G1,G,'a')
print("")
print("")
print("habitabilidad")
busqueda_prof_habitabilidad(visitado2,G1,G,'a')


G2=nx.Graph()
G2.add_nodes_from(['a', 'b', 'c', 'd','e','f'])
G2.add_edges_from([('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e'), ('c', 'd') ,('d', 'f'),('e','f')])
pos = nx.spring_layout(G2)  # Obtener la posición de los nodos
pos = {'a': (0, 0), 'b':  (1, 0) , 'c': (0, 1), 'd': (1, 1),'e': (0, 2),'f': (1, 2)}
pos_lbl={'a': (0.01, 0.2), 'b':  (1, 0.2) , 'c': (0, 1.1), 'd': (1, 1.1),'e': (0, 2.1),'f': (1, 2.1)}
nx.draw_networkx(G2, pos)
labels = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd','e': 'e','f': 'f'}
labels2 = {}
print("############################################")
for n in ( 'a','b','c','d','e','f'):
    labels2[n] = G1.get_nodo(n).get_mensaje()
    print(G1.get_nodo(n).get_mensaje())
nx.draw_networkx_labels(G2, pos_lbl, labels2, font_size=8, font_color='black', horizontalalignment='left')
nx.draw_networkx_labels(G2, pos, labels)
plt.title("Habitabilidad Edificio")
plt.show()