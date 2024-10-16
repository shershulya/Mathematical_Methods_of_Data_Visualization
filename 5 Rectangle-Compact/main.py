# Задание 5: Реализцаия Tidy-Rectangle-Compact алгоритма

# Входные данные: встроенный планарный граф G с n вершинами максимальной степени четыре;
# ортогональное представление H из G, такое, что все грани имеют прямоугольную форму.

# Результат: чертеж планарной ортогональной сетки Г из G с ортогональным представлением H и 
# минимальной высотой, шириной, площадью и общей длиной ребёр.

import matplotlib.pyplot as plt
from collections import deque

class Rectangle:
  def __init__(self, id, top, left, bottom, right):
    self.id = id
    self.top = top
    self.left = left
    self.bottom = bottom
    self.right = right
    self.width = right - left
    self.height = top - bottom
    self.drawn = False

class Edge:
  def __init__(self, to, cap, flow, link):
    self.to = to
    self.cap = cap
    self.flow = flow
    self.link = link
    

class Graph:
  def __init__(self, N, S, T):
    self.N = N
    self.S = S
    self.T = T
    self.level = [0 for _ in range(N)]
    self.queue = [0 for _ in range(N)]
    self.head = [-1 for _ in range(N)]
    self.edges = []
    self.stack = deque()

  def AddEdge(self, a, b, cap):
    e1 = Edge(b, cap, 0, self.head[a])
    self.head[a] = len(self.edges)
    self.edges.append(e1)
    
  def AddEdges(self, a, b, cap,):
    e1 = Edge(b, cap, 0, self.head[a])
    e2 = Edge(a, 0, 0, self.head[b])
    self.head[a] = len(self.edges)
    self.edges.append(e1)
    self.head[b] = len(self.edges)
    self.edges.append(e2)

  def BFS(self):
    self.level = [-1 for _ in range(self.N)]
    self.level[self.S] = 0
    q_curr = 0
    q_new = 1
    self.queue[0] = self.S
    while (q_curr < q_new and self.level[self.T] == -1):
      v = self.queue[q_curr]
      q_curr += 1
      id = self.head[v]
      while id != -1:
        e = self.edges[id]
        to = e.to
        id = e.link
        if self.level[to] == -1 and e.flow < e.cap:
          self.level[to] = self.level[v] + 1
          self.queue[q_new] = to
          q_new += 1
          
    return self.level[self.T] != -1
 
  def DFS(self, v, flow):
    if not flow:
      return 0
    if v == self.T:
      return flow

    id = self.head[v]
    while id != -1:
      e = self.edges[id]
      to = e.to
      if self.level[to] != self.level[v] + 1:
        id = e.link
        continue
      pushed = self.DFS(to, min(flow, e.cap - e.flow))
      if pushed:
        self.edges[id].flow += pushed
        self.edges[id ^ 1].flow -= pushed
        return pushed
      id = e.link
    return 0

  def Dinic(self):
    if self.S == self.T:
      print("Incorrect max flow params")
      return -1
    flow = 0
    while self.BFS():
      while pushed := self.DFS(self.S, float('inf')):
        flow += pushed
    return flow

  def ReadStack(self):
    if not self.stack:
      return
    x = self.stack.pop()
    self.ReadStack()
    self.stack.append(x)
    self.edges[x].cap += 1
    return

  def FindAllPathsFromS2T(self, v):
    if v == self.T:
      self.ReadStack()
      self.stack.pop()
      return
  
    id = self.head[v]
    while id != -1:
      e = self.edges[id]
      self.stack.append(id)
      to = e.to
      self.FindAllPathsFromS2T(to)
      id = e.link
  
    if self.stack:
      self.stack.pop()
    return

  def FindMinFlow(self):
    self.FindAllPathsFromS2T(self.S)
    max_flow_graph_vert = Graph(self.N, self.S, self.T)
    from_v = [-1 for _ in range(len(self.edges))]
    for i in range(self.N):
      id = self.head[i]
      while id != -1:
        from_v[id] = i;
        id = self.edges[id].link
  
    for i in range(len(self.edges)):
      max_flow_graph_vert.AddEdges(from_v[i], self.edges[i].to, self.edges[i].cap - 1)
  
    max_flow_graph_vert.Dinic()
  
    for i in range(len(self.edges)):
      self.edges[i].flow = self.edges[i].cap - max_flow_graph_vert.edges[i * 2].flow
    return

  def GetSizesBFS(self, rectangles, dim):
    self.level = [-1 for _ in range(self.N)]
    self.level[self.S] = 0
    q_curr = 0
    q_new = 1
    self.queue[0] = self.S
    while (q_curr < q_new):
      v = self.queue[q_curr]
      q_curr += 1
      id = self.head[v]
      size = 0
      while id != -1:
        e = self.edges[id]
        to = e.to
        id = e.link
        size += e.flow
        if self.level[to] == -1:
          self.level[to] = self.level[v] + 1
          self.queue[q_new] = to
          q_new += 1
        if v != self.S and v != self.T:
          if dim == 'width':
            rectangles[v - 1].width = size
          else:
            rectangles[v - 1].height = size
    return

def PrintResult(filename, rectangles, canvas_border_b, canvas_border_l):
  fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(9, 4.5))
  ax[0].set_title("Source graph")
  for rect in rectangles:
    ax[0].plot([rect.left, rect.right], [rect.top, rect.top], color='0', marker = 'o')
    ax[0].plot([rect.left, rect.right], [rect.bottom, rect.bottom], color='0', marker = 'o')
    ax[0].plot([rect.left, rect.left], [rect.top, rect.bottom], color='0', marker = 'o')
    ax[0].plot([rect.right, rect.right], [rect.top, rect.bottom], color='0', marker = 'o')
  
  new_rectangles = []
  for i in range(len(rectangles)):
    new_rectangles.append(rectangles[i])

  cnt = len(rectangles)
  while cnt > 0:
    for rect_i, rect_candidate in enumerate(rectangles):
      if not rect_candidate.drawn:
        
        left_border = canvas_border_l
        for i, rect_left in enumerate(rectangles):
          if rect_left.drawn and rect_left.right == rect_candidate.left:
            left_border = new_rectangles[i].right
            break
        if left_border == canvas_border_l and rect_candidate.left != canvas_border_l:
          continue
          
        bottom_border = canvas_border_b
        for i, rect_bottom in enumerate(rectangles):
          if rect_bottom.drawn and rect_bottom.top == rect_candidate.bottom:
            bottom_border = new_rectangles[i].top
            break
        if bottom_border == canvas_border_b and rect_candidate.bottom != canvas_border_b:
          continue

        rect_candidate.drawn = True
        cnt -= 1
        new_rectangles[rect_i] = Rectangle(rect_candidate.id, \
                                          bottom_border + rect_candidate.height, \
                                          left_border, \
                                          bottom_border, \
                                          left_border + rect_candidate.width
                                         )

  ax[1].set_title("Result compact graph")
  for rect in new_rectangles:
    ax[1].plot([rect.left, rect.right], [rect.top, rect.top], color='0', marker = 'o')
    ax[1].plot([rect.left, rect.right], [rect.bottom, rect.bottom], color='0', marker = 'o')
    ax[1].plot([rect.left, rect.left], [rect.top, rect.bottom], color='0', marker = 'o')
    ax[1].plot([rect.right, rect.right], [rect.top, rect.bottom], color='0', marker = 'o')
  
  plt.savefig("result_" + filename + ".png")
  plt.show()
  
def TidyRectangleCompact(filename):
  # Rectangles stored in format: id top left bottom right
  rectangles = []
  with open(filename + '.txt') as file:
    lines = file.readlines()
    for line in lines:
      id, top, left, bottom, right = map(float, line.split())
      rect = Rectangle(int(id), top, left, bottom, right)
      rectangles.append(rect)

  s = 0
  n = len(rectangles)
  t = n + 1
  canvas_border_t = max([rect.top for rect in rectangles])
  canvas_border_l = min([rect.left for rect in rectangles])
  canvas_border_b = min([rect.bottom for rect in rectangles])
  canvas_border_r = max([rect.right for rect in rectangles])

  # Build and compute min flow in vertical network
  g_vert = Graph(n + 2, s, t)
  for i in range(n):
    for j in range(i, n):
      if rectangles[i].top == rectangles[j].bottom and \
        not (rectangles[i].left > rectangles[j].right or \
        rectangles[j].left > rectangles[i].right):
        g_vert.AddEdge(rectangles[i].id, rectangles[j].id, 0)
      if rectangles[i].bottom == rectangles[j].top and \
        not (rectangles[i].left > rectangles[j].right or \
        rectangles[j].left > rectangles[i].right):
        g_vert.AddEdge(rectangles[j].id, rectangles[i].id, 0)
    if rectangles[i].top == canvas_border_t:
      g_vert.AddEdge(rectangles[i].id, t, 0)
    if rectangles[i].bottom == canvas_border_b:
      g_vert.AddEdge(s, rectangles[i].id, 0)

  g_vert.FindMinFlow()

  # Build and compute min flow in horizontal network
  g_hor = Graph(n + 2, s, t)
  for i in range(n):
    for j in range(i, n):
      if rectangles[i].right == rectangles[j].left and \
        not (rectangles[i].bottom > rectangles[j].top or \
        rectangles[j].bottom > rectangles[i].top):
        g_hor.AddEdge(rectangles[i].id, rectangles[j].id, 0)
      if rectangles[i].left == rectangles[j].right and \
        not (rectangles[i].bottom > rectangles[j].top or \
        rectangles[j].bottom > rectangles[i].top):
        g_hor.AddEdge(rectangles[j].id, rectangles[i].id, 0)
    if rectangles[i].right == canvas_border_r:
      g_hor.AddEdge(rectangles[i].id, t, 0)
    if rectangles[i].left == canvas_border_l:
      g_hor.AddEdge(s, rectangles[i].id, 0)

  g_hor.FindMinFlow()
  
  # Get new height and width in each rectangle by the minimum flow
  g_hor.GetSizesBFS(rectangles, "height")
  g_vert.GetSizesBFS(rectangles, "width")
  PrintResult(filename, rectangles, canvas_border_b, canvas_border_l)

if __name__ == "__main__":
  TidyRectangleCompact("rectangle_test1")
  TidyRectangleCompact("rectangle_test2")