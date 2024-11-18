import json
import pygraphviz as pgv

def load_data(json_file):
    """
    Load course dependencies and details from a JSON file.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

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

def incorporate_overlapping_courses(course_data, overlapping_groups, completed_courses):
    """
    Remove overlapping courses from consideration, ensuring only unmet prerequisites or completed courses are kept.
    """
    # Convert overlapping groups into a dictionary for quick lookup
    overlap_map = {}
    for group in overlapping_groups:
        for course in group:
            if overlap_map.get(course):
                overlap_map[course].update(group)
            else:
                overlap_map[course] = set(group)

    filtered_course_data = {}

    for course_id, details in course_data.items():
        prerequisites = details["prerequisites"]

        filtered_prereqs = set()
        for prereq in prerequisites:
            if prereq in completed_courses:
                # If the prerequisite is completed, keep it
                filtered_prereqs.add(prereq)
            else:
                # If not completed, check if it belongs to an overlapping group
                if prereq in overlap_map:
                    # If no overlapping course is completed, keep the prerequisite
                    if not overlap_map[prereq].intersection(completed_courses):
                        filtered_prereqs.add(prereq)
                else:
                    # If not part of an overlapping group, keep it
                    filtered_prereqs.add(prereq)

        # Update the course with filtered prerequisites
        filtered_course_data[course_id] = {
            "name": details["name"],
            "prerequisites": list(filtered_prereqs)
        }

    return filtered_course_data


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

def generate_circular_graph(
    course_data, completed_courses, overlapping_groups, output_file="updated_course_dependencies.png"
):
    """
    Generate a course dependency graph with perfect circles, dynamic label wrapping,
    marking completed courses, and highlighting unmet prerequisites for unavailable courses.
    """
    # Incorporate overlapping courses into the data
    filtered_course_data = incorporate_overlapping_courses(course_data, overlapping_groups, completed_courses)

    # Create graph
    graph = pgv.AGraph(strict=True, directed=True, rankdir="TB")

    colors = {
        "default": "#D3D3D3",  # Grey for unavailable
        "completed": "#90EE90",  # Light green
        "next": "#FFD700",       # Gold
        "unmet": "red",          # Red for unmet prerequisites
        "prerequisite": "black",  # Black for normal prerequisites
    }

    # Add nodes
    for course_id, details in filtered_course_data.items():
        raw_label = details["name"]
        wrapped_label = wrap_text(raw_label, max_width=15)
        prerequisites = details["prerequisites"]

        if course_id in completed_courses:
            fillcolor = colors["completed"] # Completed courses
        elif all(prereq in completed_courses for prereq in prerequisites):
            fillcolor = colors["next"]  # Courses that can now be taken
        else:
            fillcolor = colors["default"]  # Unavailable courses

        graph.add_node(
            course_id,
            label=f"<{wrapped_label}>",
            style="filled",
            fillcolor=fillcolor,
            shape="circle",
            fixedsize=True,
            width=1.2,
            height=1.2,
        )

        # Add edges for prerequisites
        for prereq in prerequisites:
            edge_color = (
                colors["prerequisite"] if prereq in completed_courses else colors["unmet"]
            )
            graph.add_edge(prereq, course_id, color=edge_color)

    # Apply layout and save
    graph.layout(prog="dot")
    graph.draw(output_file)  # Save with high resolution
    print(f"Graph saved to {output_file}")

def main():
    # Load the JSON files
    course_file = "course_dependencies_with_names.json"
    overlap_file = "final_overlapping_groups.json"

    course_data = load_data(course_file)
    overlapping_groups = load_data(overlap_file)

    # List of completed courses (manually provided)
    completed_courses = [
        "4101", "20474", "20476", "20441", "20471", "20277",
        "20109", "20465", "20475", "20996", "20425", "20466",
        "20997", "20407", "20229", "20582"
    ]

    # Generate the graph
    generate_circular_graph(course_data, completed_courses, overlapping_groups)

if __name__ == "__main__":
    main()
