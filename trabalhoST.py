import streamlit as st
import folium
from folium import Marker, Icon, FeatureGroup, PolyLine, vector_layers, LayerControl
from streamlit_folium import st_folium
from osmnx import graph_from_point, load_graphml, save_graphml, nearest_nodes
import networkx as nx
from os import path, makedirs
from Dijkstra import dijkstra


st.set_page_config(layout="wide")

# Dados
GARAGEM = [-22.9105756, -42.8363557]
listaEscolas = [
    {
        "id": 0,
        "nome": "Escola Nova",
        "coordenadas": [-22.9036571,-42.8291497]
    }
]

listaAlunos = [
    {"id": 0, "nome": "Maria", "coordenadas": [-22.95799, -42.94133]},
    {"id": 1, "nome": "Joao", "coordenadas": [-22.95973, -42.94906]},
    {"id": 2, "nome": "José", "coordenadas": [-22.96099, -42.95644]},
    {"id": 3, "nome": "Antonieta", "coordenadas": [-22.92716, -42.81001]},
    {"id": 4, "nome": "Carlos", "coordenadas": [-22.93048, -42.81705]},
    {"id": 5, "nome": "Sebastião", "coordenadas": [-22.92906, -42.80881]},
    {"id": 6, "nome": "Fredericjson", "coordenadas": [-22.91325, -42.82804]},
    {"id": 7, "nome": "Thomaz", "coordenadas": [-22.89902, -42.81465]},
    {"id": 8, "nome": "Ana", "coordenadas": [-22.91167, -42.83834]}
]

# Grafo
graph_folder = "graphs"
graph_filename = "marica_drive_graph.graphml"
graph_filepath = path.join(graph_folder, graph_filename)

@st.cache_resource
def carregar_grafo():
    if not path.exists(graph_folder):
        makedirs(graph_folder)
    if path.exists(graph_filepath):
        return load_graphml(graph_filepath)
    G = graph_from_point(GARAGEM, dist=15000, network_type="drive")
    save_graphml(G, filepath=graph_filepath)
    return G

G = carregar_grafo()

# Nós
orig_no = nearest_nodes(G, GARAGEM[1], GARAGEM[0])
nos_alunos = [(aluno, nearest_nodes(G, aluno["coordenadas"][1], aluno["coordenadas"][0])) for aluno in listaAlunos]
nos_escolas = [(escola, nearest_nodes(G, escola["coordenadas"][1], escola["coordenadas"][0])) for escola in listaEscolas]

# Distâncias até alunos
def calcular_distancias_alunos():
    distancias = []
    for aluno, no_aluno in nos_alunos:
        try:
            caminho, dist = dijkstra(G, orig_no, no_aluno)
            distancias.append((aluno, no_aluno, dist))
        except:
            continue
    return sorted(distancias, key=lambda x: x[2])

if 'alunos_ordenados' not in st.session_state:
    st.session_state.alunos_ordenados = calcular_distancias_alunos()
if 'indice_aluno' not in st.session_state:
    st.session_state.indice_aluno = 0

if st.button("Próximo aluno"):
    st.session_state.indice_aluno += 1
    if st.session_state.indice_aluno >= len(st.session_state.alunos_ordenados):
        st.session_state.indice_aluno = 0

# Aluno atual
aluno_atual, no_aluno, dist_ate_aluno = st.session_state.alunos_ordenados[st.session_state.indice_aluno]

# Escolhe escola mais próxima do aluno
escola_mais_proxima, no_escola = min(nos_escolas, key=lambda e: nx.shortest_path_length(G, no_aluno, e[1], weight="length"))
dist_ate_escola = nx.shortest_path_length(G, no_aluno, no_escola, weight="length")

# Rota até aluno
rota1 = nx.shortest_path(G, orig_no, no_aluno, weight="length")
# Rota do aluno até escola
rota2 = nx.shortest_path(G, no_aluno, no_escola, weight="length")

# Coordenadas das rotas
def extrair_coords(rota):
    coords = []
    for u, v in zip(rota[:-1], rota[1:]):
        dados = G.get_edge_data(u, v)
        if dados:
            edge = list(dados.values())[0]
            if 'geometry' in edge:
                coords.extend([(lat, lon) for lon, lat in edge['geometry'].coords])
            else:
                coords.append((G.nodes[u]['y'], G.nodes[u]['x']))
                coords.append((G.nodes[v]['y'], G.nodes[v]['x']))
    return coords

coords1 = extrair_coords(rota1)
coords2 = extrair_coords(rota2)

# Mapa
center_lat = G.nodes[no_aluno]['y']
center_lon = G.nodes[no_aluno]['x']
mapa = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="cartodb positron")

# Alunos
fg_alunos = FeatureGroup("Alunos").add_to(mapa)
for aluno, no in nos_alunos:
    lat = G.nodes[no]['y']
    lon = G.nodes[no]['x']
    cor = "red" if no == no_aluno else "green"
    Marker(location=(lat, lon), tooltip=f"{aluno['nome']}", icon=Icon(color=cor)).add_to(fg_alunos)

# Escolas
fg_escolas = FeatureGroup("Escolas").add_to(mapa)
for escola, no in nos_escolas:
    lat = G.nodes[no]['y']
    lon = G.nodes[no]['x']
    Marker(location=(lat, lon), tooltip=f"{escola['nome']}", icon=Icon(color="blue", icon="graduation-cap", prefix="fa")).add_to(fg_escolas)

# Garagem
vector_layers.Circle(location=GARAGEM, radius=30, fill=True, fill_opacity=0.8, color="black").add_to(mapa)

# Rotas
PolyLine(coords1, color="purple", weight=4, tooltip="Garagem → Aluno").add_to(mapa)
LayerControl().add_to(mapa)

# Interface
st.title("🚍 Roteamento de Alunos")
st.markdown(f"**Aluno atual:** {aluno_atual['nome']}  \n**Distância até aluno:** {dist_ate_aluno:.2f} m  \n**Escola destino:** {escola_mais_proxima['nome']}  \n**Distância até escola:** {dist_ate_escola:.2f} m")
st_folium(mapa, width=1000, height=600)
