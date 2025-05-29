import osmnx as ox
import networkx as nx
import folium
import json

def ler_arquivo(caminho_arquivo):

    with open(caminho_arquivo, "r") as arquivo:
        dados = json.load(arquivo)
    return dados

listaEscolas = ler_arquivo("escolas.txt")
listaAlunos = ler_arquivo("alunos.txt")

# Coordenadas de origem e destino
orig_coord = listaAlunos["alunos"][0]['coordenadas']
dest_coord = listaEscolas["escolas"][listaAlunos["alunos"][0]['idEscola']]['coordenadas']

# Baixar grafo da área em torno dos pontos
G = ox.graph_from_point(orig_coord, dist=15000, network_type="drive")

# Encontrar os nós mais próximos às coordenadas
orig_node = ox.nearest_nodes(G, X=orig_coord[1], Y=orig_coord[0])
dest_node = ox.nearest_nodes(G, X=dest_coord[1], Y=dest_coord[0])

# Calcular o menor caminho (por distância)
route = nx.shortest_path(G, source=orig_node, target=dest_node, weight="length")

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
