#                         Задание 4: Визуализация многомерных данных
# Реализуйте один из алгоритмов LLE, IsoMap, t-SNE для визуализации многомерных данных.

import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import make_s_curve
from scipy import linalg
from scipy.sparse import csgraph


def ToroidalHelix(n_samples=100,
                   rad_out=2,
                   rad_in=0.5,
                   n_turns=10,
                   random_state=None,
                   noise=0.0):
    from numpy import linspace, zeros, sin, cos, pi, random
    random.seed(seed=random_state)
    t = linspace(-1, 1, n_samples)
    X = zeros((n_samples, 3))
    x = (rad_out + rad_in * cos(n_turns * pi * t)) * cos(pi * t)
    y = (rad_out + rad_in * cos(n_turns * pi * t)) * sin(pi * t)
    z = rad_in * sin(n_turns * pi * t)
    X[:, 0] = x + rad_in * random.normal(size=n_samples, scale=noise)
    X[:, 1] = y + rad_in * random.normal(size=n_samples, scale=noise)
    X[:, 2] = z + rad_in * random.normal(size=n_samples, scale=noise)
    return X, t


def EuclidDist(matrix):
    n, m = matrix.shape
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            quadr_diff = 0
            for k in range(m):
                quadr_diff += (matrix[i][k] - matrix[j][k])**2
            dist[i][j] = np.sqrt(quadr_diff)
            dist[j][i] = dist[i][j]
    return dist


def MakeAdjacency(data, eps):
    n, m = data.shape
    dist = EuclidDist(data)
    adj = np.zeros((n, n)) + np.inf
    threshold = dist < eps
    adj[threshold] = dist[threshold]
    short = csgraph.shortest_path(adj)
    return short


def Isomap(dist):
    n, m = dist.shape
    h = np.eye(n) - (1 / n) * np.ones((n, n))
    dist = dist**2
    c = -1 / (2 * n) * h.dot(dist).dot(h)
    evals, evecs = linalg.eig(c)
    idx = evals.argsort()[::-1]
    evals = evals[idx]
    evecs = evecs[:, idx]
    evals = evals[:2]
    evecs = evecs[:, :2]
    z = evecs.dot(np.diag(evals**(-1 / 2)))
    return z.real

def SCurveEmbedding(filename, noise=0.0):
    X_curve, color_curve = make_s_curve(n_samples=1500, noise=noise)

    print("Computing Isomap embedding for " + filename[:-4])
    X_iso = Isomap(MakeAdjacency(X_curve, 0.4))
    print("Done")

    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]})
    fig.set_size_inches(8, 8)

    ax[0].xaxis.set_visible(False)
    ax[0].yaxis.set_visible(False)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax[0].spines[spine].set_visible(False)
    ax3d = fig.add_subplot(211, projection="3d")
    ax3d.scatter(X_curve[:, 0], X_curve[:, 1], X_curve[:, 2], \
                 c=color_curve, cmap=plt.cm.jet)
    ax3d.view_init(4, -72)
    ax3d.set_box_aspect(aspect=None, zoom=1.4)
    ax3d.yaxis.set_ticks(np.arange(0, 2.1, 0.6))
    ax3d.set_title("Original data")

    ax2d = fig.add_subplot(212)
    ax2d.scatter(X_iso[:, 0], X_iso[:, 1], c=color_curve, cmap=plt.cm.jet)
    ax2d.set_title("Projected data")

    fig.suptitle("Isomap with S curve", fontsize=20)
    plt.xticks([]), plt.yticks([])
    plt.savefig(filename)
    plt.show()

def HelixEmbedding(filename, noise=0.0):
    X_helix, color_helix = ToroidalHelix(n_samples=500, noise=noise)

    print("Computing Isomap embedding for " + filename[:-4])
    X_iso = Isomap(MakeAdjacency(X_helix, 0.4))
    print("Done")

    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 1]})
    fig.set_size_inches(4, 8)

    ax[0].xaxis.set_visible(False)
    ax[0].yaxis.set_visible(False)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax[0].spines[spine].set_visible(False)
    ax3d = fig.add_subplot(211, projection="3d")
    ax3d.scatter(X_helix[:, 0], X_helix[:, 1], X_helix[:, 2], \
                 c=color_helix, cmap=plt.cm.jet)
    ax3d.view_init(35, -72)
    ax3d.set_box_aspect(aspect=None, zoom=1.3)
    ax3d.xaxis.set_ticks([])
    ax3d.set_title("Original data")

    ax2d = fig.add_subplot(212)
    ax2d.scatter(X_iso[:, 0], X_iso[:, 1], c=color_helix, cmap=plt.cm.jet)
    ax2d.set_title("Projected data")

    fig.suptitle("Isomap with Toroidal Helix", fontsize=20)
    plt.xticks([]), plt.yticks([])
    plt.savefig(filename)
    plt.show()


if __name__ == "__main__":
    SCurveEmbedding("S curve.png")
    SCurveEmbedding("S curve with noise.png", 0.1)

    HelixEmbedding("Toroidal Helix.png")
    HelixEmbedding("Toroidal Helix with noise.png", 0.1)
