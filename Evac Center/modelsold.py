from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True
 
# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oldver.db'
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))

    def __repr__(self):
        return '<User %r>' % self.username

class Evaccenter(db.Model):
    evaccenter_id = db.Column(db.Integer, primary_key=True)
    evac_num = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(6))
    # Relationships
    employees = db.relationship('Employee', backref='evaccenter', lazy=True)
    supplies = db.relationship('Supply', backref='evaccenter', lazy=True)
    evacuees = db.relationship('Evacuee', backref='evaccenter', lazy=True)
   
    def __repr__(self):
        return f'Evaccenter("{self.name}","{self.city}",{self.state})'

class Supply(db.Model):
    supply_id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(100))
    supply_count = db.Column(db.Integer)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'))
    
    def __repr__(self):
        return f'Supply("{self.supply_name}",{self.supply_count})'

#have ability to add employees
class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Foreign Keys
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'))
    # Relationships
    EmployeePhoneNumbers = db.relationship('EmployeePhoneNumber', backref='employee', lazy=True)
    EmployeeEmergencyContacts = db.relationship('EmployeeEmergencyContact', backref='employee', lazy=True)
    # One-to-one relationships
    user = db.relationship('User', backref='employee', uselist=False)
    employee_address = db.relationship('Employee_address', backref='employee', uselist=False)

    def __repr__(self):
        return f'Employee("{self.employee_id}","{self.name}",{self.email})'

class Employee_address(db.Model):
    employee_address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))

    def __repr__(self):
        return f'EmployeeAddress("{self.employee_address_id}","{self.street}",{self.city})'

class EmployeeEmergencyContact(db.Model):
    employee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    employee_emergency_number = db.Column(db.String(10), nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_relation = db.Column(db.String(50))
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)

    def __repr__(self):
        return f'EmployeeEmergencyContact("{self.employee_emergency_contact_id}","{self.employee_emergency_number}","{self.contact_name}",{self.emergency_contact_relation})'

class EmployeePhoneNumber(db.Model):
    employee_phone_id = db.Column(db.Integer, primary_key=True)
    employee_phone_number = db.Column(db.String(15), nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)

    def __repr__(self):
        return f'EmployeePhoneNumber("{self.employee_phone_id}",{self.employee_phone_number})'

#Many to many for Employee -> Roles
#Roles = db.Table('Employee_roles', db.Model.metadata,
#db.Column('employee.employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True),
#db.Column('role.role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True))

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    role_description = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.role_name

#Many to many for Employee -> Departments
#Departments = db.Table('EmployeeAssignedDepartments', db.Model.metadata,
#db.Column('department.department_id', db.Integer, db.ForeignKey('department.department_id'), primary_key=True),
#db.Column('employee.employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True))

class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), unique=True)
    department_description = db.Column(db.String(200))

    def __repr__(self):
        return '<Department %r>' % self.department_name

#Have ability to add Evacuees
class Evacuee(db.Model):
    evacuee_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Foreign Keys
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'))
    # Relationships
    evacuee_phone_numbers = db.relationship('EvacueePhoneNumber', backref='evacuee', lazy=True)
    evacuee_emergency_contacts = db.relationship('EvacueeEmergencyContact', backref='evacuee', lazy=True)
    # One-to-one relationships
    evacuee_address = db.relationship('EvacueeAddress', backref='evacuee', uselist=False)

    def __repr__(self):
        return f'Evacuee("{self.evacuee_id}","{self.name}",{self.email})'

class EvacueeAddress(db.Model):
    evacuee_address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    #Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'))

    def __repr__(self):
        return f'EvacueeAddress("{self.evacuee_address_id}","{self.street}",{self.city})'

class EvacueePhoneNumber(db.Model):
    evacuee_phone_number_id = db.Column(db.Integer, primary_key=True)
    evacuee_phone_number = db.Column(db.String(15), nullable=False)
    # Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)

    def __repr__(self):
        return f'EvacueePhoneNumber("{self.evacuee_phone_number_id}",{self.evacuee_phone_number})'

class EvacueeEmergencyContact(db.Model):
    evacuee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    evacuee_emergency_number = db.Column(db.String(10), nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_relation = db.Column(db.String(50))
    # Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)

    def __repr__(self):
        return f'EvacueeEmergencyContact("{self.evacuee_emergency_contact_id}","{self.evacuee_emergency_number}","{self.contact_name}",{self.emergency_contact_relation})'

if __name__ == '__main__':
    app.run()