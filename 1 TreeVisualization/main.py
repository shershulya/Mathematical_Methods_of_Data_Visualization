#                                Задание 1: Визуализация деревьев 
# Дерево задаётся как ориентированный граф, все рёбра которого ориентированы от корня к листьям. 
# Нужно реализовать укладку дерева с помощью HV-подхода

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def FindAspectRatio(G, h, w, root, max_h, max_w):
  if (not G[root]):
    return h, w, w
  for i, child in enumerate(G[root]):
    if (i == 0):
      tmp_h, tmp_w, w = FindAspectRatio(G, h + 1, w, child, max_h, max_w)
    else:
      tmp_h, tmp_w, w = FindAspectRatio(G, h, w + 1, child, max_h, max_w)
    if (tmp_h > max_h):
        max_h = tmp_h
    if (tmp_w > max_w):
      max_w = tmp_w
  return max_h, max_w, w

def DFS(G, h, w, root, pos, aspRat, colors, clr):
  pos[root] = (w, h)
  colors[int(root)] = clr
  for i, child in enumerate(G[root]):
    if (i == 0):
      w = DFS(G, h - aspRat, w, child, pos, aspRat, colors, clr + 1)
    else:
      w = DFS(G, h, w + 1, child, pos, aspRat, colors, clr + 1)
  return w
      

if __name__ == '__main__':
  G = nx.read_graphml('binary.xml')

  root = -1
  for node in G.nodes():
    if G.in_degree(node) == 0:
      root = node
  if (root == -1):
    print("Input graph has no root!")

  h, w, _ = FindAspectRatio(G, 0, 0, root, 0, 0)
  aspRat = (w + 1) / (h + 1)
  nodeSize = 50 * aspRat if aspRat > 1 else 50 / aspRat
  
  pos = {}
  colors = {}
  DFS(G, 0, 0, root, pos, aspRat, colors, 0)
  
  
  nx.draw(G, pos, node_size=nodeSize, \
          node_color=np.array((0.6, 0.8, 0.3)).reshape(1, -1), \
          edgecolors=np.array((0.0, 0.0, 0.0)).reshape(1, -1), \
          with_labels=False, \
          connectionstyle='arc3, rad = 0.1')
  plt.gca().set_aspect("equal")
  plt.savefig('result.png')
  plt.show()

  for verts in pos:
    x = pos[verts][0]
    y = pos[verts][1]
    pos[verts] = (x + y, -x + y)

  sorted_colors = [item[1] for item in sorted(colors.items(), key=lambda x: x[0])]
  nx.draw(G, pos, node_size=nodeSize, \
          cmap=plt.cm.summer, \
          node_color=sorted_colors, \
          edgecolors=np.array((0.0, 0.0, 0.0)).reshape(1, -1), \
          with_labels=False)
  plt.gca().set_aspect("equal")
  plt.savefig('rotated_result.png')
  plt.show()