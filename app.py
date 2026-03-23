from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Integer)

# Create DB
with app.app_context():
    db.create_all()

# CREATE (POST)
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json

    if not data or 'name' not in data or 'salary' not in data:
        return jsonify({"message": "Invalid data"}), 400

    if data['name'].strip() == "":
        return jsonify({"message": "Name cannot be empty"}), 400

    if data['salary'] < 0:
        return jsonify({"message": "Salary cannot be negative"}), 400

    new_emp = Employee(name=data['name'], salary=data['salary'])
    db.session.add(new_emp)
    db.session.commit()

    return jsonify({"message": "Employee added"}), 201


# READ (ALL)
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()

    result = []
    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "salary": emp.salary
        })

    return jsonify(result)


# READ (SINGLE)
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    emp = db.session.get(Employee, id)

    if not emp:
        return jsonify({"message": "Employee not found"}), 404

    return jsonify({
        "id": emp.id,
        "name": emp.name,
        "salary": emp.salary
    })


# UPDATE (PUT)
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    emp = db.session.get(Employee, id)

    if not emp:
        return jsonify({"message": "Employee not found"}), 404

    data = request.json

    if not data or 'name' not in data or 'salary' not in data:
        return jsonify({"message": "Invalid data"}), 400

    if data['name'].strip() == "":
        return jsonify({"message": "Name cannot be empty"}), 400

    if data['salary'] < 0:
        return jsonify({"message": "Salary cannot be negative"}), 400

    emp.name = data['name']
    emp.salary = data['salary']
    db.session.commit()

    return jsonify({"message": "Employee updated"})


# DELETE
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    emp = db.session.get(Employee, id)

    if not emp:
        return jsonify({"message": "Employee not found"}), 404

    db.session.delete(emp)
    db.session.commit()

    return jsonify({"message": "Employee deleted successfully"})


# Run server
if __name__ == "__main__":
    app.run(debug=True)