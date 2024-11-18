import json
import requests
from bs4 import BeautifulSoup
import re

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

def extract_prerequisites_and_name(course_url):
    """
    Fetch the course name and prerequisites from the course URL.
    """
    response = requests.get(course_url)
    prerequisites = []
    course_name = "Unknown Course"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract course name
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

def update_missing_courses(course_data, base_url="https://www.openu.ac.il/courses/"):
    """
    Identify missing courses, fetch their details, and update the course data.
    """
    all_course_ids = set(course_data.keys())
    prerequisite_ids = {
        prereq for details in course_data.values() for prereq in details["prerequisites"]
    }
    missing_ids = prerequisite_ids - all_course_ids

    for course_id in missing_ids:
        print(f"Fetching details for missing course: {course_id}")
        course_url = f"{base_url}{course_id}.htm"
        course_name, prerequisites = extract_prerequisites_and_name(course_url)

        # Add the missing course to the data
        course_data[course_id] = {
            "name": course_name,
            "prerequisites": prerequisites
        }

    return course_data

def main():
    # Load the JSON file
    json_file = "course_dependencies_with_names.json"
    course_data = load_data(json_file)

    # Update missing courses
    updated_course_data = update_missing_courses(course_data)

    # Save the updated data back to the JSON file
    save_data(json_file, updated_course_data)
    print(f"Updated course data saved to {json_file}")

if __name__ == "__main__":
    main()
