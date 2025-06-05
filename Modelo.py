from osmnx import nearest_nodes, graph_to_gdfs
from heapq import heappush, heappop
from json import load
from folium import Map, Marker, Icon, PolyLine, vector_layers, FeatureGroup, LayerControl

# abrir json
class Funcoes():
    def __init__(self):
        pass
    @staticmethod
    def lerArquivo(caminhoArquivo):
        print("Lendo Json...")
        with open(caminhoArquivo, "r") as arquivo:
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
    
    def calcular_distancias(self, lista, grafo, G, coordenadaInicial, listaPessoasRecolhidas):
        pontoAtual = nearest_nodes(G, X=coordenadaInicial[1], Y=coordenadaInicial[0] )
        distancias = []
        for item in lista:
            if isinstance(item, Pessoa):
                item.calcularPonto(G)
            else:
                item.calcularPonto(G, listaPessoasRecolhidas)
            if int(item.ponto)> 0:
                try:
                    caminho, dist = self.dijkstra(grafo, pontoAtual, item.ponto)
                    distancias.append((item, dist))
                except:
                    continue
        return sorted(distancias, key=lambda x: x[1])
    
    def plotarMapa(self, coordenadaInicial, listaBusca, grafo, G, listaPessoasRecolhidas, indice_ponto):
        
        pontoAtual = nearest_nodes(G, X=coordenadaInicial[1], Y=coordenadaInicial[0] )
        pontosProximosOrdenados = self.calcular_distancias(listaBusca, grafo, G, coordenadaInicial, listaPessoasRecolhidas)
        #print(pontosProximosOrdenados)
        mapa = Map(location=[coordenadaInicial[0],coordenadaInicial[1]], zoom_start=13, tiles="cartodb voyager")
        marcadores = FeatureGroup("Marcadores").add_to(mapa)
        grupoRota = FeatureGroup("RotaAtual").add_to(mapa)
        
        
        vector_layers.Circle(location = (G.nodes[pontoAtual]['y'], G.nodes[pontoAtual]['x']), radius = 30, fill = 'blue', fill_opacity = .8).add_to(mapa)
        for indice, item in enumerate(pontosProximosOrdenados):
            item[0].exibirMarcador(indice_ponto == indice, mapa, G, marcadores)

        # Converter o grafo em GeoDataFrames
        nodes, edges = graph_to_gdfs(G)

        caminho, distancia = self.dijkstra(grafo,pontoAtual,pontosProximosOrdenados[indice_ponto][0].ponto)

        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in caminho]
        
        
        PolyLine(route_coords, color="red", weight=4, opacity=0.8, tooltip=f"{distancia/1000:.2f} KM").add_to(grupoRota)

        coordenadaInicial = pontosProximosOrdenados[indice_ponto][0].coordenadas
        listaPessoasRecolhidas.append(pontosProximosOrdenados[indice_ponto][0])
        listaBusca.remove(pontosProximosOrdenados[indice_ponto][0])

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

    def calcularPonto(self, grafo):
        if not self.recolhido:
            if self.ponto == 0:
                self.ponto = nearest_nodes(grafo, X=self.coordenadas[1], Y=self.coordenadas[0])
            return self.ponto
                
    def exibirDados(self):
        print(f"{'='*20}")
        print(f"Nome: {self.nome}")
        print(f"DestinoId: {self.idDestino}")
        print(f"Coordenada: {self.coordenadas}")
        print(f"{'='*20}")
    
    def recolherPessoa(self):
        self.recolhido = True
    def exibirMarcador(self, indice, mapa, G, grupo):

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
        if self.temVisitantes:
            if len(listaPessoasRecolhidas) > 0:
                totalRecolhidos = set(listaPessoasRecolhidas)
                totalDestino = set(self.visitantes)
                if totalDestino.issubset(totalRecolhidos):
                    print(f'destino {self.nome} liberado para visitação')
                    if self.ponto == 0:
                        self.ponto = nearest_nodes(grafo, X=self.coordenadas[1], Y=self.coordenadas[0])


    def calcularVisitantes(self, listaPessoas):
        for pessoa in listaPessoas:
            if pessoa.id == self.id:
                self.temVisitantes = True
                self.visitantes.append(pessoa)

    def adicionarVisitante(self, pessoa):
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
    def exibirMarcador(self, indice, mapa, G, grupo):
        desembarque = "\n"
        for pessoa in self.visitantes:
            desembarque += "\n"+pessoa.nome
        Marker(
            location=(self.coordenadas[0], self.coordenadas[1]),
            tooltip=f"{self.nome}",
            icon=Icon(color=("blue" if indice else "lightblue"), icon=self.marcador, prefix="fa"),
            popup=f"Desembarque de:\n {desembarque}"
        ).add_to(grupo)
