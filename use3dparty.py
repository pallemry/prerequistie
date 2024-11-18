import json
import pygraphviz as pgv

def load_data(json_file):
    """
    Load course dependencies and details from a JSON file.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(json_file, data):
    """
    Save updated course data to a JSON file.
    """
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def wrap_text(label, max_width=15):
    """
    Wrap text to fit within a node by breaking at spaces.
    """
    words = label.split()
    lines = []
    current_line = []

    for word in words:
        if sum(len(w) for w in current_line) + len(current_line) + len(word) > max_width:
            lines.append(" ".join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    if current_line:
        lines.append(" ".join(current_line))
    return "<br/>".join(lines)

def add_completed_courses_to_graph(graph, completed_courses):
    """
    Add completed courses to the graph and mark them as completed.
    """
    for course_id in completed_courses:
        if graph.has_node(course_id):
            graph.get_node(course_id).attr.update(style="filled", fillcolor="#90EE90")  # Light green for completed

def identify_next_courses(course_data, completed_courses):
    """
    Identify courses that can be taken next based on completed prerequisites.
    """
    next_courses = []
    for course_id, details in course_data.items():
        prerequisites = details["prerequisites"]
        if all(prereq in completed_courses for prereq in prerequisites) and course_id not in completed_courses:
            next_courses.append(course_id)
    return next_courses

def generate_circular_graph(course_data, completed_courses, output_file="updated_course_dependencies.png"):
    """
    Generate a course dependency graph with perfect circles, dynamic label wrapping,
    and marking completed courses.
    """
    graph = pgv.AGraph(strict=True, directed=True, rankdir="TB")

    colors = {
        "default": "#D3D3D3",
        "completed": "#90EE90",  # Light green
        "next": "#FFD700",       # Gold
        "prerequisite": "black"
    }

    # Add nodes
    for course_id, details in course_data.items():
        raw_label = details["name"]
        wrapped_label = wrap_text(raw_label, max_width=15)
        prerequisites = details["prerequisites"]

        fillcolor = colors["completed"] if course_id in completed_courses else colors["default"]
        graph.add_node(
            course_id,
            label=f"<{wrapped_label}>",
            style="filled",
            fillcolor=fillcolor,
            shape="circle",
            fixedsize=True,
            width=1.2,
            height=1.2
        )

        for prereq in prerequisites:
            graph.add_edge(prereq, course_id, color=colors["prerequisite"])

    # Mark completed courses
    add_completed_courses_to_graph(graph, completed_courses)

    # Identify and mark next courses
    next_courses = identify_next_courses(course_data, completed_courses)
    for course_id in next_courses:
        graph.get_node(course_id).attr.update(style="filled", fillcolor=colors["next"])

    # Apply layout and save
    graph.layout(prog="dot")
    graph.draw(output_file)  # Save with 300 DPI for high resolution
    print(f"Graph saved to {output_file}")

def main():
    # Load the JSON file
    json_file = "course_dependencies_with_names.json"
    course_data = load_data(json_file)

    # List of completed courses (manually provided)
    completed_courses = [
        "4101", "20474", "20476", "20441", "20471", "20277",
        "20109", "20465", "20475", "20996", "20425", "20466",
        "20997", "20407", "20229", "20582"
    ]

    # Generate the graph
    generate_circular_graph(course_data, completed_courses)

if __name__ == "__main__":
    main()
