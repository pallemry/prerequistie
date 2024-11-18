# Course Dependency Graph

A web application to visualize course dependencies dynamically. Users can select completed courses, generate an updated dependency graph, and interact with it through a responsive and mobile-friendly interface.

## Features

- **Dynamic Course Selection**: Select completed courses using a checkbox list.
- **Real-Time Graph Generation**: Updates the course dependency graph based on user input.
- **Zoom Modal**: View the graph in detail by clicking on it.
- **Responsive Design**: Optimized for desktop and mobile devices.

## Project Structure

```
.
├── app.py                             # Flask backend for generating the graph
├── static/
│   ├── index.html                     # Main front-end HTML
│   ├── script.js                      # JavaScript for interactivity
│   ├── styles.css                     # Optional external CSS for styling
├── course_dependencies_with_names.json # Course data with dependencies and names
├── final_overlapping_groups.json      # Overlapping course group data
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- pygraphviz
- A web browser (Chrome, Firefox, etc.)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/course-dependency-graph.git
   cd course-dependency-graph
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Graphviz**:
   - Install Graphviz on your system:
     - [Graphviz Downloads](https://graphviz.org/download/)

4. **Run the Flask Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   - Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

1. **Select Courses**:
   - Check the boxes corresponding to completed courses.

2. **Generate Graph**:
   - Click the **Generate Graph** button to visualize the updated course dependency graph.

3. **Zoom In**:
   - Click the graph image to open it in a full-screen modal.

## API Endpoints

- **`GET /get_courses`**:
  - Retrieves all courses with their dependencies and names.
  - Example Response:
    ```json
    {
      "20407": {
        "name": "Data Structures",
        "prerequisites": ["20229"]
      }
    }
    ```

- **`POST /generate_graph`**:
  - Accepts completed courses and generates a dependency graph.
  - Request Body:
    ```json
    {
      "completed_courses": ["20407", "20229"]
    }
    ```
  - Returns the graph as a PNG image.

## Technologies Used

- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Responsive design for mobile and desktop

- **Backend**:
  - Python, Flask

- **Graph Generation**:
  - PyGraphviz (Graphviz for Python)

## Screenshots

### Desktop View
![Desktop View](https://via.placeholder.com/800x400?text=Desktop+View)

### Mobile View
![Mobile View](https://via.placeholder.com/400x800?text=Mobile+View)

### Zoomed Graph
![Zoomed Graph](https://via.placeholder.com/800x400?text=Zoomed+Graph)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributions

Contributions, issues, and feature requests are welcome! Feel free to fork this repository and submit pull requests.
