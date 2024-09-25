import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_edge(1, 3)
G.add_edge(1, 2)
pos = {1:[100, 120], 2:[200, 300], 3:[50, 75]}

fig = plt.figure(1)
img = mpimg.imread("image.jpg")
plt.imshow(img)
ax = fig.add_subplot(1, 1, 1)

nx.draw(G, pos=pos)

extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
plt.savefig('1.png', bbox_inches=extent)

plt.axis('off') 
plt.show()