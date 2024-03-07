from manim import *
from typing import Hashable


class WeightedDiGraph(DiGraph):
    def __init__(
        self,
        vertex_values: list[Hashable],
        weighted_edges: list[tuple[Hashable, Hashable, Hashable]],
        vertex_config: dict | None = None,
        edge_config: dict | None = None,
        edge_font_size: int = 20,
        vertex_font_size: int = 24,
        layout: str | dict = "spring",
        layout_config: dict | None = None,
        **kwargs
    ):
        if vertex_config is None:
            vertex_config = {}
            for v in vertex_values:
                vertex_config[v] = {
                    "radius": 0.3,
                    "color": GREEN,
                    "fill_opacity": 1.0,
                }
        if edge_config is None:
            edge_config = {}
            for v1, v2, _ in weighted_edges:
                edge_config[(v1, v2)] = {"tip_length": 0.2, "color": DARK_GRAY}

        if layout == "spring" and layout_config is None:
            layout_config = {"iterations": 1000, "threshold": 1e-4, "seed": 2}
        edge_pairs = [(v1, v2) for v1, v2, _ in weighted_edges]
        super().__init__(
            vertex_values,
            edge_pairs,
            layout=layout,
            layout_config=layout_config,
            labels=False,  # keep this False, since default labels don't work with animations
            vertex_config=vertex_config,
            edge_config=edge_config,
            **kwargs
        )
        self.edge_font_size = edge_font_size
        self.vertex_font_size = vertex_font_size
        self.label_setup(
            vertex_values, weighted_edges, vertex_font_size, edge_font_size
        )

    def label_setup(
        self,
        vertices: list[Hashable],
        weighted_edges: list[tuple[Hashable, Hashable, Hashable]],
        vertex_font_size: int,
        edge_font_size: int,
    ):
        vertex_label_group = VGroup()
        for v in vertices:
            v_obj = self.vertices[v]
            label = Text(str(v), font_size=vertex_font_size, color=BLACK)
            label.move_to(v_obj.get_center())
            vertex_label_group.add(label)

        self.add(vertex_label_group)
        self.vertex_label_group = vertex_label_group

        alpha = 0.5
        edge_labels = VGroup()
        for v1, v2, weight in weighted_edges:
            edge_obj = self.edges[(v1, v2)]
            point = edge_obj.point_from_proportion(alpha)
            label = Text(
                str(weight), font_size=edge_font_size, color=LIGHT_GRAY
            ).move_to(point)
            label.add_background_rectangle(
                color=config.background_color, opacity=1.0, buff=0.05
            )
            edge_labels.add(label)

        self.add(edge_labels)
        self.edge_labels = edge_labels


# manim -pql weighted-digraph.py WeightedGraphDemo
class WeightedGraphDemo(MovingCameraScene):
    def construct(self):
        graph = {
            0: [(1, 2), (2, 1)],
            1: [(2, 5), (3, 11), (4, 3)],
            2: [(5, 15)],
            3: [(4, 2)],
            4: [(2, 1), (5, 4), (6, 5)],
            5: [],
            6: [(3, 1), (5, 1)],
        }
        vertices, edges = self.graph_to_digraph_format(graph)
        vgraph = WeightedDiGraph(vertices, edges)
        scalar = 1.2
        self.camera.frame.set(
            width=vgraph.width * scalar, height=vgraph.height * scalar
        )
        self.add(vgraph)

    def graph_to_digraph_format(self, graph):
        vertices = list(graph.keys())
        edges = []
        for vertex, neighbors in graph.items():
            for neighbor, weight in neighbors:
                edges.append((vertex, neighbor, weight))
        return vertices, edges


class CustomWeightedDiGraph(WeightedDiGraph):
    def highlight_vertex(self, v, color=RED, opacity=1.0):
        self.vertices[v].set(color=color, fill_opacity=opacity)

    def unhighlight_vertex(self, v, color=RED, opacity=1.0):
        self.vertices[v].set(color=color, fill_opacity=opacity)


# manim -pql weighted-digraph.py HighlightNodeDemo
class HighlightNodeDemo(MovingCameraScene):
    def construct(self):
        graph = {
            0: [(1, 2), (2, 1)],
            1: [(2, 5), (3, 11), (4, 3)],
            2: [(5, 15)],
            3: [(4, 2)],
            4: [(2, 1), (5, 4), (6, 5)],
            5: [],
            6: [(3, 1), (5, 1)],
        }

        def dfs(node, graph, vgraph: CustomWeightedDiGraph, visited=[]):
            visited.append(node)
            vgraph.highlight_vertex(node)
            self.wait()
            for neighbor, w in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, graph, vgraph, visited)

        vertices, edges = self.graph_to_digraph_format(graph)
        vgraph = CustomWeightedDiGraph(vertices, edges)
        scalar = 1.2
        self.camera.frame.set(
            width=vgraph.width * scalar, height=vgraph.height * scalar
        )
        self.add(vgraph)
        dfs(0, graph, vgraph)

    def graph_to_digraph_format(self, graph):
        vertices = list(graph.keys())
        edges = []
        for vertex, neighbors in graph.items():
            for neighbor, weight in neighbors:
                edges.append((vertex, neighbor, weight))
        return vertices, edges
