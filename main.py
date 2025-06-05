from Modelo import Pessoa, Destino, Funcoes
from Modelo import Pessoa, Destino, Funcoes
from osmnx import load_graphml, graph_from_point, save_graphml, nearest_nodes, graph_to_gdfs
from os import path, makedirs
from json import load
from folium import Map, FeatureGroup, PolyLine, Marker, Icon, vector_layers, LayerControl

funcoes = Funcoes()

# coordenada inicial - GARAGEM

coordenadaInicial = [-22.9105756,-42.8363557]
localizacaoAtual = coordenadaInicial


# PEGANDO DADOS DO JSON
lista = funcoes.lerArquivo("alunos.txt")


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


       
mapa, listaBusca, coordenadaInicial, listaPessoasRecolhidas = funcoes.plotarMapa(coordenadaInicial, listaBusca, grafo, G, listaPessoasRecolhidas, 0)
for pontos in listaPessoasRecolhidas:
    print(pontos.nome)
mapa.show_in_browser() # exibe temporario