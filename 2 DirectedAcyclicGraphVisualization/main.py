#                       Задание 2: Визуализация ациклических ориентированных графов
# На входе алгоритма ациклический орграф и, опционально, число W (максимально допустимая ширина слоя).

# Требуется при наличествующем W реализовать распределение по слоям с помощью алгоритма Грэхема—Коффмана.
# При отсутствующем W нужно реализовать алгоритм минимизации количества dummy-вершин.

# После укладки по слоям требуется добавить нужно число dummy-вершин и 
# минимизировать (эвристическими средствами) количество пересечений рёбер, идущих между соседними слоями.

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import copy as cp
from scipy.optimize import linprog

def Order(a, b):
  len_a = len(a)
  len_b = len(b)
  if not len_a: return True
  if len_a and not len_b: return False
  sort_a = sorted(a, reverse=True)
  sort_b = sorted(b, reverse=True)
  min_len = len_a if len_a < len_b else len_b
  for i in range(min_len):
    if sort_a[i] != sort_b[i]:
      return sort_a[i] < sort_b[i]
  res = True if len_a < len_b else False
  return res

def LabelNodes(G):
  labeled = []
  nodes = sorted(G.nodes(), key = lambda x: G.in_degree[x])
  for i in range(len(nodes)):
    possible_nodes = {}
    for node in nodes:
      if node not in labeled:
        ancestors = [edge[0] for edge in G.edges() if edge[1] == node]
        if not len([0 for ancestor in ancestors if ancestor not in labeled]):
          possible_nodes[node] = ancestors

    labeled_node = next(iter(possible_nodes))
    for node, ancestors in possible_nodes.items():
      if Order(ancestors, possible_nodes[labeled_node]):
        labeled_node = node
    labeled.append(labeled_node)
  return labeled

def CheckDescendants(G, node, layers, current):
  layered = [y for x in [layers[i] for i in range(current)] for y in x]
  for edge in G.edges(node):
    if edge[1] not in layered:
      return False
  return True
  
def CoffmanGrahamLayering(G, W):
  labeled_nodes = LabelNodes(G)
  labeled_nodes.reverse()

  layers = [[]]
  used = []
  current = 0
  while(len(used) != len(labeled_nodes)):
    for node in labeled_nodes:
      if node not in used:
        if not len([0 for edge in G.edges(node) if edge[1] not in used]):
          if len(layers[current]) < W and CheckDescendants(G, node, layers, current):
            layers[current].append(node)
          else:
            current += 1
            layers.append([node])
          used.append(node)
  layers.reverse()
  return layers

def LinprogLayering(G):
  c = [0 for node in G.nodes()]
  A = [[0 for node in G.nodes()] for edge in G.edges()] 
  for i, edge in enumerate(G.edges()):
    c[edge[0]] -= 1
    c[edge[1]] += 1
    
    A[i][edge[0]] = 1
    A[i][edge[1]] = -1
  
  solver = linprog(c, A_ub = A, b_ub = [-1 for edge in G.edges()], \
                        bounds = [0, len(G.nodes) + 1])
  
  nodes_layer = [round(x) for x in solver.x]
  nodes_layer = [x - min(nodes_layer) for x in nodes_layer] 
  layers = [[] for i in range(max(nodes_layer) + 1)]
  for node, id in enumerate(nodes_layer):
    layers[id].append(node)
  return layers

def FindFinishLayer(layers, end_node):
  for i, layer in enumerate(layers):
    for node in layer:
        if node == end_node:
          return i
  
def AddDummyNodes(G, layers):
  long_edges = {}
  for i in range(len(layers) - 1):
    for node in layers[i]:
      for edge in G.edges(node):
        if edge[1] not in layers[i + 1]:
          long_edges[edge] = i

  dummy_nodes = []
  dummy_edges = []
  new_node = max(G.nodes()) + 1
  for edge, begin_layer in long_edges.items():
    prev_node = edge[0]
    end_layer = FindFinishLayer(layers, edge[1])
    while begin_layer != end_layer - 1:
      dummy_nodes.append(new_node)
      dummy_edges.append([prev_node, new_node])
      G.add_node(new_node)
      G.add_edge(prev_node, new_node)
      begin_layer += 1
      layers[begin_layer].append(new_node)
      prev_node = new_node
      new_node += 1
    dummy_edges.append([new_node - 1, edge[1]])
    G.add_edge(new_node - 1, edge[1])
    G.remove_edge(*edge)

  return dummy_nodes, dummy_edges

def Sort2Layers(G, prev_layer, curr_layer):
  edges = [edge for node in prev_layer for edge in G.edges(node)]
  edges = sorted(edges, key = lambda x : prev_layer.index(x[0]))
  sort_nodes = [edge[::-1][0] for edge in edges]
  sort_nodes = sort_nodes + [node for node in curr_layer if node not in sort_nodes]
  curr_layer = sorted(curr_layer, key=lambda x: sort_nodes.index(x))
  return curr_layer

def SortLayers(G, layers):
  new_layers = layers
  for _ in range(len(layers) - 1):
    old_layers = [new_layers[0]]
    for i in range(len(layers) - 1):
      old_layers.append(Sort2Layers(G, new_layers[i], new_layers[i + 1]))
    new_layers = old_layers
  return new_layers

def DrawGraph(filename, W = 0):
  G = nx.convert_node_labels_to_integers(nx.read_graphml(filename))
  layers = CoffmanGrahamLayering(G, W) if W else LinprogLayering(G)

  colors = {}
  for i, layer in enumerate(layers):
    for node in layer:
      colors[node] = i
  
  init_nodes = cp.deepcopy(G.nodes())
  dummy_nodes, dummy_edges = AddDummyNodes(G, layers)

  sorted_layers = SortLayers(G, layers)
  
  pos = {}
  y = 0
  for layer in sorted_layers:
    mid = - len(layer) / 2
    x = mid + 0.5 if len(layer) % 2 == 0 else mid
    for node in layer:
      pos[node] = (x, y)
      x += 1
    y -= 1

  sorted_colors = [item[1] for item in sorted(colors.items(), key=lambda x: x[0])]
  nx.draw_networkx_nodes(G, pos, node_size=50, \
          cmap=plt.cm.summer, \
          node_color=sorted_colors, \
          nodelist=init_nodes, \
          edgecolors=np.array((0.0, 0.0, 0.0)).reshape(1, -1))
  nx.draw_networkx_nodes(G, pos, node_size=0, \
          nodelist=dummy_nodes)
  nx.draw_networkx_edges(G, pos, node_size=0, \
          arrowstyle='-|>')
  
  plt.gca().set_aspect("equal")
  plt.savefig('result_W=' + str(W) + '.png')
  plt.show()

if __name__ == '__main__':
  DrawGraph('flow.xml', 2)
  DrawGraph('flow.xml')