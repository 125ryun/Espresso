import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

data = pd.read_csv("./out/stats/count_screenclass_type.csv", keep_default_na=False, na_values="-", index_col=0)
df = pd.DataFrame(data)

labels = df.index.tolist()
visits = []
for row in df.iloc:
    visit = row.sum()
    visits.append(visit)
nodes = []

data = pd.read_csv("./out/stats/count_screenclass_series_2.csv", keep_default_na=False, na_values="-", index_col=0)
df = pd.DataFrame(data)

u_v = [(n1_n2.split("-")[0],n1_n2.split("-")[1]) for n1_n2 in df.index.tolist()]
print(u_v)
exit(1)
u_v = df.index.tolist()
weighs = []
# for i in range(df.shape[0]):
for row in df.iloc:
    # weigh = df.iloc[i].sum()
    weigh = row.sum()
    weighs.append(weigh)
edges = [(node.split("-")[0],node.split("-")[1],weighs[i]) for i, node in enumerate(u_v)]

G = nx.DiGraph()
# G.add_weighted_edges_from(edges)
for (u, v, w) in edges:
    G.add_edge(u,v, minlen=w*100, width=w)
    
nx.draw(G, pos=nx.drawing.nx_agraph.graphviz_layout(G, prog='dot'))
    
# pos = nx.fruchterman_reingold_layout(G)
# nx.draw(G, with_labels=True, node_size=80, font_size=10, arrowsize=10)

PNG_FILE_NAME = "foo"
i=0
if not os.path.exists("./image"):
    os.mkdir("./image")
while f"{PNG_FILE_NAME}.png" in os.listdir("./image"):
    PNG_FILE_NAME = "foo" + str(i).zfill(3)
    i += 1
plt.savefig(f"./image/{PNG_FILE_NAME}.png")