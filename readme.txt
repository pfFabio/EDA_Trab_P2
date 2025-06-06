README - Sistema de Roteirização de Transporte Escolar

Descrição do Projeto

Este projeto é um sistema de roteirização para transporte escolar que utiliza algoritmos de otimização de rotas (Dijkstra) e dados geográficos para calcular os melhores trajetos entre pontos de coleta de alunos e suas escolas. O sistema foi desenvolvido em Python e utiliza bibliotecas como OSMnx para manipulação de dados de mapas e Folium para visualização geográfica.

Arquivos do Projeto
1. Modelo.py
    Contém as classes principais do sistema:

Funcoes - Classe utilitária com métodos para:
    Classe utilitária com métodos para
    Leitura de arquivos JSON
    Criação de grafos a partir de dados OSM
    Implementação do algoritmo de Dijkstra
    Cálculo de distâncias entre pontos
    Plotagem de mapas interativos

Pessoa - Representa um aluno com:
    Dados pessoais
    Coordenadas geográficas
    Escola de destino

Destino - Representa uma escola com:
    Dados da instituição
    Lista de alunos que frequentam
    Coordenadas geográficas

2. Main.ipynb

Notebook Jupyter - demonstra o uso do sistema:
    Carrega os dados de alunos e escolas
    Prepara os objetos do sistema
    Baixa/carrega o grafo de ruas da região
    Calcula e exibe rotas otimizadas
    Visualiza os resultados em mapas interativos

3. dados.txt

Armazena o Json com os dados de alunos e escolas cadastradas


4. requirements.txt
Lista de dependências do projeto, incluindo:

    OSMnx
    Folium
    GeoPandas
    NetworkX
    Entre outras

Como Usar
Instale as dependências:

    pip install -r requirements.txt

Execute o notebook Jupyter (Untitled.ipynb) para:
    Carregar os dados de alunos e escolas
    Calcular as rotas otimizadas
    Visualizar os resultados no mapa

Personalize as informações JSON do notebook Jupyter com seus próprios dados.



Funcionalidades Principais
    Cálculo automático da rota mais curta entre pontos
    Visualização interativa das rotas no mapa
    Agrupamento de alunos por escola de destino
    Identificação visual do próximo ponto de coleta
    Exibição de distâncias e trajetos

Requisitos
    Python 3.x
    Jupyter Notebook (para execução do notebook)
    Conexão com internet (para download inicial dos dados de mapa)

Observações
    O sistema armazena localmente os dados de mapa (em graphs/marica_drive_graph.graphml) para evitar downloads repetidos

    Os exemplos estão configurados para a região de Maricá-RJ, mas podem ser adaptados para qualquer localidade


Contribuição 
    Contribuições são bem-vindas! Siga os passos: 
    Faça um Fork do projeto 
    Crie uma branch (git checkout -b feature/nova-feature) 
    Commit suas mudanças (git commit -m 'Adiciona nova feature') 
    Push para a branch (git push origin feature/nova-feature) 
    Abra um Pull Request 
