def cria_grafo(G):
    grafo = {}
    for u, v, data in G.edges(data=True):
        dist = data.get('length', 1)
        if u not in grafo:
            grafo[u] = {}
        grafo[u][v] = dist

        if not G.is_directed():
                if v not in grafo:
                    grafo[v] = {}
                grafo[v][u] = dist
    
    return grafo

