import os
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt

def draw_graph(min_node_visit=10, min_edge_visit=10):
    
    NODE_DATA_FILE_NAME = "./out/stats/count_screenclass_type.csv"
    EDGE_DATA_FILE_NAME = "./out/stats/count_screenclass_series_2.csv"
    
    G = nx.DiGraph()

    data_nodes = pd.read_csv(NODE_DATA_FILE_NAME, keep_default_na=False, na_values="-", index_col=0)
    df_nodes = pd.DataFrame(data_nodes)
    labels = df_nodes.index.tolist()
    node_cnt = len(labels)
    for i in range(node_cnt):
        visit = df_nodes.iloc[i].sum()
        node = labels[i]
        G.add_node(node, visit=visit, edge_count=0)

    data_edges = pd.read_csv(EDGE_DATA_FILE_NAME, keep_default_na=False, na_values="-", index_col=0)
    df_edges = pd.DataFrame(data_edges)
    paths = df_edges.index.tolist()
    edge_cnt = len(paths)
    for i in range(edge_cnt):
        visit = df_edges.iloc[i].sum()
        node_A, node_B = paths[i].split("-")
        G.add_edge(node_A, node_B, visit=visit)
        
        G.nodes[node_A]["edge_count"] += 1
        G.nodes[node_B]["edge_count"] += 1
        
    # 데이터가 너무 적은 노드 및 간선 삭제
    remove_nodes = []
    for node, data in G.nodes(data=True):
        if data["visit"] < min_node_visit:
            remove_nodes.append(node)
    G.remove_nodes_from(remove_nodes)
    remove_edges = []
    for u, v, data in G.edges(data=True):
        if data["visit"] < min_edge_visit:
            remove_edges.append((u,v))
    G.remove_edges_from(remove_edges)

    # 노드 및 간선 속성 설정
    node_colors = [data["visit"]/10 + 10 for label, data in G.nodes(data=True)]
    node_sizes = [data["visit"]*15 + 5 for label, data in G.nodes(data=True)]
    
    edge_colors = [data["visit"]/10 + 10 for u, v, data in G.edges(data=True)]
    edge_widths = [data["visit"]/15 + 1 for u, v, data in G.edges(data=True)]

    # 그래프 그리기
    
    # options = {
    #     "arrowstyle": "-|>",
    #     "arrowsize": 5,
    #     "node_color": "lightblue",
    #     "with_labels": True,
    #     "node_shape": "o",
    #     "font_size": 8,
    #     "alpha": 0.7,
    # }
    
    plt.figure(figsize=(18,13))
    pos = nx.kamada_kawai_layout(G)  # 레이아웃 설정
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.7, cmap=plt.cm.Blues)
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.7, edge_cmap=plt.cm.Greys)
    nx.draw_networkx_labels(G, pos)

    # 그래프 저장
    PNG_FILE_NAME = "foo000"
    i = 0
    while f"{PNG_FILE_NAME}.png" in os.listdir("./out/image"):
        i += 1
        PNG_FILE_NAME = "foo" + str(i).zfill(3)
    plt.savefig(f"./out/image/{PNG_FILE_NAME}.png")

    print(f"Done generating ./out/image/{PNG_FILE_NAME}.png")