# -*- coding: utf-8 -*-
from osmnx import nearest_nodes, graph_to_gdfs
from heapq import heappush, heappop
from json import load
from folium import Map, Marker, Icon, PolyLine, vector_layers, FeatureGroup, LayerControl

# abrir json
class Funcoes():
    def __init__(self):
        pass
    @staticmethod
    def lerArquivoJson(caminhoArquivo):
        print("Lendo Json...")
        with open(caminhoArquivo, "r", encoding="utf-8") as arquivo:
            dados = load(arquivo)
        return dados
    
    @staticmethod
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
    @staticmethod
    def dijkstra(grafo, origem, destino):
        #botando as distancias tudo pra infinito
        dist = {no: float('inf') for no in grafo}
        #resetando o anterior só em caso de bug
        anterior = {no: None for no in grafo}
        #distancia da origam né
        dist[origem] = 0
        #não sei o que é heap mas ta aí e ta dando bom
        heap = [(0, origem)]

        while heap:
            #dando pop na cabeça
            atual_dist, atual_no = heappop(heap)
            if atual_dist > dist[atual_no]:
                continue
            #testando se cheguei no destino//condição de parada
            if atual_no == destino:
                break
            #lendo os vizinhos do nó atual
            for vizinho in grafo.get(atual_no, {}):
                #pega distancia da aresta
                peso = grafo[atual_no][vizinho]
                #adiciona no acumulado
                nova_dist = atual_dist + peso
                #testando se o caminho é menor
                if nova_dist < dist[vizinho]:
                    #anotando a nova distancia
                    dist[vizinho] = nova_dist
                    #anotando o nó
                    anterior[vizinho] = atual_no
                    #adicionando no heap(ainda não entendi o heap)
                    heappush(heap, (nova_dist, vizinho))

        #agora volta pra ver qual foi o melhor caminho
        melhor_caminho = []
        #começa no destino pra voltar ao começo
        no = destino
        while no is not None:
            melhor_caminho.append(no)
            #quase uma recursão
            no = anterior[no]
        #print("Melhor caminho encontrado:", melhor_caminho)
        melhor_caminho.reverse()

        
        return melhor_caminho, dist[destino]
    
    def calcular_distancias(self, listaBusca, grafo, G, coordenadaInicial, listaPessoasRecolhidas):
        #CALCULA A DISTANCIA DO PONTO INICIAL A TODOS OS OUTROS PONTOS E CRIA UMA LISTA ORDENADA POR DISTANCIA, A LISTA CONTEM O OBJETO E A DISTANCIA CALCULADA
        #LISTABUSCA -  DEVE CONTER TODOS OBJETOS DE PESSOAS E DESTINOS
        # GRAFO - GRAFO CALCULADO UTILIZANDO FUNCAO DO FABIO
        # G - GRAFO DE RUAS OBTIDO PELO OSMNX
        # LISTA DE PESSOAS RECOLHIDAS - SÃO OS PONTOS QUE JÁ FORAM VISITADOS PELO INTERESSADO
        pontoAtual = nearest_nodes(G, X=coordenadaInicial[1], Y=coordenadaInicial[0] ) 
        distancias = []
        for item in listaBusca:
            if isinstance(item, Pessoa):
                item.calcularPonto(G) # funcao da classe pessoa
            else:
                item.calcularPonto(G, listaPessoasRecolhidas) #funcao da classe Destino 
            if int(item.ponto)> 0:
                try:
                    caminho, dist = self.dijkstra(grafo, pontoAtual, item.ponto)
                    distancias.append((item, dist)) #item é o objeto pessoa ou destino
                except:
                    continue
        return sorted(distancias, key=lambda x: x[1])
    
    def plotarMapa(self, coordenadaInicial, listaBusca, grafo, G, listaPessoasRecolhidas = [], indice_ponto = 0):
        
        pontoAtual = nearest_nodes(G, X=coordenadaInicial[1], Y=coordenadaInicial[0] )

        pontosProximosOrdenados = self.calcular_distancias(listaBusca, grafo, G, coordenadaInicial, listaPessoasRecolhidas)
        #INICIANDO MAPA
        mapa = Map(location=[coordenadaInicial[0],coordenadaInicial[1]], zoom_start=13, tiles="cartodb voyager", width='960px', height='640px')
        marcadores = FeatureGroup("Marcadores").add_to(mapa)
        grupoRota = FeatureGroup("RotaAtual").add_to(mapa)
        
        #CIRCULO AZUL DA LOCALIZAÇÃO DE PARTIDA
        vector_layers.Circle(location = (G.nodes[pontoAtual]['y'], G.nodes[pontoAtual]['x']), radius = 30, fill = 'blue', fill_opacity = .8).add_to(mapa)
        #CRIA OS MARCADORES
        for indice, item in enumerate(pontosProximosOrdenados):
            item[0].exibirMarcador(indice_ponto == indice, G, marcadores)

        # Converter o grafo em GeoDataFrames - UTILIZADO PARA CONVERTER PONTOS EM COORDENADAS
        nodes, edges = graph_to_gdfs(G)

        #OBTEM O CAMINHO DE ACORDO COM O INDICE_PONTO INFORMADO
        #INFORME "0" NO INDICE PARA SEMPRE BUSCAR O DESTINO MAIS PRÓXIMO
        caminho, distancia = self.dijkstra(grafo,pontoAtual,pontosProximosOrdenados[indice_ponto][0].ponto)

        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in caminho]
        
        # TRAÇA A ROTA ATUAL NO MAPA
        PolyLine(route_coords, color="red", weight=4, opacity=0.8, tooltip=f"{distancia/1000:.2f} KM").add_to(grupoRota)

        coordenadaInicial = pontosProximosOrdenados[indice_ponto][0].coordenadas # AJUSTA O POSICIONAMENTO DE PARTIDA PARA O PONTO DE CHEGADA ATUAL
        listaPessoasRecolhidas.append(pontosProximosOrdenados[indice_ponto][0]) # ADICIONA O PONTO PASSADO NA LISTA
        listaBusca.remove(pontosProximosOrdenados[indice_ponto][0]) # REMOVE O PONTO PASSADO DA LISTA DE OBJETIVOS

        LayerControl().add_to(mapa)
        return mapa, listaBusca, coordenadaInicial, listaPessoasRecolhidas


class Pessoa:
    def __init__(self, id, nome, idDestino, coordenadas):
        self.id = id
        self.nome = nome
        self.idDestino = idDestino
        self.coordenadas = coordenadas
        self.ponto = 0
        self.marcador = "user"
        self.recolhido = False

    def calcularPonto(self, G):
        #CONVERTE AS COORDENADAS NO PONTO MAIS PROXIMO DO GRAFO DE RUAS
        if not self.recolhido:
            if self.ponto == 0:
                self.ponto = nearest_nodes(G, X=self.coordenadas[1], Y=self.coordenadas[0])
            return self.ponto
                
    def exibirDados(self):
        print(f"{'='*20}")
        print(f"Nome: {self.nome}")
        print(f"DestinoId: {self.idDestino}")
        print(f"Coordenada: {self.coordenadas}")
        print(f"{'='*20}")
    
    def recolherPessoa(self):
        #OPÇAO PARA AO INVES DE TER LISTAPESSOASRECOLHIDAS CONTROLAR NO OBJETO
        self.recolhido = True

    def exibirMarcador(self, indice, G, grupo):

        Marker(
            location=(G.nodes[self.ponto]['y'], G.nodes[self.ponto]['x']),
            tooltip=f"{self.nome}",
            icon=Icon(color=("red" if indice else "gray"), icon=self.marcador, prefix="fa")
        ).add_to(grupo)

class Destino:
    def __init__(self, id, nome, coordenadas):
        self.id = id
        self.nome = nome
        self.coordenadas = coordenadas
        self.ponto = 0
        self.temVisitantes = False
        self.visitantes = []
        self.marcador = "building"
  
    def calcularPonto(self, grafo, listaPessoasRecolhidas = []):
        #SÓ CALCULA O PONTO SE A LISTA DE PESSOAS RECOLHIDAS JA TIVER TODAS AS PESSOAS COM ESSE DESTINO
        if self.temVisitantes:
            if len(listaPessoasRecolhidas) > 0:
                totalRecolhidos = set(listaPessoasRecolhidas)
                totalDestino = set(self.visitantes)
                if totalDestino.issubset(totalRecolhidos):
                    #print(f'destino {self.nome} liberado para visitação')
                    if self.ponto == 0:
                        self.ponto = nearest_nodes(grafo, X=self.coordenadas[1], Y=self.coordenadas[0])


    def calcularVisitantes(self, listaPessoas):
        #CALCULA OS VISITANTES QUE TEM O OBJETO COMO DESTINO
        for pessoa in listaPessoas:
            if pessoa.id == self.id:
                self.temVisitantes = True
                self.visitantes.append(pessoa)

    def adicionarVisitante(self, pessoa):
        #ADICIONA UM VISITANTE NA LISTA - APENAS OUTRA FORMA DE FAZER O CALCULAR VISITANTES
        self.temVisitantes = True
        self.visitantes.append(pessoa)

    def exibirDados(self):
        print(f"{'='*20}")
        print(f"Nome: {self.nome}")
        print(f"Visitantes: {len(self.visitantes)}")
        print(f"{'-'*20}")

    def exibirVisitantes(self):
        print(f"Pessoas a chegar em {self.nome}")
        print(f"{'-'*20}")
        for pessoa in self.visitantes:
            print(pessoa.nome)
        print(f"{'='*20}")

    def exibirMarcador(self, indice, G, grupo):
        desembarque = "\n"
        for pessoa in self.visitantes:
            desembarque += "\n"+pessoa.nome
        Marker(
            location=(self.coordenadas[0], self.coordenadas[1]),
            tooltip=f"{self.nome}",
            icon=Icon(color=("blue" if indice else "lightblue"), icon=self.marcador, prefix="fa"),
            popup=f"Desembarque de:\n {desembarque}"
        ).add_to(grupo)
