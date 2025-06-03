import Dijkstra


def Caixeiro_preguiçoso(grafo, alunos, origem, destino):

    print("lista de alunos: ", alunos)
    alunos_a_visitar = list(set(alunos))

    print(f"Nós a visitar: {alunos_a_visitar}")

    # Vizinho Mais Próximo
    nos_a_visitar = set(alunos_a_visitar)
    tour = [origem]
    no_atual = origem
    total_dist = 0.0

    print(f"Iniciando tour a partir do nó: {origem}")

    while nos_a_visitar:
        vizinho_proximo = None
        menor_distancia = float('inf')

        print(f"  Nó atual: {no_atual}. Procurando vizinho mais próximo em {nos_a_visitar}")

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
                    print(f"    - Testando vizinho {no_vizinho}: Distância = {distancia:.2f} m")
                else:
                        print(f"    - Testando vizinho {no_vizinho}: Caminho encontrado não termina no destino ({caminho[-1]}).")
            elif distancia == float('inf'):
                print(f"    - Testando vizinho {no_vizinho}: Inalcançável (distância infinita).")
            else:
                print(f"    - Testando vizinho {no_vizinho}: Caminho não encontrado ou inválido (len(caminho)={len(caminho) if caminho else 0}).")


        # Move para o vizinho mais próximo
        total_dist += menor_distancia
        no_atual = vizinho_proximo
        tour += melhor_caminho[1:]  # Adiciona o caminho, exceto o nó atual (já está no tour)
        nos_a_visitar.remove(no_atual)
        print(f"  -> Movendo para {no_atual}. Distância acumulada: {total_dist:.2f} m")

    # vai para o destino
    if no_atual != destino:
        path, distance = Dijkstra.dijkstra(grafo, no_atual, destino)
        if path and len(path) > 1 and path[-1] == destino:
            total_dist += distance
            tour += path[1:]  # Adiciona o caminho, exceto o nó atual (já está no tour)
            print(f"  -> Indo para destino {destino}. Distância final: {total_dist:.2f} m")
        else:
            print(f"Não foi possível calcular o caminho do último aluno para o destino.")
            return None, float('inf'), None
  

#    print(f"Tour final (nós): {tour}")
    print(f"Distância total: {total_dist:.2f} m")
    return tour, total_dist



