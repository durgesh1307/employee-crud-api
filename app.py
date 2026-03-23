from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Model (Table)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Integer)

# Create database
with app.app_context():
    db.create_all()

# Create Employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    new_emp = Employee(name=data['name'], salary=data['salary'])
    db.session.add(new_emp)
    db.session.commit()
    return jsonify({"message": "Employee added"}), 201

# Get All Employees
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = []
    for emp in employees:
        result.append({"id": emp.id, "name": emp.name, "salary": emp.salary})
    return jsonify(result)

# Update Employee
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    emp = Employee.query.get(id)
    data = request.json
    emp.name = data['name']
    emp.salary = data['salary']
    db.session.commit()
    return jsonify({"message": "Employee updated"})

# Delete Employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    emp = Employee.query.get(id)
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message": "Employee deleted"})

if __name__ == "__main__":
    app.run(debug=True)