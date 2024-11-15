import osmnx as ox
import networkx as nx
import folium
import matplotlib.pyplot as plt

# Загружаем граф для Москвы, улица Арбат
#city_name = "Ленинградский проспект, Москва, Россия"
#graph = ox.graph_from_place(city_name, network_type="drive")

# Центр Ленинградского проспекта
center_point = (55.801765, 37.531894)  # Координаты Ленинградского проспекта
graph = ox.graph_from_point(center_point, dist=1480, network_type="drive") # Указание дистанции прорисовки карты + вид передвижения


# Проверяем размер графа
print(f"Граф успешно загружен. Количество узлов: {len(graph.nodes)}, количество рёбер: {len(graph.edges)}")

# Координаты начальной и конечной точки
orig_point = (55.802349, 37.529273)  # МАДИ
dest_point = (55.790491, 37.531373)  # Авиапарк

# Ближайшие узлы графа
orig_node = ox.distance.nearest_nodes(graph, X=orig_point[1], Y=orig_point[0])
dest_node = ox.distance.nearest_nodes(graph, X=dest_point[1], Y=dest_point[0])

# Построение кратчайшего маршрута
shortest_route = nx.shortest_path(graph, source=orig_node, target=dest_node, weight='length')

# Визуализация маршрута
fig, ax = ox.plot_graph_route(graph, shortest_route, show=False, close=False)

# Добавляем подписи к начальной и конечной точкам
ax.scatter([orig_point[1], dest_point[1]], [orig_point[0], dest_point[0]], 
           c=['red', 'blue'], s=100, zorder=5, label='Start/End Points')
ax.text(orig_point[1], orig_point[0] + 0.001, 'МАДИ', fontsize=12, color='red', zorder=6)
ax.text(dest_point[1] + 0.001, dest_point[0] - 0.001, 'Авиапарк', fontsize=12, color='blue', zorder=6)

plt.legend()
plt.show()

# Получение координат маршрута
route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_route]

# Создаем карту
m = folium.Map(location=orig_point, zoom_start=14)

# Добавляем маршрут на карту
folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.7).add_to(m)

# Отображение карты
m.save("route_map.html")
print('Карта загружена!')