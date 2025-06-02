import osmnx as ox
import networkx as nx
import folium
import json
import criaGrafo
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

    with open(caminho_arquivo, "r") as arquivo:
        dados = json.load(arquivo)
    return dados


listaEscolas = ler_arquivo("escolas.txt")
listaAlunos = ler_arquivo("alunos.txt")

# Coordenadas de origem e destino
orig_coord = [-22.95799250187836, -42.94133869533531]
dest_coord = [-22.9186637,-42.8835449]

#coordenada inicial

coordenadaInicial = [-22.9105756,-42.8363557]

# Baixar grafo da área em torno dos pontos
G = None
if os.path.exists(graph_filepath):
    print(f"Carregando grafo de '{graph_filepath}'...")
    G = ox.load_graphml(graph_filepath)
    print("Grafo carregado com sucesso.")
else:
    print(f"Baixando grafo para a área ao redor de {orig_coord}...")
    G = ox.graph_from_point(orig_coord, dist=15000, network_type="drive")
    print("Grafo baixado com sucesso.")
    print(f"Salvando grafo em '{graph_filepath}'...")
    ox.save_graphml(G, filepath=graph_filepath)
    print("Grafo salvo com sucesso.")

# nós de origem e destino
orig_no = ox.nearest_nodes(G,-22.95799250187836, -42.94133869533531)
dest_no = ox.nearest_nodes(G,-22.9186637,-42.8835449)

#le todos os nós e calcula a distancia entre eles, criando o grafo
grafo = criaGrafo.cria_grafo(listaAlunos,G,orig_no, dest_no)

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

#criar marcadores de escolas
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

#localizacao atual - falta verificar a coordenada do elemento
folium.vector_layers.Circle(location = (-22.910478, -42.834864), radius = 30, fill = 'blue', fill_opacity = .8).add_to(mapa)

folium.LayerControl().add_to(mapa)
# Salvar e exibir
mapa.save("mapa_marica.html") # salva um html
mapa.show_in_browser() # exibe temporario
