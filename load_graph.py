import ijson
import networkx as nx
import matplotlib.pyplot as plt

def load_dependency_graph_incrementally(json_file):
    """
    Load a dependency graph incrementally from a JSON file.
    """
    graph = nx.DiGraph()

    with open(json_file, 'r', encoding='utf-8') as f:
        # Incrementally parse the JSON file
        parser = ijson.items(f, 'item')
        
        for course_id, data in ijson.kvitems(f, ''):
            course_name = data.get("name", f"Course {course_id}")
            prerequisites = data.get("prerequisites", [])

            # Add the course to the graph
            graph.add_node(course_id, label=course_name)

            # Add edges for prerequisites
            for prereq in prerequisites:
                graph.add_edge(prereq, course_id)

    return graph

def visualize_graph(graph, max_nodes=None):
    """
    Visualize a dependency graph with an optional limit on the number of nodes.
    """
    if max_nodes and len(graph.nodes) > max_nodes:
        subgraph = graph.subgraph(list(graph.nodes)[:max_nodes])
    else:
        subgraph = graph

    pos = nx.spring_layout(subgraph)
    plt.figure(figsize=(15, 10))
    
    # Draw the graph
    labels = nx.get_node_attributes(subgraph, 'label')
    nx.draw(subgraph, pos, with_labels=True, labels=labels, node_size=3000, font_size=10, arrowsize=20)
    plt.title("Course Dependency Graph")
    plt.show()

def main():
    json_file = "course_dependencies_with_names.json"

    # Load the dependency graph incrementally
    print("Loading dependency graph incrementally...")
    graph = load_dependency_graph_incrementally(json_file)

    # Visualize the graph
    print("Visualizing the dependency graph...")
    visualize_graph(graph, max_nodes=50)  # Visualize up to 50 nodes

if __name__ == "__main__":
    main()
