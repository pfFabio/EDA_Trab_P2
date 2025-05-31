import osmnx as ox
import networkx as nx

def cria_grafo(listaAlunos,G, origem, destino):
    # Mapear cada aluno para o nó mais próximo
    aluno_no = {}
    for aluno in listaAlunos['alunos']:
        coord = aluno['coordenadas']
        no = ox.nearest_nodes(G, X=coord[1], Y=coord[0])
        aluno_no[aluno['id']] = no

    # Criar o dicionário dos caminhos
    caminhos = {}
    caminhos['origem'] = {}
    caminhos['destino'] = {}

    for aluno_origem in listaAlunos['alunos']:
        id_origem = aluno_origem['id']
        no_origem = aluno_no[id_origem]

        caminhos[id_origem] = {}

        for aluno_destino in listaAlunos['alunos']:
            id_destino = aluno_destino['id']
            no_destino = aluno_no[id_destino]

            if id_origem != id_destino:
                # Calcular o caminho 
                caminho = nx.shortest_path(G, no_origem, no_destino, weight='length')
                distancia = nx.shortest_path_length(G, no_origem, no_destino, weight='length')

                caminhos[id_origem][id_destino] = {
                    'caminho': caminho,
                    'distancia_metros': distancia
                }

    for aluno in listaAlunos['alunos']:
        id_aluno = aluno['id']
        no_aluno = aluno_no[id_aluno]
        # origem
        caminho_origem = nx.shortest_path(G, origem, no_aluno, weight='length')
        distancia_origem = nx.shortest_path_length(G, origem, no_aluno, weight='length')
        caminhos['origem'][id_aluno] = {
            'caminho': caminho_origem,
            'distancia_metros': distancia_origem
        }
        # destino
        caminho_destino = nx.shortest_path(G, no_aluno, destino, weight='length')
        distancia_destino = nx.shortest_path_length(G, no_aluno, destino, weight='length')
        caminhos['destino'][id_aluno] = {
            'caminho': caminho_destino,
            'distancia_metros': distancia_destino
        }


