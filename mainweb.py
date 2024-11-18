from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import json
import pygraphviz as pgv
from io import BytesIO

from use3party_withoverlap import generate_graphv2

app = Flask(__name__)

# Load course data
COURSE_FILE = "course_dependencies_with_names.json"
OVERLAP_FILE = "final_overlapping_groups.json"
with open(COURSE_FILE, "r", encoding="utf-8") as f:
    course_data = json.load(f)
with open(OVERLAP_FILE, "r", encoding="utf-8") as f:
    overlapping_groups = json.load(f)

@app.route('/')
def index():
    """Serve the index.html file."""
    return send_from_directory(app.static_folder, "index.html")


@app.route('/get_courses', methods=['GET'])
def get_courses():
    """Serve the course data."""
    return jsonify(course_data)

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    """Generate and return the graph image."""
    completed_courses = request.json.get('completed_courses', [])

    img_data = BytesIO()
    generate_graphv2(completed_courses, img_data, format="png")
    img_data.seek(0)
    return send_file(img_data, mimetype="image/png")

def incorporate_overlapping_courses(course_data, overlapping_groups, completed_courses):
    """Filter course data based on overlapping courses and completed courses."""
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
                filtered_prereqs.add(prereq)
            else:
                if prereq in overlap_map and overlap_map[prereq].intersection(completed_courses):
                    continue
                else:
                    filtered_prereqs.add(prereq)
        filtered_course_data[course_id] = {
            "name": details["name"],
            "prerequisites": list(filtered_prereqs),
        }
    return filtered_course_data

if __name__ == "__main__":
    app.run(debug=True)
