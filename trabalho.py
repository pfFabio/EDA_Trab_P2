from osmnx import load_graphml, graph_from_point, save_graphml, nearest_nodes, graph_to_gdfs
from folium import Map, FeatureGroup, PolyLine, Marker, Icon, vector_layers, LayerControl
from json import load
import criaGrafo
import Dijkstra
from os import path, makedirs
#salvando grafos para nao recalcular

graph_filename = "marica_drive_graph.graphml"
graph_folder = "graphs" # Pasta para armazenar os grafos

# Cria a pasta 'graphs' se ela não existir
if not path.exists(graph_folder):
    makedirs(graph_folder)

graph_filepath = path.join(graph_folder, graph_filename)


# abrir json
def ler_arquivo(caminho_arquivo):
    print("Lendo Json...")
    with open(caminho_arquivo, "r") as arquivo:
        dados = load(arquivo)
    return dados

listaEscolas = ler_arquivo("escolas.txt")
listaAlunos = ler_arquivo("alunos.txt")

#coordenada inicial - GARAGEM

coordenadaInicial = [-22.9105756,-42.8363557]

# Coordenadas de origem e destino
orig_coord = coordenadaInicial
dest_coord = listaEscolas["escolas"][listaAlunos["alunos"][7]['idEscola']]['coordenadas']

print(dest_coord)
# Baixar grafo da área em torno dos pontos
G = None
if path.exists(graph_filepath):
    print(f"Carregando grafo de '{graph_filepath}'...")
    G = load_graphml(graph_filepath)
    print("Grafo carregado com sucesso.")
else:
    print(f"Baixando grafo para a área ao redor de {orig_coord}...")
    G = graph_from_point(orig_coord, dist=15000, network_type="drive")
    print("Grafo baixado com sucesso.")
    print(f"Salvando grafo em '{graph_filepath}'...")
    save_graphml(G, filepath=graph_filepath)
    print("Grafo salvo com sucesso.")

# nós de origem e destino
orig_no = nearest_nodes(G, float(orig_coord[1]), float(orig_coord[0]))
dest_no = nearest_nodes(G, float(dest_coord[1]), float(dest_coord[0]))

#le todos os nós e organiza
grafo = criaGrafo.cria_grafo(G)

route, distancia = Dijkstra.dijkstra(grafo, orig_no, dest_no)

# Converter o grafo em GeoDataFrames
nodes, edges = graph_to_gdfs(G)

# Criar mapa folium centralizado no ponto médio
center_lat = (orig_coord[0] + dest_coord[0]) / 2
center_lon = (orig_coord[1] + dest_coord[1]) / 2
mapa = Map(location=[center_lat, center_lon], zoom_start=13, tiles="cartodb voyager")

grupoEscolas = FeatureGroup("Escolas").add_to(mapa)
grupoAlunos = FeatureGroup("Alunos").add_to(mapa)
grupoRuas = FeatureGroup("Ruas").add_to(mapa)
grupoRota = FeatureGroup("RotaAtual").add_to(mapa)

"""# Adicionar ruas
for _, row in edges.iterrows():
    coords = [(lat, lon) for lon, lat in row["geometry"].coords]
    PolyLine(coords, color="gray", weight=1, opacity=0.5).add_to(grupoRuas)
"""


# Adicionar rota do menor caminho
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
PolyLine(route_coords, color="red", weight=4, opacity=0.8, tooltip="Menor caminho").add_to(grupoRota)


"""
criar marcadores de escolas
for escola in listaEscolas['escolas']:
    alunosEscola = []
    for aluno in listaAlunos['alunos']:
        aluno['idEscola'] == escola['id'] and alunosEscola.append(aluno['nome'])
        
        Marker(
            aluno['coordenadas'], 
            tooltip=aluno['nome'], 
            popup=aluno['nome'], 
            icon=Icon(prefix = "fa", color="red", icon= "graduation-cap") ).add_to(grupoAlunos)
    Marker(
        escola['coordenadas'], 
        tooltip=escola['nome'], 
        popup=f"ALUNOS PARA ENTREGAR \n {alunosEscola}",
        icon=Icon(prefix = "fa", color="blue", icon= "building")).add_to(grupoEscolas)
"""
#localizacao atual - falta verificar a coordenada do elemento
vector_layers.Circle(location = (orig_coord[0], orig_coord[1]), radius = 30, fill = 'blue', fill_opacity = .8).add_to(mapa)

LayerControl().add_to(mapa)
# Salvar e exibir
#mapa.save("mapa_marica.html") # salva um html
mapa.show_in_browser() # exibe temporario
