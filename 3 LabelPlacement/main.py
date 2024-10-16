#                       Задание 3: Расположение меток/подписей
# На входе алгоритма набор пар целочисленных координат точек от 0 до 500,
# а также для каждой точки размеры подписи к ней (два целых числа — ширина и высота рамки подписи) и
# некоторое подмножество возможных расположений подписи.

# На выходе — картинка с точками и неперекрывающимися метками (в частности, не выходящими за пределы холста 500×500)
# либо указание, что такое расположение недостижимо.


# input file description - x y w h
#   x - x coord of dot
#   y - y coord of dot
#   w - w width of rectangle
#   h - h height of rectangle

# possible positions of dot:
#   top left
#   bottom mid
#   center

import copy as cp
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def CheckBoundsIntersect(pos):
  if pos[0] > 500 or pos[1] > 500 \
  or pos[0] < 0 or pos[1] < 0 \
  or pos[0] + pos[2] > 500 or pos[1] - pos[3] > 500:
    return False
  return True

def CheckPosition(description, pos):
  normalized_position = cp.deepcopy(description)
  if pos == 2:
    normalized_position[0] = description[0] - description[2] / 2
    normalized_position[1] = description[1] + description[3]
  if pos == 3:
    normalized_position[0] = description[0] - description[2] / 2
    normalized_position[1] = description[1] + description[3] / 2
  return normalized_position if CheckBoundsIntersect(normalized_position) else 0

def AtLeastOneClauses(description):
  clauses = []
  for rect_num, descr in enumerate(description):
    clause = []
    if CheckPosition(descr, 1): clause.append(rect_num * 3 + 1)
    if CheckPosition(descr, 2): clause.append(rect_num * 3 + 2)
    if CheckPosition(descr, 3): clause.append(rect_num * 3 + 3)
    if not clause:
      print("Impossible to draw such rectangles in 500x500 frame")
      exit(0)
    clauses.append(clause)
  return clauses

def IntersectRectangles(pos1, pos2):
  if \
  pos1[0] > pos2[0] + pos2[2] or \
  pos1[0] + pos1[2] < pos2[0] or \
  pos1[1] < pos2[1] - pos2[3] or \
  pos1[1] - pos1[3] > pos2[1]:
    return False
  else:
    return True

def IntersectionClauses(description):
  clauses = []
  for rect_num, descr in enumerate(description):
    for pos in [1, 2, 3]:
      normalized_position = CheckPosition(descr, pos)
      if normalized_position:
        for rect_num_neib, descr_neib in enumerate(description):
          if rect_num_neib != rect_num:
            normalized_position_neib = CheckPosition(descr_neib, 1)
            if normalized_position_neib and \
              IntersectRectangles(normalized_position, normalized_position_neib):
                clauses.append([-(rect_num * 3 + pos), -(rect_num_neib * 3 + 1)])
            normalized_position_neib = CheckPosition(descr_neib, 2)
            if normalized_position_neib and \
              IntersectRectangles(normalized_position, normalized_position_neib):
                clauses.append([-(rect_num * 3 + pos), -(rect_num_neib * 3 + 2)])
            normalized_position_neib = CheckPosition(descr_neib, 3)
            if normalized_position_neib and \
              IntersectRectangles(normalized_position, normalized_position_neib):
                clauses.append([-(rect_num * 3 + pos), -(rect_num_neib * 3 + 3)])
  return clauses

def ReadInput(filename):
  f = open(filename + '.txt', 'r')
  description = [[int(x) for x in line.split()] for line in f]
  return description

def DrawRects(filename):
  description = ReadInput(filename)
  at_least_one_clauses = AtLeastOneClauses(description)
  intersection_clauses = IntersectionClauses(description)

  g = Glucose3()
  for clause in (at_least_one_clauses + intersection_clauses):
    g.add_clause(clause)
  res = g.solve()
  model = g.get_model()
  if res == False:
    print("Impossible to draw such rectangles without intersections")
    exit(0)

  plt.imshow(np.zeros((501, 501)), cmap='Greys')
  plt.gca().invert_yaxis()
  plt.gca().add_patch(Rectangle((0, 0), \
                  500, 500, linewidth=1, \
                  edgecolor=(0, 0, 0), facecolor='none'))
  clr = (104/255, 186/255, 79/255)
  for i, rect in enumerate(description):
    plt.plot(rect[0], rect[1], 'go', ms=4)
    if model[3 * i] > 0:
      plt.gca().add_patch(Rectangle((rect[0], rect[1] - rect[3]), \
                  rect[2], rect[3], linewidth=2, \
                  edgecolor=clr, facecolor='none'))
    elif model[3 * i + 2] > 0:
      plt.gca().add_patch(Rectangle((rect[0] - rect[2] / 2, rect[1] - rect[3] / 2), \
                  rect[2], rect[3], linewidth=2, \
                  edgecolor=clr, facecolor='none'))
    elif model[3 * i + 1] > 0:
      plt.gca().add_patch(Rectangle((rect[0] - rect[2] / 2, rect[1]), \
                  rect[2], rect[3], linewidth=2, \
                  edgecolor=clr, facecolor='none'))
    else:
      print("Impossible to draw such rectangles without intersections")
  plt.axis('off')
  plt.savefig(filename + '_result.png')
  plt.show()
  
  
  
if __name__ == '__main__':
  DrawRects("test4")
  DrawRects("test16")
  DrawRects("test")