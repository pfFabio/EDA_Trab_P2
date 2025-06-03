import osmnx as ox
import networkx as nx
import folium
import json
import criaGrafo
import Dijkstra
import os
#salvando grafos para nao recalcular

graph_filename = "marica_drive_graph.graphml"
graph_folder = "graphs" # Pasta para armazenar os grafos

# Cria a pasta 'graphs' se ela não existir
if not os.path.exists(graph_folder):
    os.makedirs(graph_folder)

graph_filepath = os.path.join(graph_folder, graph_filename)


# abrir json
def ler_arquivo(caminho_arquivo):
    print("Lendo Json...")
    with open(caminho_arquivo, "r") as arquivo:
        dados = json.load(arquivo)
    return dados


# Coordenadas de origem e destino
orig_coord = [-22.924934, -42.818895]
dest_coord = [-22.913423, -42.819966]



# nós de origem e destino
orig_no = ox.nearest_nodes(G, orig_coord[1], orig_coord[0])
dest_no = ox.nearest_nodes(G, dest_coord[1], dest_coord[0])

#le todos os nós e organiza
grafo = criaGrafo.cria_grafo(G)

route, distancia = Dijkstra.dijkstra(grafo, orig_no, dest_no)

# Converter o grafo em GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G)

# Criar mapa folium centralizado no ponto médio
center_lat = (orig_coord[0] + dest_coord[0]) / 2
center_lon = (orig_coord[1] + dest_coord[1]) / 2
mapa = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="cartodb voyager")

grupoEscolas = folium.FeatureGroup("Escolas").add_to(mapa)
grupoAlunos = folium.FeatureGroup("Alunos").add_to(mapa)
grupoRuas = folium.FeatureGroup("Ruas").add_to(mapa)
grupoRota = folium.FeatureGroup("RotaAtual").add_to(mapa)

"""# Adicionar ruas
for _, row in edges.iterrows():
    coords = [(lat, lon) for lon, lat in row["geometry"].coords]
    folium.PolyLine(coords, color="gray", weight=1, opacity=0.5).add_to(grupoRuas)
"""


# Adicionar rota do menor caminho
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
folium.PolyLine(route_coords, color="red", weight=4, opacity=0.8, tooltip="Menor caminho").add_to(grupoRota)


"""
criar marcadores de escolas
for escola in listaEscolas['escolas']:
    alunosEscola = []
    for aluno in listaAlunos['alunos']:
        aluno['idEscola'] == escola['id'] and alunosEscola.append(aluno['nome'])
        
        folium.Marker(
            aluno['coordenadas'], 
            tooltip=aluno['nome'], 
            popup=aluno['nome'], 
            icon=folium.Icon(prefix = "fa", color="red", icon= "graduation-cap") ).add_to(grupoAlunos)
    folium.Marker(
        escola['coordenadas'], 
        tooltip=escola['nome'], 
        popup=f"ALUNOS PARA ENTREGAR \n {alunosEscola}",
        icon=folium.Icon(prefix = "fa", color="blue", icon= "building")).add_to(grupoEscolas)
"""
#localizacao atual - falta verificar a coordenada do elemento
folium.vector_layers.Circle(location = (orig_coord[0], orig_coord[1]), radius = 30, fill = 'blue', fill_opacity = .8).add_to(mapa)

folium.LayerControl().add_to(mapa)
# Salvar e exibir
mapa.save("mapa_marica.html") # salva um html
mapa.show_in_browser() # exibe temporario
