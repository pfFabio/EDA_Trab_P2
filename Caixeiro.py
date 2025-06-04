import Dijkstra


def Caixeiro_preguicoso(grafo, alunos, origem, destino):
    trechos = []
    alunos_a_visitar = list(set(alunos))


    nos_a_visitar = set(alunos_a_visitar)
    tour = [origem]
    no_atual = origem
    total_dist = 0.0

    print(f"Iniciando tour a partir do nó: {origem}")

    while nos_a_visitar:
        vizinho_proximo = None
        menor_distancia = float('inf')

        # Encontra o vizinho não visitado mais próximo
        for no_vizinho in nos_a_visitar:
            # Chama Dijkstra para obter caminho e distância
            caminho, distancia = Dijkstra.dijkstra(grafo, no_atual, no_vizinho)

            # Verifica se um caminho foi encontrado
            if caminho and len(caminho) > 1 and distancia < menor_distancia:
                # Verifica se o caminho realmente termina no nó vizinho esperado
                if caminho[-1] == no_vizinho:
                    menor_distancia = distancia
                    vizinho_proximo = no_vizinho
                    melhor_caminho = caminho
 
        


        # Move para o vizinho mais próximo
        trechos.append(melhor_caminho)
        total_dist += menor_distancia
        no_atual = vizinho_proximo
        tour += melhor_caminho[1:]  # Adiciona o caminho, exceto o nó atual (já está no tour)
        nos_a_visitar.remove(no_atual)

    # vai para o destino
    if no_atual != destino:
        path, distance = Dijkstra.dijkstra(grafo, no_atual, destino)
        if path and len(path) > 1 and path[-1] == destino:
            trechos.append(path)
            total_dist += distance
            tour += path  # Adiciona o caminho, exceto o nó atual (já está no tour)
        else:
            return None, float('inf'), None
  

#    print(f"Tour final (nós): {tour}")
    return tour, total_dist, trechos



