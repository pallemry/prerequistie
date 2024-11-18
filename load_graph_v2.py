import ijson
import networkx as nx
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from networkx.drawing.nx_agraph import graphviz_layout
import plotly.graph_objects as go

def format_label(text):
    """
    Correct Hebrew text for proper display.
    """
    return text
    return get_display(text)

def load_dependency_graph_incrementally(json_file):
    """
    Load a dependency graph incrementally from a JSON file.
    """
    graph = nx.DiGraph()

    with open(json_file, 'r', encoding='utf-8') as f:
        for course_id, data in ijson.kvitems(f, ''):
            course_name = format_label(data.get("name", f"Course {course_id}"))
            prerequisites = data.get("prerequisites", [])

            # Add the course to the graph
            graph.add_node(course_id, label=course_name)

            # Add edges for prerequisites
            for prereq in prerequisites:
                graph.add_edge(prereq, course_id)

    # Debug: Ensure every node has a label
    for node in graph.nodes(data=True):
        if 'label' not in node[1]:
            print(f"Warning: Node {node[0]} is missing a label!")
            graph.nodes[node[0]]['label'] = f"Course {node[0]}"  # Fallback label

    return graph


def visualize_graph(graph, max_nodes=None):
    return
    """
    Visualize a dependency graph using PyGraphviz for better layout.
    """
    if max_nodes and len(graph.nodes) > max_nodes:
        subgraph = graph.subgraph(list(graph.nodes)[:max_nodes])
    else:
        subgraph = graph

    pos = graphviz_layout(subgraph, prog="dot")  # Use "dot" layout for hierarchy
    plt.figure(figsize=(15, 10))
    
    # Draw the graph
    labels = nx.get_node_attributes(subgraph, 'label')
    nx.draw(subgraph, pos, with_labels=True, labels=labels, node_size=3000, font_size=10, arrowsize=20)
    plt.title("Course Dependency Graph")
    plt.show()

def visualize_graph_interactive(graph):
    """
    Visualize the graph interactively using Plotly.
    """
    # Generate positions for nodes
    pos = nx.spring_layout(graph)
    nx.set_node_attributes(graph, pos, 'pos')

    edge_x = []
    edge_y = []
    for edge in graph.edges:
        x0, y0 = graph.nodes[edge[0]]['pos']
        x1, y1 = graph.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    for node in graph.nodes:
        x, y = graph.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)
        node_text.append(graph.nodes[node]['label'])  # Node label

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='top center',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            line_width=2))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    fig.show()


def main():
    json_file = "course_dependencies_with_names.json"

    # Load the dependency graph incrementally
    print("Loading dependency graph incrementally...")
    graph = load_dependency_graph_incrementally(json_file)

    # Visualize the graph
    print("Visualizing the dependency graph...")
    # visualize_graph(graph)  # PyGraphviz
    visualize_graph_interactive(graph)  # Plotly (optional)

if __name__ == "__main__":
    main()
