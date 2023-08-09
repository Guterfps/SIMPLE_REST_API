
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from producer import SendMsg

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employee'

    name = db.Column(db.String(64), primary_key=True)
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    salary = db.Column(db.Integer)

    def json(self):
        return {
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'salary': self.salary
        }

db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/employees', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_employee = Employee(name=data['name'], country=data['country'], 
                                city=data['city'], salary=data['salary'])
        db.session.add(new_employee)
        db.session.commit()
        SendMsg('new employee created: ' + data['name'] + ' in ' + 
                data['country'] + ' city: ' + data['city'] + ' salary: ' + 
                str(data['salary']) + ' $')
        return make_response(jsonify({'message': 'Employee created successfully'}), 201)
    except e:
        return make_response(jsonify({'message': f"error creating employee {e}"}), 500)

@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.all()
        return make_response(jsonify({'employees': [employee.json() for employee in employees]}), 200)
    except e:
        return make_response(jsonify({'message': 'error getting employees'}), 500)

@app.route('/employees/<string:name>', methods=['GET'])
def get_employee(name):
    try:
        employee = Employee.query.filter_by(name=name).first()
        if employee:
            return make_response(jsonify({'employee': employee.json()}), 200)
        else:
            return make_response(jsonify({'message': 'employee not found'}), 404)
    except e:
        return make_response(jsonify({'message': 'error getting employee'}), 500)

@app.route('/employees/<string:name>', methods=['PUT'])
def update_employee(name):
    try:
        employee = Employee.query.filter_by(name=name).first()
        if employee:
            data = request.get_json()
            employee.name = data['name']
            employee.country = data['country']
            employee.city = data['city']
            employee.salary = data['salary']
            db.session.commit()
            return make_response(jsonify({'message': 'employee updated successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'employee not found'}), 404)
    except e:
        return make_response(jsonify({'message': 'error updating employee'}), 500)

@app.route('/employees/<string:name>', methods=['DELETE'])
def delete_employee(name):
    try:
        employee = Employee.query.filter_by(name=name).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return make_response(jsonify({'message': 'employee deleted successfully'}), 200)
        else:
            return make_response(jsonify({'message': 'employee not found'}), 404)
    except e:
        return make_response(jsonify({'message': 'error deleting employee'}), 500)

if __name__ == '__main__':
    app.run()