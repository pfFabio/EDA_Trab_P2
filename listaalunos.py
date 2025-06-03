from osmnx import nearest_nodes

def lista_alunos(id_escola, listaAlunos, G):
    alunos_ids_escola = []
    for aluno in listaAlunos['alunos']:
        if aluno['idEscola'] == id_escola:
            lat, lon = aluno['coordenadas']
            no_osmnx = nearest_nodes(G, lon, lat)
            alunos_ids_escola.append(no_osmnx)
    return alunos_ids_escola