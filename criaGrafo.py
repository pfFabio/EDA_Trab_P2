def cria_grafo(G):
    grafo = {}

    for node in G.nodes:
        grafo[node] = {}

    for u, v, data in G.edges(data=True):
        dist = data.get('length', 1)
        grafo[u][v] = dist


        if not G.is_directed():
            grafo[v][u] = dist
    
    return grafo

