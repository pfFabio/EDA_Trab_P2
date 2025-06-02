import heapq




def dijkstra(grafo, origem, destino):
    #botando as distancias tudo pra infinito
    dist = {no: float('inf') for no in grafo}
    #resetando o anterior só em caso de bug
    anterior = {no: None for no in grafo}
    #distancia da origam né
    dist[origem] = 0
    #não sei o que é heap mas ta aí e ta dando bom
    heap = [(0, origem)]

    while heap:
        #dando pop na cabeça
        atual_dist, atual_no = heapq.heappop(heap)
        if atual_dist > dist[atual_no]:
            continue
        #testando se cheguei no destino//condição de parada
        if atual_no == destino:
            break
        #lendo os vizinhos do nó atual
        for vizinho in grafo.get(atual_no, {}):
            #pega distancia da aresta
            peso = grafo[atual_no][vizinho]
            #adiciona no acumulado
            nova_dist = atual_dist + peso
            #testando se o caminho é menor
            if nova_dist < dist[vizinho]:
                #anotando a nova distancia
                dist[vizinho] = nova_dist
                #anotando o nó
                anterior[vizinho] = atual_no
                #adicionando no heap(ainda não entendi o heap)
                heapq.heappush(heap, (nova_dist, vizinho))

    #agora volta pra ver qual foi o melhor caminho
    melhor_caminho = []
    #começa no destino pra voltar ao começo
    no = destino
    while no is not None:
        melhor_caminho.append(no)
        #quase uma recursão
        no = anterior[no]
    print("Melhor caminho encontrado:", melhor_caminho)
    melhor_caminho.reverse()

    
    return melhor_caminho, dist[destino]
    