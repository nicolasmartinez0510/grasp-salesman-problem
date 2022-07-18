from utilidades import writer,parsear_xml
from grasp import grasp

archivo = input('Nombre instancia: ')
cantidad_iteraciones = input('Cantidad de iteraciones: ')

grafo = parsear_xml(f'instancias/{archivo}.xml')
solucion = grasp(grafo['matriz'], grafo['vertices'], archivo, int(cantidad_iteraciones))
writer(solucion, archivo)

