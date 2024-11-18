import requests
from bs4 import BeautifulSoup
import re
import json
import networkx as nx
import matplotlib.pyplot as plt

# Base URL for courses
main_url = "https://academic.openu.ac.il/cs/computer/program/M6.aspx"

def fetch_course_links(main_url):
    response = requests.get(main_url)
    course_links = {}
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "courses/" in href:
                course_id = re.search(r'(\d+)\.htm', href)
                if course_id:
                    course_id = course_id.group(1)
                    if href.startswith('http'):
                        course_links[course_id] = href
                    else:
                        course_links[course_id] = "https://www.openu.ac.il" + href
    
    return course_links

def extract_prerequisites_and_name(course_url):
    response = requests.get(course_url)
    prerequisites = []
    course_name = "Unknown Course"
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract course name from <h1 id="course_title">
        title_tag = soup.find('h1', id='course_title')
        if title_tag:
            course_name = title_tag.get_text(strip=True)
        
        # Search for prerequisites
        prereq_section = soup.find(string=re.compile(r"ידע קודם דרוש"))
        if prereq_section:
            parent = prereq_section.find_parent()
            if parent:
                for link in parent.find_all('a', href=True):
                    course_id = re.search(r'(\d+)\.htm', link['href'])
                    if course_id:
                        prerequisites.append(course_id.group(1))
    
    return course_name, prerequisites

def build_dependency_graph(course_dependencies):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add nodes and edges
    for course_id, data in course_dependencies.items():
        course_name = data["name"]
        graph.add_node(course_id, label=course_name)
        for prereq_id in data["prerequisites"]:
            graph.add_edge(prereq_id, course_id)

    return graph

def visualize_graph(graph):
    pos = nx.spring_layout(graph)  # Layout for visualization
    plt.figure(figsize=(15, 10))
    
    # Draw the graph
    labels = nx.get_node_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000, font_size=10, arrowsize=20)
    plt.title("Course Dependency Graph")
    plt.show()

def main():
    # Process all courses and build dependencies
    course_dependencies = {}
    course_links = fetch_course_links(main_url)

    for course_id, course_url in course_links.items():
        try:
            course_name, prerequisites = extract_prerequisites_and_name(course_url)
            course_dependencies[course_id] = {
                "name": course_name,
                "prerequisites": prerequisites
            }
        except Exception as e:
            print(f"Error processing course {course_id}: {e}")

    # Save the enhanced data to a JSON file
    output_file = "course_dependencies_with_names.json"

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(course_dependencies, json_file, ensure_ascii=False, indent=4)

    print(f"Course dependencies graph saved to {output_file}")

    # Build and visualize the dependency graph
    graph = build_dependency_graph(course_dependencies)
    visualize_graph(graph)

if __name__ == "__main__":
    main()
