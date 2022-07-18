import sys
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import xml.etree.ElementTree as ET

def writer(solucion, nombre_instancia):
    f = open(f"soluciones/{datetime.now().timestamp()}-{nombre_instancia}-solucion.txt", "w+")
    f.write("Camino: ")
    f.write("\n")
    for i in solucion[0]:
        
        f.write(f'{str(i)} -->')
        f.write("\n")
    f.write("\n")
    f.write(f"Costo: {str(solucion[1])}")
    f.close()

def printer(iteraciones, resultados, nombre_instancia, cant_ciudades): 
    df = pd.DataFrame({'x_values': iteraciones, 'y_values': resultados })
    plt.plot( 'x_values', 'y_values', data=df, color='skyblue')
    plt.suptitle(f"Instancia {nombre_instancia} para {cant_ciudades} ciudades")
    plt.xlabel("Iteraciones")
    plt.ylabel("Costo")
    plt.savefig(f'graficos/{nombre_instancia}-{len(iteraciones) - 1} iteraciones-{datetime.now().timestamp()}.jpg')
    # plt.show()

def parsear_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    grafo = root.find('graph')
    nodos = grafo.findall('vertex')
    matriz = {}
    vertices = []
    for i,v in enumerate(nodos):
        matriz[i,i] = 0
        vertices.append(False)
        for edge in v.findall('edge'):
            matriz[i,int(edge.text)] = float(edge.get("cost"))
    return {'matriz': matriz, 'vertices': vertices}

sys.modules[printer] = printer
sys.modules[writer] = writer
sys.modules[parsear_xml] = parsear_xml