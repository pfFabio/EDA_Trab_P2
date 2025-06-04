from osmnx import load_graphml, graph_from_point, save_graphml, nearest_nodes, graph_to_gdfs
from folium import Map, FeatureGroup, PolyLine, Marker, Icon, vector_layers, LayerControl
from json import load
import criaGrafo
from listaalunos import lista_alunos
from Caixeiro import Caixeiro_preguicoso
from os import path, makedirs
from streamlit import title, button,columns,markdown, cache_resource,cache_data, session_state, selectbox
from streamlit_folium import st_folium
#salvando grafos para nao recalcular

graph_filename = "marica_drive_graph.graphml"
graph_folder = "graphs" # Pasta para armazenar os grafos

# Cria a pasta 'graphs' se ela não existir
if not path.exists(graph_folder):
    makedirs(graph_folder)

graph_filepath = path.join(graph_folder, graph_filename)


# abrir json
@cache_data
def ler_arquivo(caminho_arquivo):
    print("Lendo Json...")
    with open(caminho_arquivo, "r") as arquivo:
        dados = load(arquivo)
    return dados

listaEscolas = ler_arquivo("escolas.txt")
listaAlunos = ler_arquivo("alunos.txt")

#coordenada inicial - GARAGEM

coordenadaInicial = [-22.9105756,-42.8363557]
localizacaoAtual = coordenadaInicial

escolas_options = [
    f"{escola['id']} - {escola.get('nome', 'Sem nome')}" for escola in listaEscolas['escolas']
]
escolas_ids = [escola['id'] for escola in listaEscolas['escolas']]

id_escola = selectbox(
    "Selecione a escola:",
    options=range(len(escolas_options)),
    format_func=lambda idx: escolas_options[idx],
    index=0
)



dest_coord = listaEscolas["escolas"][id_escola]['coordenadas']


# Baixar grafo da área em torno dos pontos
G = None

@cache_resource
def carregar_grafo(graph_filepath, coordenadaInicial):
    if path.exists(graph_filepath):
        print(f"Carregando grafo de '{graph_filepath}'...")
        G = load_graphml(graph_filepath)
        print("Grafo carregado com sucesso.")
    else:
        print(f"Baixando grafo para a área ao redor de {coordenadaInicial}...")
        G = graph_from_point(coordenadaInicial, dist=15000, network_type="drive")
        print("Grafo baixado com sucesso.")
        print(f"Salvando grafo em '{graph_filepath}'...")
        save_graphml(G, filepath=graph_filepath)
        print("Grafo salvo com sucesso.")
    return G

G = carregar_grafo(graph_filepath, coordenadaInicial)

# nós de origem e destino
orig_no = nearest_nodes(G, float(coordenadaInicial[1]), float(coordenadaInicial[0]))
dest_no = nearest_nodes(G, float(dest_coord[1]), float(dest_coord[0]))

#le todos os nós e organiza
grafo = criaGrafo.cria_grafo(G)



#cria lista de alunos (id escola, lista de alunos, grafo)
nosAlunos = lista_alunos(id_escola, listaAlunos, G)


# Executar o algoritmo do Caixeiro Preguiçoso
@cache_data
def carregar_trechos(grafo, nosAlunos, orig_no, dest_no):
    return Caixeiro_preguicoso(grafo, nosAlunos, orig_no, dest_no)
    
caminhos, total_dist, trechos = carregar_trechos(grafo, nosAlunos, orig_no, dest_no)

# Converter o grafo em GeoDataFrames
nodes, edges = graph_to_gdfs(G)

# Criar mapa folium centralizado no ponto médio
center_lat = (coordenadaInicial[0] + dest_coord[0]) / 2
center_lon = (coordenadaInicial[1] + dest_coord[1]) / 2
mapa = Map(location=[center_lat, center_lon], zoom_start=13, tiles="cartodb voyager")


grupoRuas = FeatureGroup("Ruas").add_to(mapa)
grupoRota = FeatureGroup("RotaAtual").add_to(mapa)


title("Mapa de Trechos")

# Slider para escolher o trecho
if "trecho_idx" not in session_state:
    session_state.trecho_idx = 0

col1, col2, col3 = columns([1,2,1])

with col1:
    if button("⬅️ Anterior") and session_state.trecho_idx > 0:
        session_state.trecho_idx -= 1

with col3:
    if button("Próximo ➡️") and session_state.trecho_idx < len(trechos) - 1:
        session_state.trecho_idx += 1

with col2:
    markdown(f"<h4 style='text-align: center;'>Trecho {session_state.trecho_idx + 1} de {len(trechos)}</h4>", unsafe_allow_html=True)

trecho_idx = session_state.trecho_idx

trecho = trechos[trecho_idx]


rota_coords = []
for i, (u, v) in enumerate(zip(trecho[:-1], trecho[1:])):
    edge_data = G.get_edge_data(u, v)
    if edge_data is None:
        continue
    edge = list(edge_data.values())[0]
    if 'geometry' in edge:
        coords = [(lat, lon) for lon, lat in edge['geometry'].coords]
        if i == 0:
            rota_coords.extend(coords)
        else:
            rota_coords.extend(coords[1:])
    else:
        lat1, lon1 = G.nodes[u]['y'], G.nodes[u]['x']
        lat2, lon2 = G.nodes[v]['y'], G.nodes[v]['x']
        if i == 0:
            rota_coords.append((lat1, lon1))
        rota_coords.append((lat2, lon2))


if trecho:
    start_node = trecho[0]
    center_lat = G.nodes[start_node]['y']
    center_lon = G.nodes[start_node]['x']
print(start_node)

mapa_temp = Map(location=[center_lat, center_lon], zoom_start=13, tiles="cartodb voyager")

PolyLine(rota_coords, color="green", weight=4, opacity=0.8, tooltip="Menor caminho").add_to(mapa_temp)
#localizacao atual - falta verificar a coordenada do elemento
vector_layers.Circle(location = (center_lat, center_lon), radius = 30, fill = 'blue', fill_opacity = .8).add_to(mapa_temp)
    




# marcadores de escolas
grupoEscolas = FeatureGroup("Escolas").add_to(mapa_temp)
for escola in listaEscolas['escolas']:
    lat = escola['coordenadas'][0]
    lon = escola['coordenadas'][1]
    Marker(
        location=(lat, lon),
        tooltip=f"Escola {escola.get('nome', escola.get('id', ''))}",
        icon=Icon(color="blue", icon="graduation-cap", prefix="fa")
    ).add_to(grupoEscolas)

# marcadores de alunos
grupoAlunos = FeatureGroup("Alunos").add_to(mapa_temp)
for node_id in nosAlunos:
    lat = G.nodes[node_id]['y']
    lon = G.nodes[node_id]['x']
    Marker(
        location=(lat, lon),
        tooltip=f"Aluno {node_id}",
        icon=Icon(color="green", icon="user")
    ).add_to(grupoAlunos)

LayerControl().add_to(mapa_temp)
st_folium(mapa_temp, width=900, height=600)



