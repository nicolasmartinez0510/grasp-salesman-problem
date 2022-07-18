import random
from utilidades import printer
import time
import sys

# random.seed(0)

def viajante_de_comercio(matriz_de_distancias, vertices): #O(n . n . log n)
    fuente = source_aleatorio(vertices) #O(1)
    visitar(fuente, vertices) #O(1)
    actual = fuente #O(1)
    visitados = 1 #O(1)
    costo_hasta_ahora = 0 #O(1)
    solucion = [fuente] #O(1)
    while visitados != len(vertices): #O(n)
        anterior = actual
        actual = obtener_mas_cercano_aleatorio(anterior, matriz_de_distancias, vertices) #O(n . log n)
        visitar(actual, vertices) #O(1)
        visitados += 1 #O(1)
        costo_hasta_ahora += matriz_de_distancias[anterior, actual] #O(1)
        solucion.append(actual) #O(1)
    costo_hasta_ahora += matriz_de_distancias[actual, fuente] #O(1)
    solucion.append(fuente) #O(1)
    return (solucion, costo_hasta_ahora)



def visitar(nodo, vertices): #O(1)
    vertices[nodo] = True #O(1)

def source_aleatorio(vertices): #O(1)
    return random.randint(0, len(vertices) - 1) #O(1)

def obtener_mas_cercano_aleatorio(nodo, matriz_de_distancias, vertices):
    #O(n + n . log n) => #O(n . log n) donde n es la cantidad de vertices
    def funcion_de_ordenamiento(adyacente):
        return vertices_y_distancias[adyacente] #O(1)

    vertices_y_distancias = {}
    for i in range(0, len(vertices)): #O(n)
        if(not vertices[i]):
            vertices_y_distancias[i] = (matriz_de_distancias[nodo, i])

    ordenados = sorted(vertices_y_distancias, key=funcion_de_ordenamiento) #O(n . log n)
    
    random_index =  random.randint(0, (len(ordenados) * 5 // 100)) #O(1) 5%
    return ordenados[random_index]


def busqueda_local(solucion, matriz_de_distancias): #O(n²)
    mejor_solucion = solucion[0].copy() #O(n)
    mejor_costo = solucion[1] #O(1)
    cantidad_de_iteraciones = 50 #O(1)

    while cantidad_de_iteraciones > 0: #O(1) dado que cantidad_de_iteraciones es constante
        vecino = buscar_vecino(matriz_de_distancias, mejor_solucion, mejor_costo) #O(n²)

        if(vecino[1] < mejor_costo): 
            mejor_solucion = vecino #O(1)
        elif vecino[1] == mejor_costo:
            break

        cantidad_de_iteraciones -= 1 #O(1)

    return mejor_solucion

def buscar_vecino(matriz_de_distancias, mejor_solucion, mejor_costo): #O(n²)
    mejor_solucion_encontrada = mejor_solucion
    mejor_costo_encontrado = mejor_costo

    for i in range(0, len(mejor_solucion_encontrada) - 2): #O(n)
            for j in range(i + 1, len(mejor_solucion_encontrada) - 1): #O(n)
                vertice_origen_anterior = mejor_solucion_encontrada[(i - 1) % len(mejor_solucion_encontrada)] #O(1)
                vertice_origen = mejor_solucion_encontrada[i] #O(1)
                vertice_destino = mejor_solucion_encontrada[j] #O(1)
                vertice_destino_siguiente = mejor_solucion_encontrada[j + 1] #O(1)

                costo_antes = matriz_de_distancias[vertice_origen_anterior, vertice_origen] + matriz_de_distancias[vertice_destino, vertice_destino_siguiente] #O(1)
                costo_actual = matriz_de_distancias[vertice_origen_anterior, vertice_destino] + matriz_de_distancias[vertice_origen, vertice_destino_siguiente] #O(1)

                costo_actual_total = (mejor_costo_encontrado + costo_actual) - costo_antes #O(1)

                if  costo_actual_total < mejor_costo_encontrado: #O(1)
                    sol_actual = mejor_solucion_encontrada[:] #O(1)
                    sol_actual[i:j+1] = mejor_solucion_encontrada[i:j+1][::-1] #O(1)
                    mejor_solucion_encontrada = sol_actual #O(1)
                    mejor_costo_encontrado = costo_actual_total #O(1)
    return (mejor_solucion_encontrada, mejor_costo_encontrado)

def grasp(matriz, vertices, nombre_instancia, iteraciones=20,): #O(log e . (n . n . log n + n²))
    # n = cantidad de vertices
    inicio = round(time.time() * 1000) #O(1)
    iteraciones_hasta_ahora = 0 #O(1)
    solucion_actual = viajante_de_comercio(matriz, vertices.copy()) #O(n . n . log n)
    mejor_solucion = busqueda_local(solucion_actual, matriz) #O(n²)
    tiempo_por_vuelta = round(time.time() * 1000) - inicio #O(1)
    
    lista_iteraciones = [] #O(1)
    resultados = [] #O(1)

    while iteraciones_hasta_ahora < iteraciones: #O(log e)
        solucion_actual = viajante_de_comercio(matriz, vertices.copy()) #O(n . n . log n)
        nueva_busqueda_local = busqueda_local(solucion_actual, matriz) #O(n²)
        print(f'[#{iteraciones_hasta_ahora}, {round(tiempo_por_vuelta)} msec]: costo {nueva_busqueda_local[1]}') #O(1)
        
        if nueva_busqueda_local[1] < mejor_solucion[1]:
            mejor_solucion = nueva_busqueda_local

        if((iteraciones % 10) == 0):
            lista_iteraciones.append(iteraciones_hasta_ahora) #O(1)
            resultados.append(mejor_solucion[1]) #O(1)
           
        tiempo_por_vuelta = round(time.time() * 1000) - inicio #O(1)
        iteraciones_hasta_ahora += 1 #O(1)
    print(f"Mejor costo encontrado con {len(vertices)} ciudades: {mejor_solucion[1]}") #O(1)

    if((iteraciones % 10) == 0): #O(1)
        lista_iteraciones.append(iteraciones_hasta_ahora) #O(1)
        resultados.append(mejor_solucion[1]) #O(1)

    printer(lista_iteraciones, resultados, nombre_instancia, len(vertices)) #O(1)
    return mejor_solucion

sys.modules[grasp] = grasp