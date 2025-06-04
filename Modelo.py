from osmnx import nearest_nodes
from json import load

# abrir json
class Funcoes():
    def lerArquivo(caminhoArquivo):
        print("Lendo Json...")
        with open(caminhoArquivo, "r") as arquivo:
            dados = load(arquivo)
        return dados


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
                if self.visitantes in listaPessoasRecolhidas:
                    if self.ponto == 0:
                        self.ponto = nearest_nodes(grafo, X=self.coordenadas[1], Y=self.coordenadas[0])

    def calcularVisitantes(self, listaPessoas):
        for pessoa in listaPessoas:
            if pessoa.id == self.id:
                self.temVisitantes = True
                self.visitantes.append(pessoa)

    def adicionarVisitante(self, pessoa):
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
    
    
