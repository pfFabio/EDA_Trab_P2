"""
Algoritmo de Dijkstra para rotas de ônibus
Prioriza manter o passageiro na mesma linha para evitar trocas de veículos
O peso das arestas é o tempo de deslocamento entre pontos
"""

import heapq
from collections import defaultdict, namedtuple

# Estrutura para representar uma aresta no grafo
Aresta = namedtuple('Aresta', ['destino', 'tempo', 'linha'])

class GrafoOnibus:
    def __init__(self):
        # Dicionário que mapeia cada ponto para suas conexões (arestas)
        self.grafo = defaultdict(list)
        # Conjunto de todas as linhas de ônibus
        self.linhas = set()
        # Conjunto de todos os pontos de ônibus
        self.pontos = set()
    
    def adicionar_conexao(self, origem, destino, tempo, linha):
        """
        Adiciona uma conexão (aresta) entre dois pontos de ônibus.
        
        Args:
            origem: Ponto de origem
            destino: Ponto de destino
            tempo: Tempo de deslocamento entre os pontos (em minutos)
            linha: Identificador da linha de ônibus
        """
        self.grafo[origem].append(Aresta(destino=destino, tempo=tempo, linha=linha))
        self.pontos.add(origem)
        self.pontos.add(destino)
        self.linhas.add(linha)
    
    def dijkstra(self, origem, destino, penalidade_troca=5):
        """
        Implementação do algoritmo de Dijkstra adaptado para priorizar
        a permanência na mesma linha de ônibus.
        
        Args:
            origem: Ponto de partida
            destino: Ponto de chegada
            penalidade_troca: Tempo adicional (em minutos) ao trocar de linha
            
        Returns:
            Tupla contendo (tempo_total, caminho, linhas_usadas)
        """
        if origem not in self.pontos or destino not in self.pontos:
            return None, None, None
        
        # Inicializa as estruturas de dados
        # A fila de prioridade armazena (tempo_total, ponto_atual, linha_atual, caminho, linhas_usadas)
        fila_prioridade = [(0, origem, None, [origem], [])]
        # Dicionário para armazenar o menor tempo para cada combinação (ponto, linha)
        visitados = {}
        
        while fila_prioridade:
            # Obtém o nó com menor tempo acumulado
            tempo_atual, ponto_atual, linha_atual, caminho_atual, linhas_atuais = heapq.heappop(fila_prioridade)
            
            # Se chegamos ao destino, retornamos o resultado
            if ponto_atual == destino:
                return tempo_atual, caminho_atual, linhas_atuais
            
            # Se já visitamos este ponto com esta linha e com tempo menor, ignoramos
            if (ponto_atual, linha_atual) in visitados and visitados[(ponto_atual, linha_atual)] <= tempo_atual:
                continue
            
            # Marca como visitado
            visitados[(ponto_atual, linha_atual)] = tempo_atual
            
            # Explora as conexões a partir do ponto atual
            for aresta in self.grafo[ponto_atual]:
                proximo_ponto = aresta.destino
                tempo_conexao = aresta.tempo
                linha_conexao = aresta.linha
                
                # Calcula o tempo adicional se houver troca de linha
                tempo_adicional = 0
                if linha_atual is not None and linha_atual != linha_conexao:
                    tempo_adicional = penalidade_troca
                
                # Tempo total até o próximo ponto
                novo_tempo = tempo_atual + tempo_conexao + tempo_adicional
                
                # Atualiza o caminho e as linhas usadas
                novo_caminho = caminho_atual + [proximo_ponto]
                novas_linhas = linhas_atuais.copy()
                if not novas_linhas or novas_linhas[-1] != linha_conexao:
                    novas_linhas.append(linha_conexao)
                
                # Adiciona à fila de prioridade
                heapq.heappush(fila_prioridade, (novo_tempo, proximo_ponto, linha_conexao, novo_caminho, novas_linhas))
        
        # Se não encontrou caminho
        return None, None, None
    
    def imprimir_rota(self, origem, destino, penalidade_troca=5):
        """
        Imprime a melhor rota entre dois pontos, priorizando manter-se na mesma linha.
        
        Args:
            origem: Ponto de partida
            destino: Ponto de chegada
            penalidade_troca: Tempo adicional (em minutos) ao trocar de linha
        """
        tempo_total, caminho, linhas = self.dijkstra(origem, destino, penalidade_troca)
        
        if caminho is None:
            print(f"Não foi encontrada rota de {origem} para {destino}")
            return
        
        print(f"\nMelhor rota de {origem} para {destino}:")
        print(f"Tempo total: {tempo_total} minutos")
        print("Caminho:")
        
        linha_atual = None
        for i in range(len(caminho) - 1):
            ponto_atual = caminho[i]
            proximo_ponto = caminho[i + 1]
            
            # Encontra a linha usada entre estes dois pontos
            for aresta in self.grafo[ponto_atual]:
                if aresta.destino == proximo_ponto:
                    if linha_atual != aresta.linha:
                        if linha_atual is not None:
                            print(f"Troque para a linha {aresta.linha}")
                        else:
                            print(f"Pegue a linha {aresta.linha}")
                        linha_atual = aresta.linha
                    print(f"  {ponto_atual} -> {proximo_ponto} ({aresta.tempo} min)")
                    break
        
        print(f"Número de trocas de linha: {len(linhas) - 1}")
        print(f"Linhas utilizadas: {', '.join(linhas)}")


# Exemplo de uso
def criar_exemplo():
    """
    Cria um exemplo de rede de ônibus com múltiplas linhas e pontos.
    """
    grafo = GrafoOnibus()
    
    # Adiciona conexões para a linha 101
    grafo.adicionar_conexao("Terminal Central", "Praça da República", 5, "101")
    grafo.adicionar_conexao("Praça da República", "Hospital Municipal", 7, "101")
    grafo.adicionar_conexao("Hospital Municipal", "Shopping Norte", 10, "101")
    grafo.adicionar_conexao("Shopping Norte", "Bairro Industrial", 8, "101")
    
    # Adiciona conexões para a linha 102
    grafo.adicionar_conexao("Terminal Central", "Mercado Municipal", 4, "102")
    grafo.adicionar_conexao("Mercado Municipal", "Parque da Cidade", 6, "102")
    grafo.adicionar_conexao("Parque da Cidade", "Universidade", 5, "102")
    grafo.adicionar_conexao("Universidade", "Bairro Industrial", 12, "102")
    
    # Adiciona conexões para a linha 103
    grafo.adicionar_conexao("Terminal Central", "Estádio", 6, "103")
    grafo.adicionar_conexao("Estádio", "Hospital Municipal", 4, "103")
    grafo.adicionar_conexao("Hospital Municipal", "Parque da Cidade", 8, "103")
    grafo.adicionar_conexao("Parque da Cidade", "Shopping Norte", 9, "103")
    
    # Adiciona conexões para a linha 104
    grafo.adicionar_conexao("Mercado Municipal", "Praça da República", 3, "104")
    grafo.adicionar_conexao("Praça da República", "Estádio", 5, "104")
    grafo.adicionar_conexao("Estádio", "Universidade", 7, "104")
    
    return grafo

def executar_testes():
    """
    Executa testes com diferentes origens e destinos para demonstrar
    a priorização de manter-se na mesma linha.
    """
    grafo = criar_exemplo()
    
    # Teste 1: Rota direta na mesma linha
    print("\n=== TESTE 1: Rota na mesma linha ===")
    grafo.imprimir_rota("Terminal Central", "Bairro Industrial")
    
    # Teste 2: Rota com troca necessária
    print("\n=== TESTE 2: Rota com troca necessária ===")
    grafo.imprimir_rota("Estádio", "Bairro Industrial")
    
    # Teste 3: Comparação com diferentes penalidades de troca
    print("\n=== TESTE 3: Comparação com penalidade de troca baixa (2 min) ===")
    grafo.imprimir_rota("Terminal Central", "Shopping Norte", 2)
    
    print("\n=== TESTE 3: Comparação com penalidade de troca alta (10 min) ===")
    grafo.imprimir_rota("Terminal Central", "Shopping Norte", 10)

if __name__ == "__main__":
    executar_testes()