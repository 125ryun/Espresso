import os
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

G = nx.DiGraph()

data_nodes = pd.read_csv("./out/stats/count_screenclass_type.csv", keep_default_na=False, na_values="-", index_col=0)
df_nodes = pd.DataFrame(data_nodes)

visits = []
for row in df_nodes.iloc:
    visit = row.sum()
    visits.append(visit)
df_nodes["visits"] = visits

labels = df_nodes.index.tolist()
node_sizes = [3 + visit/10 for visit in visits]

for i in range(len(labels)):
    if visit > 0:
        G.add_node(labels[i], size=visits[i], edge_count=0)

data_edges = pd.read_csv("./out/stats/count_screenclass_series_2.csv", keep_default_na=False, na_values="-", index_col=0)
df_edges = pd.DataFrame(data_edges)

nodes = df_edges.index.tolist()
weighs = []
for i, row in enumerate(df_edges.iloc):
    weigh = row.sum()
    weighs.append(weigh)
    node = nodes[i].split("-")
    G.nodes[node[0]]['edge_count'] += 1
    G.nodes[node[1]]['edge_count'] += 1
df_edges["weighs"] = weighs
print(df_edges)
df_edges.drop(df_edges[df_edges["weighs"]<10].index, axis=0, inplace=True)
weighs = df_edges["weighs"].tolist()

u_v = [(n1_n2.split("-")[0],n1_n2.split("-")[1]) for n1_n2 in df_edges.index.tolist()]

for i in range(len(u_v)):
    G.add_edge(u_v[i][0], u_v[i][1], weight = weighs[i])

# 노드 및 간선 속성 설정
node_sizes = [data['size'] * 5 + 10 for node, data in G.nodes(data=True) if data['edge_count'] > 10]
edge_widths = [data['weight']/25+1 for u, v, data in G.edges(data=True)]
edge_alphas = [data['weight'] for u, v, data in G.edges(data=True)]

# 그래프 그리기
plt.figure(figsize=(18,13))
pos = nx.fruchterman_reingold_layout(G, k=1.5)  # 레이아웃 설정
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='gray', alpha=0.5, nodelist=[node for node, data in G.nodes(data=True) if data['size'] > 0 and data['edge_count'] > 50],)
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='blue', alpha=0.5)
nx.draw_networkx_labels(G, pos)

# 그래프 저장
PNG_FILE_NAME = "foo000"
i = 0
while f"{PNG_FILE_NAME}.png" in os.listdir("./out/image"):
    i += 1
    PNG_FILE_NAME = "foo" + str(i).zfill(3)
plt.savefig(f"./out/image/{PNG_FILE_NAME}.png")

print(f"Done generating ./out/image/{PNG_FILE_NAME}.png")

# plt.savefig("image.png")
# plt.show()
exit(1)
'''
edge_alphas = [1-1/weigh for weigh in weighs]


edges = [(node[0],node[1],weighs[i]) for i, node in enumerate(u_v)]

G.add_weighted_edges_from(edges)
'''

'''
for (u, v, w) in edges:
    G.add_edge(u,v, weighs=w*10)
    
options = {
    "arrowsize": 5,
    "with_labels": True,
    "node_size": 200,
    "node_color": "lightgray", 
    "node_shape": "o", 
    "alpha": 0.5, 
    "edge_color": "red",
    "font_size": 8,
}

# nx.draw(G, **options, pos=nx.drawing.nx_agraph.graphviz_layout(G, prog='dot'))
    
pos = nx.fruchterman_reingold_layout(G)
# nx.draw(G, with_labels=True, node_size=80, font_size=10, arrowsize=10)
nx.draw(G, **options)
'''

#################################
plt.figure(figsize=(10, 7))
# node_color = [0.01 * v for v in visits]
node_size = [0.0005 * v for v in visits]
edge_width = [0.0015 * s for s in weighs]
options = {
    "arrowstyle": "-|>",
    "arrowsize": 5,
    "node_color": "lightblue",
    "with_labels": True,
    "node_shape": "o",
    "font_size": 8,
    "alpha": 0.7,
}
nx.draw(G, **options, node_size = node_size, width = edge_width)
#################################

PNG_FILE_NAME = "foo000"
i=0
if not os.path.exists("./out/image"):
    os.mkdir("./out/image")
while f"{PNG_FILE_NAME}.png" in os.listdir("./out/image"):
    PNG_FILE_NAME = "foo" + str(i).zfill(3)
    i += 1
plt.savefig(f"./out/image/{PNG_FILE_NAME}.png")

print(f"Done generating ./out/image/{PNG_FILE_NAME}.png")