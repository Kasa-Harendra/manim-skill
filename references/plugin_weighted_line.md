# manim-weighted-line Plugin Reference Guide

`manim-weighted-line` provides weighted edge mobjects (`WeightedLine`) for network graphs in Manim Community. It bridges a long-standing gap in Manim's native `Graph` and `DiGraph` classes by rendering clear numeric edge weights with custom label backgrounds, perfect for algorithms like Dijkstra, Bellman-Ford, Prim's, and Kruskal's.

- **Repository**: [https://github.com/mutable-learning/manim-weighted-line](https://github.com/mutable-learning/manim-weighted-line)
- **Author**: MutableLearning
- **Package**: `manim-weighted-line`
- **Import Namespace**: `manim_weighted_line`

---

## 1. Installation & Setup

```bash
pip install manim-weighted-line networkx
```

Import in your script:
```python
from manim import *
from manim_weighted_line import *
```

---

## 2. Core API: `WeightedLine`

Use `WeightedLine` as an individual line or as the `edge_type` parameter in Manim's `Graph` and `DiGraph`:

```python
# Standalone weighted line:
line = WeightedLine(start=LEFT * 2, end=RIGHT * 2, weight=7)
```

### Integration with `Graph` & `DiGraph`
```python
vertices = [1, 2, 3, 4]
edges = [(1, 2), (2, 3), (3, 4), (4, 1)]

g = Graph(
    vertices,
    edges,
    layout="circular",
    layout_scale=2.5,
    labels=True,
    edge_type=WeightedLine,
    edge_config={
        (1, 2): {"weight": 5, "stroke_color": BLUE_C},
        (2, 3): {"weight": 12, "stroke_color": TEAL_C},
        (3, 4): {"weight": 3, "stroke_color": GREEN_C},
        (4, 1): {"weight": 8, "stroke_color": ORANGE},
    }
)
```

---

## 3. Production Recipe: Dijkstra's Shortest Path Graph

```python
from manim import *
from manim_weighted_line import *
import networkx as nx

class WeightedGraphScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title = Tex(r"\textbf{Weighted Network: Shortest Path Routing}", font_size=32).to_edge(UP, buff=0.6)
        self.add(title)

        # 1. Define NetworkX weighted graph
        G = nx.Graph()
        G.add_nodes_from(["A", "B", "C", "D", "E"])
        weighted_edges = [
            ("A", "B", 4),
            ("A", "C", 2),
            ("B", "C", 1),
            ("B", "D", 5),
            ("C", "D", 8),
            ("C", "E", 10),
            ("D", "E", 2),
        ]
        G.add_weighted_edges_from(weighted_edges)

        # Custom node positions for clean layout
        layout = {
            "A": LEFT * 3.5,
            "B": LEFT * 1.2 + UP * 1.5,
            "C": LEFT * 1.2 + DOWN * 1.5,
            "D": RIGHT * 1.5 + UP * 1.0,
            "E": RIGHT * 3.5 + DOWN * 0.5,
        }

        # 2. Build Manim Graph with WeightedLine edges
        graph = Graph(
            list(G.nodes),
            list(G.edges),
            layout=layout,
            labels=True,
            vertex_config={"radius": 0.35, "fill_color": "#111111", "stroke_color": BLUE_C, "stroke_width": 2},
            edge_type=WeightedLine,
            edge_config={(u, v): {"weight": G[u][v]["weight"], "stroke_color": GRAY_C, "stroke_width": 2.0} for u, v in G.edges}
        )

        self.play(Create(graph), run_time=2.0)
        self.wait(1)

        # 3. Highlight Optimal Shortest Path: A -> C -> B -> D -> E
        path_edges = [("A", "C"), ("B", "C"), ("B", "D"), ("D", "E")]
        for u, v in path_edges:
            edge_mob = graph.edges[(u, v)] if (u, v) in graph.edges else graph.edges[(v, u)]
            self.play(
                edge_mob.animate.set_stroke(color=YELLOW_C, width=4.0),
                run_time=0.5
            )

        self.wait(1.5)
```

---

## 4. Best Practices

1. **Undirected Edge Key Ordering**: In undirected graphs, edge tuples can be keyed as `(u, v)` or `(v, u)` depending on how NetworkX orders them; access via conditional lookup or standardize keys.
2. **Weight Visibility**: Ensure weight text contrast remains sharp by setting edge lines to subtle tones (`GRAY_C`) and active paths to vibrant highlights (`YELLOW_C` or `GREEN_C`).
