# a principio vou descartar
import Dijkstra
from osmnx import nearest_nodes
from json import load
# abrir json
def ler_arquivo(caminho_arquivo):
    print("Lendo Json...")
    with open(caminho_arquivo, "r") as arquivo:
        dados = load(arquivo)
    return dados

listaEscolas = ler_arquivo("escolas.txt")
listaAlunos = ler_arquivo("alunos.txt")

def adicionarPontoNoDicionario(grafo, lista):
    for item in lista:
        item['ponto'] = nearest_nodes(grafo, X=item['coordenadas'][1], Y=item['coordenadas'][0])


for aluno in listaAlunos['alunos']:
    aluno['ponto'] = nearest_nodes(grafo, X=aluno['coordenadas'][1], Y=aluno['coordenadas'][0])
    print(aluno)




def definirProximosPontos(grafo, listaAlunos, listaEscolas, origem, destino, listaBusca = []):
    alunosRecolhidos = []
    escolasLiberadas = [] #quando todos alunos da escola ja tiverem recolhidos ela é adicionada a lista
    pontosAlunosPorEscola = []
    if len(listaBusca) == 0:
        for aluno in listaAlunos['alunos']:
            listaBusca.append(aluno['id'])


    for escola in listaEscolas['escolas']:
        pontosAlunos = []
        idAlunos = []
        nomes = []
        for aluno in listaAlunos['alunos']:
            if aluno['idEscola'] == escola['id']:
                pontosAlunos.append(nearest_nodes(grafo, X=aluno['coordenadas'][1], Y=aluno['coordenadas'][0]))
                idAlunos.append(aluno['id'])
                nomes.append(aluno['nome'])
        if len(pontosAlunos) > 0:
            ponto = nearest_nodes(grafo, X=escola['coordenadas'][1], Y=escola['coordenadas'][0])
            pontosAlunosPorEscola.append(dict(idEscola = escola['id'], nomeEscola = escola['nome'], pontoEscola = ponto, alunosId = idAlunos, nomeAluno = nomes, pontosAlunos = pontosAlunos))

    if len(alunosRecolhidos) > 0:
        for alunos in alunosRecolhidos:

            print(pontosAlunosPorEscola)
        for escola in pontosAlunosPorEscola:
            print(pontosAlunosPorEscola)


    return None

"""
    print("lista de pontos a visitar: ", todosPontos)
    Pontos = list(set(todosPontos))

    print(f"Nós a visitar: {alunos_a_visitar}")

    # Vizinho Mais Próximo
    nos_a_visitar = set(alunos_a_visitar)
    tour = [origem]
    no_atual = origem
    total_dist = 0.0

    print(f"Iniciando tour a partir do nó: {origem}")

    while nos_a_visitar:
        vizinho_proximo = None
        menor_distancia = float('inf')

        print(f"  Nó atual: {no_atual}. Procurando vizinho mais próximo em {nos_a_visitar}")

        # Encontra o vizinho não visitado mais próximo
        for no_vizinho in nos_a_visitar:
            # Chama Dijkstra para obter caminho e distância
            caminho, distancia = Dijkstra.dijkstra(grafo, no_atual, no_vizinho)

            # Verifica se um caminho foi encontrado
            if caminho and len(caminho) > 1 and distancia < menor_distancia:
                # Verifica se o caminho realmente termina no nó vizinho esperado
                if caminho[-1] == no_vizinho:
                    menor_distancia = distancia
                    vizinho_proximo = no_vizinho
                    melhor_caminho = caminho
                    print(f"    - Testando vizinho {no_vizinho}: Distância = {distancia:.2f} m")
                else:
                        print(f"    - Testando vizinho {no_vizinho}: Caminho encontrado não termina no destino ({caminho[-1]}).")
            elif distancia == float('inf'):
                print(f"    - Testando vizinho {no_vizinho}: Inalcançável (distância infinita).")
            else:
                print(f"    - Testando vizinho {no_vizinho}: Caminho não encontrado ou inválido (len(caminho)={len(caminho) if caminho else 0}).")


        # Move para o vizinho mais próximo
        total_dist += menor_distancia
        no_atual = vizinho_proximo
        tour += melhor_caminho[1:]  # Adiciona o caminho, exceto o nó atual (já está no tour)
        nos_a_visitar.remove(no_atual)
        print(f"  -> Movendo para {no_atual}. Distância acumulada: {total_dist:.2f} m")

    # vai para o destino
    if no_atual != destino:
        path, distance = Dijkstra.dijkstra(grafo, no_atual, destino)
        if path and len(path) > 1 and path[-1] == destino:
            total_dist += distance
            tour += path[1:]  # Adiciona o caminho, exceto o nó atual (já está no tour)
            print(f"  -> Indo para destino {destino}. Distância final: {total_dist:.2f} m")
        else:
            print(f"Não foi possível calcular o caminho do último aluno para o destino.")
            return None, float('inf'), None
  

#    print(f"Tour final (nós): {tour}")
    print(f"Distância total: {total_dist:.2f} m")
    return tour, total_dist"""



