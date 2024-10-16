#include <iostream>
#include <iomanip>
#include <vector>
#include <cstring>

#include<bits/stdc++.h>

const int INF = 1000; // константа-бесконечность

struct Edge {
  int to, cap, flow, link;
};

class Graph
{
public:
    int n, s, t; // number of vertex
    int *level, *queue, *head; // stores level of a node
    std::vector<Edge> edges;
    std::stack<int> stack;
public:
    Graph(int n, int s, int t)
    {
        this->n = n;
        this->s = s;
        this->t = t;
        level = new int[n];
        queue = new int[n];
        head = new int[n];
        memset (head, -1, n * sizeof(int));
    }
 
    // add edge to the graph
    void AddEdges (int a, int b, int cap) {
      Edge e1 = { b, cap, 0, head[a] };
      Edge e2 = { a, 0, 0, head[b] };

      head[a] = (int) edges.size();
      edges.push_back (e1);

      head[b] = (int) edges.size();
      edges.push_back (e2);
    }

    void AddEdge (int a, int b, int cap) {
      Edge e1 = { b, cap, 0, head[a] };

      head[a] = (int) edges.size();
      edges.push_back (e1);
    }
 
    bool BFS();
    int DFS(int v, int flow);
    int Dinic();
    int MinCostFlow();
    int MyDFS(int v);
    int MinFlow();
    void ReadStack();
};

bool Graph::BFS() {
  int q_curr_v = 0, q_new_v = 0;
  queue[q_new_v++] = s;
  memset (level, -1, n * sizeof(level[0]));
  level[s] = 0;
  while (q_curr_v < q_new_v && level[t] == -1) {
    int v = queue[q_curr_v++];
    int id = head[v];
    while (id != -1) {
      Edge e = edges[id];
      int to = e.to;
      id = e.link;
      if (level[to] == -1 && e.flow < e.cap) {
        queue[q_new_v++] = to;
        level[to] = level[v] + 1;
      }
    }
  }
  return level[t] != -1;
}

int Graph::DFS (int v, int flow) {
  if (!flow)  return 0;
  if (v == t)  return flow;

  int id = head[v];
  while (id != -1) {
    // std::cout << "v: " << v << ", id: " << id << std::endl;
    Edge e = edges[id];


    int to = e.to;
    if (level[to] != level[v] + 1) {
      id = e.link;
      continue;
    }
    int pushed = DFS(to, std::min(flow, e.cap - e.flow));
    if (pushed) {
      edges[id].flow += pushed;
      edges[id ^ 1].flow -= pushed;
      // std::cout << "e: " << e.flow << ", e_rev: " << e_rev.flow << ", pushed: " << pushed << std::endl;
      return pushed;
    }
    id = e.link;
  }
  return 0;
}

void Graph::ReadStack()
{
    if(stack.empty())
    {
        std::cout << std::endl;
        return;
    }
    int x = stack.top();
    stack.pop();
    ReadStack();
    stack.push(x);
    std::cout << x << " ";
    edges[x].cap += 1;
    return;
 }

int Graph::MyDFS (int v) {
  if (v == t) {
    ReadStack();
    stack.pop();
    return 0;
  }

  int id = head[v];
  
  while (id != -1) {
    Edge e = edges[id];
    stack.push(id);
    int to = e.to;
    MyDFS(to);
    id = e.link;
  }

  if (v == s) {
    std::cout << std::endl << "Edges: ";
    for (size_t i = 0; i < edges.size(); ++i) {
        std::cout << std::setw(2) << i << " ";
    }
    std::cout << std::endl;
    std::cout << "Capss: ";
    for (size_t i = 0; i < edges.size(); ++i) {
        std::cout << std::setw(2) << edges[i].cap << " ";
    }
    std::cout << std::endl;
  }
  stack.pop();
  return 0;
}

int Graph::Dinic() {
  int flow = 0;
  // std::cout << "Nums: ";
  // for (int i = 0; i < n; ++i) {
  //   std::cout << std::setw(2) << i << " ";
  // }
  // std::cout << std::endl;

  // std::cout << "Head: ";
  // for (int i = 0; i < n; ++i) {
  //   std::cout << std::setw(2) << head[i] << " ";
  // }
  // std::cout << std::endl;


  // std::cout << "Edges: ";
  // for (size_t i = 0; i < edges.size(); ++i) {
  //   std::cout << std::setw(2) << i << " ";
  // }
  // std::cout << std::endl;

  // std::cout << "Capss: ";
  // for (size_t i = 0; i < edges.size(); ++i) {
  //     std::cout << std::setw(2) << edges[i].cap << " ";
  // }
  // std::cout << std::endl;

  // std::cout << "Links: ";
  // for (size_t i = 0; i < edges.size(); ++i) {
  //   std::cout << std::setw(2) << edges[i].link << " ";
  // }
  // std::cout << std::endl;



  while (true) {
    if (!BFS())
      break;
    while (int pushed = DFS(s, INT_MAX)) {
      std::cout << pushed << std::endl;
      flow += pushed;
    }
  }

  std::cout << "Flows Dinic: ";
  for (size_t i = 0; i < edges.size(); ++i) {
    std::cout << std::setw(2) << edges[i].flow << " ";
  }
  std::cout << std::endl;

  return flow;
}

int main (int argc, char **argv) {
  int s = 0;
  int t = 11;
  int n = 12;

  Graph g(n, s, t);
  int a, b;
  while (std::cin >> a >> b) {
    // std::cout << a << " " << b << std::endl;
    g.AddEdge(a, b, 0);
  }

  g.MyDFS(s);

  Graph g_final(n, s, t);

  std::vector<int> from(g.edges.size());
  for (int i = 0; i < n; ++i) {
    int id = g.head[i];
    while (id != -1) {
      from[id] = i;
      id = g.edges[id].link;
    }
  }
  for (size_t i = 0; i < g.edges.size(); ++i) {
    g_final.AddEdges(from[i], g.edges[i].to, g.edges[i].cap - 1);
  }

  int flow = g_final.Dinic();
  std::cout << "Flow: " << flow << std::endl;


  for (size_t i = 0; i < g.edges.size(); ++i) {
    g.edges[i].flow = g.edges[i].cap - g_final.edges[i * 2].flow;
  }

  std::cout << "Flows: ";
  for (size_t i = 0; i < g.edges.size(); ++i) {
    std::cout << std::setw(2) << g.edges[i].flow << " ";
  }
  std::cout << std::endl;
  return 0;
}


















// int Graph::MinCostFlow() {


//   std::cout << "Nums: ";
//   for (int i = 0; i < n; ++i) {
//     std::cout << std::setw(2) << i << " ";
//   }
//   std::cout << std::endl;

//   std::cout << "Head: ";
//   for (int i = 0; i < n; ++i) {
//     std::cout << std::setw(2) << head[i] << " ";
//   }
//   std::cout << std::endl;


//   std::cout << "Edges: ";
//   for (size_t i = 0; i < edges.size(); ++i) {
//     std::cout << std::setw(2) << i << " ";
//   }
//   std::cout << std::endl;

//   std::cout << "Links: ";
//   for (size_t i = 0; i < edges.size(); ++i) {
//     std::cout << std::setw(2) << edges[i].link << " ";
//   }
//   std::cout << std::endl;


//   int flow = 0,  cost = 0;
//   while (flow < k) {
//     std::vector<int> id (n, 0);
//     std::vector<int> d (n, INF);
//     std::vector<int> q (n);
//     std::vector<int> p (n);
//     std::vector<size_t> p_rib (n);
//     int qh=0, qt=0;
//     q[qt++] = s;
//     d[s] = 0;
//     while (qh != qt) {
//       int v = q[qh++];
//       id[v] = 2;
//       if (qh == n)  qh = 0;
//       // for (size_t i=0; i<g[v].size(); ++i) {
//       int ids = head[v];
//       while (ids != -1) {
//         // rib & r = g[v][i];
//         Edge &r = edges[ids];
//         if (r.flow < r.cap && d[v] + r.cost < d[r.to]) {
//           d[r.to] = d[v] + r.cost;
//           if (id[r.to] == 0) {
//             q[qt++] = r.to;
//             if (qt == n)  qt = 0;
//           }
//           else if (id[r.to] == 2) {
//             if (--qh == -1)  qh = n-1;
//             q[qh] = r.to;
//           }
//           id[r.to] = 1;
//           p[r.to] = v;
//           p_rib[r.to] = ids;
//         }
//         ids = r.link;
//       }
//     }

//     // std::cout << "Dist: ";
//     // for (int i = 0; i < n; ++i) {
//     //   std::cout << std::setw(2) << d[i] << " ";
//     // }
//     // std::cout << std::endl;

//     if (d[t] == INF) {
//       std::cout << "here" << std::endl;
//       break;
//     }
//     int addflow = k - flow;
//     for (int v = t; v != s; v = p[v]) {
//       int pv = p[v];
//       size_t pr = p_rib[v];

//       size_t ids = head[pv];
//       Edge es = edges[ids];
//       while (ids != pr) {
//         ids = es.link;
//         es = edges[ids];
//       }
//       // addflow = min(addflow, g[pv][pr].u - g[pv][pr].f);
//       addflow = std::min(addflow, es.cap - es.flow);
//     }
//     for (int v = t; v != s; v = p[v]) {
//       int pv = p[v];
//       size_t pr = p_rib[v];

//       size_t r = pr + 1;
//       // size_t r = g[pv][pr].back;

//       size_t ids = head[pv];
//       Edge es = edges[ids];
//       while (ids != pr) {
//         ids = es.link;
//         es = edges[ids];
//       }

//       edges[ids].flow += addflow;
//       cost += edges[ids].cost * addflow;
      
//       ids = head[v];
//       es = edges[ids];
//       while (ids != r) {
//         ids = es.link;
//         es = edges[ids];
//       }

//       edges[ids].flow -= addflow;


//       // g[pv][pr].f += addflow;
//       // g[v][r].f -= addflow;
//       // cost += g[pv][pr].c * addflow;
//     }
//     flow += addflow;
//   }

//   std::cout << "Flows: ";
//   for (size_t i = 0; i < edges.size(); ++i) {
//     std::cout << std::setw(2) << edges[i].flow << " ";
//   }
//   std::cout << std::endl;

//   std::cout << "Cost: " << cost << std::endl;
//   return flow;
// }