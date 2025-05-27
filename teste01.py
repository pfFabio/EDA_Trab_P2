import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Define o nome da cidade ou área de interesse
lugar = "Maricá, Brazil"

# Baixa o grafo da rede viária da área
G = ox.graph_from_place(lugar, network_type="drive")  # use 'drive' para carros

# Define coordenadas de origem e destino (longitude, latitude)
orig_coord = (-22.95799250187836, -42.94133869533531)  
dest_coord = (-22.904698114208646, -42.80202441250512)  

# Converte coordenadas para nós mais próximos no grafo
orig_node = ox.distance.nearest_nodes(G, X=orig_coord[1], Y=orig_coord[0])
dest_node = ox.distance.nearest_nodes(G, X=dest_coord[1], Y=dest_coord[0])

# Calcula a rota mais curta por distância
rota = nx.shortest_path(G, orig_node, dest_node, weight="length")

distancia_km = nx.shortest_path_length(G, orig_node, dest_node, weight="length")/1000

# Plota o grafo com a rota destacada
print(distancia_km)
fig, ax = ox.plot_graph_route(G, rota, route_linewidth=4, node_size=0, bgcolor='white')
plt.show()