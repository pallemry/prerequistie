import requests
from bs4 import BeautifulSoup
import re
import json

# Base URL for courses
main_url = "https://academic.openu.ac.il/cs/computer/program/M6.aspx"

def fetch_course_links(main_url):
    response = requests.get(main_url)
    course_links = {}
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all <a> tags containing course links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if "courses/" in href:  # Filter for course URLs
                course_id = re.search(r'(\d+)\.htm', href)  # Extract course ID
                if course_id:
                    course_id = course_id.group(1)
                    # Handle relative and absolute URLs
                    if href.startswith('http'):
                        course_links[course_id] = href
                    else:
                        course_links[course_id] = "https://www.openu.ac.il" + href
    
    return course_links

def extract_prerequisites(course_url):
    response = requests.get(course_url)
    prerequisites = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for "ידע קודם דרוש" or similar keywords
        prereq_section = soup.find(string=re.compile(r"ידע קודם דרוש"))
        if prereq_section:
            parent = prereq_section.find_parent()
            if parent:
                # Find all linked courses in the section
                for link in parent.find_all('a', href=True):
                    course_id = re.search(r'(\d+)\.htm', link['href'])
                    if course_id:
                        prerequisites.append(course_id.group(1))
    
    return prerequisites


def main():
    # Process all courses and build dependencies
    course_dependencies = {}
    course_links = fetch_course_links(main_url)

    for course_id, course_url in course_links.items():
        try:
            prerequisites = extract_prerequisites(course_url)
            course_dependencies[course_id] = prerequisites
        except Exception as e:
            print(f"Error processing course {course_id}: {e}")

    # Save the graph as a JSON file
    output_file = "course_dependencies.json"

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(course_dependencies, json_file, ensure_ascii=False, indent=4)

    print(f"Course dependencies graph saved to {output_file}")



if __name__ == "__main__":
    main()