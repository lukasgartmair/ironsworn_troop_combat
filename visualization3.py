import networkx as nx
import matplotlib.pyplot as plt

# # Combat dictionaries
close_combat_dict = {
    "skirmishers": {"skirmishers": 0, "warriors": -1, "archers": 2, "cavalry": -2},
    "warriors": {"skirmishers": 2, "warriors": 0, "archers": 3, "cavalry": -1},
    "cavalry": {"skirmishers": 2, "warriors": 1, "archers": 3, "cavalry": 0},
}

ranged_combat_dict = {
    "skirmishers": {"skirmishers": 0, "warriors": 1, "archers": -5, "cavalry": 1},
    "archers": {"skirmishers": 2, "warriors": 3, "archers": 0, "cavalry": 2},
}

# Relevant attributes per class
relevant_attributes = {
    "skirmishers": "heart",
    "warriors": "iron",
    "archers": "edge",
    "cavalry": "wits",
}

# Unit types
unit_types = {0: "skirmishers", 1: "warriors", 2: "archers", 3: "cavalry"}


# Set light grey background
plt.figure(figsize=(8, 8), facecolor='lightgrey')

# Draw the graph with the circular layout and edge colors based on weights
ax = plt.gca()  # Get current axes to modify background color
ax.set_facecolor('lightgrey')  # Set axis background to light grey
# Create directed graph
G = nx.DiGraph()

for unit1 in close_combat_dict:
    for unit2 in close_combat_dict[unit1]:
        if unit1 in close_combat_dict:
            if unit2 in close_combat_dict[unit1].keys():
                if close_combat_dict[unit1][unit2] != 0:
                    G.add_edge(unit1, unit2, weight=close_combat_dict[unit1][unit2])
        
        if unit2 in ranged_combat_dict:
            if unit1 in ranged_combat_dict[unit2].keys():
                if ranged_combat_dict[unit2][unit1] != 0:
                    G.add_edge(unit2, unit1, weight=ranged_combat_dict[unit2][unit1])

for unit1 in ranged_combat_dict:
    for unit2 in ranged_combat_dict[unit1]:
        if unit1 in ranged_combat_dict:
            if unit2 in ranged_combat_dict[unit1].keys():
                if ranged_combat_dict[unit1][unit2] != 0:
                    G.add_edge(unit1, unit2, weight=ranged_combat_dict[unit1][unit2])
        
        if unit2 in ranged_combat_dict:
            if unit1 in ranged_combat_dict[unit2].keys():
                if ranged_combat_dict[unit2][unit1] != 0:
                    G.add_edge(unit2, unit1, weight=ranged_combat_dict[unit2][unit1])


# Create the circular layout for node positions
pos = nx.spring_layout(G)

# Get the weights from the graph to apply colormap
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

# Normalize the weights to map to colormap
norm = plt.Normalize(vmin=-5, vmax=5)  # Normalizing based on your min and max values
cmap = plt.get_cmap("RdYlGn")  # Red to Yellow to Green colormap

# Map the edge weights to colors using the colormap
edge_colors = [cmap(norm(weight)) for weight in edge_weights]
edge_widths = [0.5 + abs(weight) * 0.5 for weight in edge_weights]  # Make edge width based on weight

nx.draw(G, pos, with_labels=True, width=edge_widths,edge_color=edge_colors,node_size=5000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True, arrowsize=20, 
        connectionstyle='arc3,rad=0.15')

# Add edge labels (weights), including negative weights
edge_labels = nx.get_edge_attributes(G, 'weight')

# # Add edge labels
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=30)

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14, 
                             verticalalignment="center", horizontalalignment="center", label_pos=0.25,
                             bbox=dict(facecolor='none', edgecolor='none', boxstyle="round,pad=0.3"))

plt.tight_layout()

plt.show()
