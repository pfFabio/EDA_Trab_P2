from Modelo import Pessoa, Destino, Funcoes
from osmnx import load_graphml, graph_from_point, save_graphml
from os import path, makedirs
from json import load
from folium import LayerControl
from streamlit import title, button,columns,markdown, cache_resource,cache_data, session_state
from streamlit_folium import st_folium



funcoes = Funcoes()
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

lista = ler_arquivo("alunos.txt")

#coordenada inicial - GARAGEM

coordenadaInicial = [-22.9105756,-42.8363557]
localizacaoAtual = coordenadaInicial

# PREPARANDO LISTA DE ALUNOS EM OBJETOS
alunos = []

for aluno in lista['alunos']:
    alunos.append(Pessoa(aluno['id'], aluno['nome'], aluno['idEscola'], aluno['coordenadas']))


# PREPARANDO LISTA DE ESCOLAS QUE TEM ALUNOS A RECEBER EM OBJETOS
escolas = []
escolasIdCadastradas = []

for aluno in alunos:
    if aluno.idDestino not in escolasIdCadastradas:
        escolaEmCadastro = Destino(lista['escolas'][aluno.idDestino]['id'], lista['escolas'][aluno.idDestino]['nome'], lista['escolas'][aluno.idDestino]['coordenadas'])
        escolaEmCadastro.adicionarVisitante(aluno)
        escolas.append(escolaEmCadastro)
        escolasIdCadastradas.append(aluno.idDestino)
    else:
        for escola in escolas:
            if escola.id == aluno.idDestino:
                escola.adicionarVisitante(aluno)

#GRAFOS DE RUAS

#salvando ou abrindo grafos para nao recalcular

graph_filename = "marica_drive_graph.graphml"
graph_folder = "graphs" # Pasta para armazenar os grafos

# Cria a pasta 'graphs' se ela não existir
if not path.exists(graph_folder):
    makedirs(graph_folder)

graph_filepath = path.join(graph_folder, graph_filename)


# Baixar grafo da área em torno dos pontos
G = None
if path.exists(graph_filepath):
    print(f"Carregando grafo de ruas de '{graph_filepath}'...")
    G = load_graphml(graph_filepath)
    print("Grafo de ruas carregado com sucesso.")
else:
    print(f"Baixando grafo de ruas para a área ao redor de {localizacaoAtual}...")
    G = graph_from_point(localizacaoAtual, dist=15000, network_type="drive")
    print("Grafo baixado com sucesso.")
    print(f"Salvando grafo em '{graph_filepath}'...")
    save_graphml(G, filepath=graph_filepath)
    print("Grafo salvo com sucesso.")

#le todos os nós e organiza
grafo = funcoes.cria_grafo(G)

#CRIANDO LISTA DE BUSCAS
coordenadaInicial = [-22.9105756,-42.8363557]
listaBusca = [] 
listaPessoasRecolhidas = []

for aluno in alunos:
    listaBusca.append(aluno)

for escola in escolas:
    listaBusca.append(escola)

listaPessoasRecolhidas = [""]


title("PROVan")



trecho_idx = 0

# Inicializa índice de trecho e flag de primeira renderização
if "trecho_idx" not in session_state:
    session_state.trecho_idx = 0
if "mostrar_mapa" not in session_state:
    session_state.mostrar_mapa = True  # Primeira renderização

col1, col2, col3 = columns([1, 2, 1])

with col1:
    if button("⬅️ Anterior") and session_state.trecho_idx > 0:
        session_state.trecho_idx -= 1
        session_state.mostrar_mapa = True

with col3:
    if button("Próximo ➡️") and session_state.trecho_idx < len(listaBusca) - 1:
        session_state.trecho_idx += 1
        session_state.mostrar_mapa = True

with col2:
    markdown(
        f"<h4 style='text-align: center;'>{listaPessoasRecolhidas[-1]}</h4>",
        unsafe_allow_html=True
    )


# Se for a primeira vez ou se clicou em algum botão, plota o mapa
if session_state.get("mostrar_mapa", False):
    mapa_temp, listaBusca, coordenadaInicial, listaPessoasRecolhidas = funcoes.plotarMapa(
        coordenadaInicial, listaBusca, grafo, G, listaPessoasRecolhidas, session_state.trecho_idx
    )
    LayerControl().add_to(mapa_temp)



    
    st_folium(mapa_temp, width=900, height=600)
    
    #session_state.mostrar_mapa = False  # Resetar flag após plotar




