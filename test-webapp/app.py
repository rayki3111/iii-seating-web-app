import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import os

app = Flask(__name__)

SAVE_FILE = "seating.json"

students = [
    {"name": "Ethan Walker", "gender": "Male", "height": "Medium", "grade": "High", "vision": "Nearsighted"},
    {"name": "Aisha Patel", "gender": "Female", "height": "Short", "grade": "Medium", "vision": "Good"},
    {"name": "Noah Thompson", "gender": "Male", "height": "Tall", "grade": "High", "vision": "Good"},
    {"name": "Sakura Tanaka", "gender": "Female", "height": "Medium", "grade": "Low", "vision": "Nearsighted"},
    {"name": "Liam O'Connor", "gender": "Male", "height": "Short", "grade": "Medium", "vision": "Good"},
    {"name": "Olivia Müller", "gender": "Female", "height": "Tall", "grade": "High", "vision": "Nearsighted"},
    {"name": "Rafael Kim", "gender": "Male", "height": "Medium", "grade": "Low", "vision": "Good"},
    {"name": "Amara Singh", "gender": "Female", "height": "Medium", "grade": "High", "vision": "Nearsighted"},
    {"name": "Sebastian Carter", "gender": "Male", "height": "Tall", "grade": "Medium", "vision": "Good"},
    {"name": "Emily Laurent", "gender": "Female", "height": "Short", "grade": "Low", "vision": "Good"},
    {"name": "Daniel Petrov", "gender": "Male", "height": "Medium", "grade": "High", "vision": "Nearsighted"},
    {"name": "Chloe Andersson", "gender": "Female", "height": "Medium", "grade": "Medium", "vision": "Good"},
    {"name": "Isaac Johnson", "gender": "Male", "height": "Short", "grade": "Low", "vision": "Nearsighted"},
    {"name": "Layla Ahmed", "gender": "Female", "height": "Tall", "grade": "High", "vision": "Good"},
    {"name": "Javier Rossi", "gender": "Male", "height": "Medium", "grade": "Medium", "vision": "Good"},
    {"name": "Priya Sharma", "gender": "Female", "height": "Short", "grade": "Low", "vision": "Nearsighted"},
    {"name": "Viktor Kuznetsov", "gender": "Male", "height": "Tall", "grade": "High", "vision": "Nearsighted"},
    {"name": "Naomi Becker", "gender": "Female", "height": "Medium", "grade": "Medium", "vision": "Good"},
    {"name": "Felix Moreau", "gender": "Male", "height": "Short", "grade": "Low", "vision": "Good"},
    {"name": "Hana Lee", "gender": "Female", "height": "Tall", "grade": "High", "vision": "Nearsighted"},
    {"name": "Oscar Evans", "gender": "Male", "height": "Medium", "grade": "Medium", "vision": "Good"},
    {"name": "Isabella Novak", "gender": "Female", "height": "Short", "grade": "Low", "vision": "Good"},
    {"name": "Elijah Smith", "gender": "Male", "height": "Tall", "grade": "High", "vision": "Nearsighted"},
    {"name": "Sofia Dimitrov", "gender": "Female", "height": "Medium", "grade": "Medium", "vision": "Good"}
]

@app.route('/')
def index():
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    """Add a student to the list."""
    name = request.form['name']
    gender = request.form['gender']
    height = request.form['height']
    grade = request.form['grade']
    vision = request.form['vision']

    students.append({'name': name, 'gender': gender, 'height': height, 'grade': grade, 'vision': vision})
    return redirect(url_for('index'))

@app.route('/delete_student/<string:name>', methods=['POST'])
def delete_student(name):
    """Remove a student by name."""
    global students
    students = [s for s in students if s['name'] != name]
    return redirect(url_for('index'))

@app.route('/generate_seating')
def generate_seating():
    if not students:
        return render_template('seating.html', seating=[[None] * 8 for _ in range(8)])

    students_sorted = sorted(students, key=lambda s: (s['vision'] != 'Nearsighted', s['height'] == 'Tall'))

    males = [s for s in students_sorted if s['gender'] == 'Male']
    females = [s for s in students_sorted if s['gender'] == 'Female']

    seating_order = []
    while males or females:
        if females:
            seating_order.append(females.pop(0))
        if males:
            seating_order.append(males.pop(0))

    allowed_positions = [(1, 0), (1, 1), (1, 3), (1, 4), (1, 6), (1, 7),
                         (3, 0), (3, 1), (3, 3), (3, 4), (3, 6), (3, 7),
                         (5, 0), (5, 1), (5, 3), (5, 4), (5, 6), (5, 7),
                         (7, 0), (7, 1), (7, 3), (7, 4), (7, 6), (7, 7)]

    seating_grid = [[None for _ in range(8)] for _ in range(8)]
    index = 0

    for row, col in allowed_positions:
        if index < len(seating_order):
            seating_grid[row][col] = seating_order[index]
            index += 1

    for r in range(8):
        for c in range(8):
            if seating_grid[r][c] is None and index < len(seating_order):
                seating_grid[r][c] = seating_order[index]
                index += 1

    return render_template('seating.html', seating=seating_grid)

@app.route('/save_seating', methods=['POST'])
def save_seating():
    """Save the current seating arrangement to a JSON file."""
    seating_data = request.json
    with open(SAVE_FILE, "w") as f:
        json.dump(seating_data, f)
    return jsonify({"message": "Seating arrangement saved successfully!"})

@app.route('/load_seating')
def load_seating():
    """Load the seating arrangement from the JSON file."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            seating_data = json.load(f)
        return jsonify(seating_data)
    else:
        return jsonify({"message": "No saved seating arrangement found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
