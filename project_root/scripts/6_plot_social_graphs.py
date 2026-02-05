import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from utils.paths import (
    SOCIAL_ROLES_DIR,
)

from utils.translate import translate_category

# ======================================================
# Setup
# ======================================================

EDGE_COLORS = {
    "Agonista": "red",
    "Apaciguamiento": "green",
    "Afiliativa": "blue"
}

INDIVIDUAL_COLORS = {
    "N1": "#f1d5f5",
    "N2": "#9ed4e6",
    "N3": "#e6aa9e",
    "N4": "#97bfa8",
    "N5": "#a39a8b",
    "N6": "#7364b0",
    "N7": "#fffac4",
    "N8": "#7f7f7f"
}

NODE_SIZE = 900
EDGE_ALPHA = 0.85
EDGE_SCALE = 1 / 800

# Arrow behavior
ARROW_STYLE = "-|>"
ARROW_SIZE = 18
NODE_MARGIN = 18

# ======================================================
# LOAD DATA
# ======================================================

def load_data():
    edges = pd.read_csv(
        SOCIAL_ROLES_DIR / "directed_social_edges.csv"
    )
    ledger = pd.read_csv(
        SOCIAL_ROLES_DIR / "individual_social_ledgers.csv"
    )

    individuals = sorted(ledger["Individual"].unique())
    return edges, individuals

# ------------------------------------------------------------
# BUILD FIXED NODE POSITIONS
# ------------------------------------------------------------

def compute_node_positions(individuals, edges):
    G = nx.DiGraph()
    G.add_nodes_from(individuals)

    for _, row in edges.iterrows():
        G.add_edge(row["Source"], row["Target"])

    pos = nx.spring_layout(G, seed=42)
    return pos

# ------------------------------------------------------------
# CORE PLOTTING FUNCTION
# ------------------------------------------------------------

def plot_graph(edges, individuals, pos, allowed_categories, title, curved=False):
    plt.figure(figsize=(10, 10))

    G = nx.DiGraph()
    G.add_nodes_from(individuals)

    # Node colors by individual
    node_colors = [INDIVIDUAL_COLORS[n] for n in individuals]

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=NODE_SIZE,
        node_color=node_colors,
        edgecolors="black",
        linewidths=1.2
    )

    # Node labels
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9,
        font_weight="bold",
        font_color="black"
    )

    # Edge curvature
    connectionstyle = "arc3,rad=0.18" if curved else "arc3,rad=0.0"

    for category in allowed_categories:
        cat_edges = edges[edges["Category"] == category]

        if cat_edges.empty:
            continue

        edge_list = list(zip(cat_edges["Source"], cat_edges["Target"]))
        widths = (cat_edges["Weighted_Intensity"] * EDGE_SCALE).tolist()

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edge_list,
            width=widths,
            edge_color=EDGE_COLORS[category],
            arrows=True,
            arrowstyle=ARROW_STYLE,
            arrowsize=ARROW_SIZE,
            min_source_margin=NODE_MARGIN,
            min_target_margin=NODE_MARGIN,
            alpha=EDGE_ALPHA,
            connectionstyle=connectionstyle
        )

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------
# GRAPH WRAPPERS (ENGLISH)
# ------------------------------------------------------------

def plot_agonista(edges, individuals, pos):
    plot_graph(
        edges,
        individuals,
        pos,
        allowed_categories=["Agonista"],
        title=f"{translate_category('Agonista')} interactions (pressure)",
        curved=False
    )

def plot_agonista_apaciguamiento(edges, individuals, pos):
    plot_graph(
        edges,
        individuals,
        pos,
        allowed_categories=["Agonista", "Apaciguamiento"],
        title=(
            f"{translate_category('Agonista')} + "
            f"{translate_category('Apaciguamiento')} "
            "(pressure and de-escalation)"
        ),
        curved=True
    )

def plot_afiliativa(edges, individuals, pos):
    plot_graph(
        edges,
        individuals,
        pos,
        allowed_categories=["Afiliativa"],
        title=f"{translate_category('Afiliativa')} interactions (bonding)",
        curved=False
    )

def plot_all(edges, individuals, pos):
    plot_graph(
        edges,
        individuals,
        pos,
        allowed_categories=["Agonista", "Apaciguamiento", "Afiliativa"],
        title="Full social system (all interaction types)",
        curved=True
    )

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    edges, individuals = load_data()
    pos = compute_node_positions(individuals, edges)

    plot_agonista(edges, individuals, pos)
    plot_agonista_apaciguamiento(edges, individuals, pos)
    plot_afiliativa(edges, individuals, pos)
    plot_all(edges, individuals, pos)

# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
