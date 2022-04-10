#app configuration
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#database section
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    
    def __repr__(self):
        return '<User %r>' % self.usernam

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
    #evacuees
    
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
    name = db.Column(db.String(150))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #Foreign Keys
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'))
    # Relationships
    employee_phone_numbers = db.relationship('Employee_phone_number', backref='employee', lazy=True)
    employee_contacts = db.relationship('Employee_contact', backref='employee', lazy=True)
    employee_emergency_contacts = db.relationship('Employee_emergency_contact', backref='employee', lazy=True)
    # One-to-one relationships
    user = db.relationship('User', backref='employee', uselist=False)
    employee_address = db.relationship('Employee_address', backref='employee', uselist=False)

    def __repr__(self):
        return f'Employee("{self.employee_id}","{self.name}",{self.email})'

class Employee_phone_number(db.Model):
    employee_phone_number_id = db.Column(db.Integer, primary_key=True)
    employee_phone_number = db.Column(db.String(15), nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    #
    employee_contact_id = db.Column(db.Integer, db.ForeignKey('employee_contact.employee_contact_id'), nullable=False)

    def __repr__(self):
        return f'Employee_phone_number("{self.employee_phone_number_id}",{self.employee_phone_number})'

class Employee_contact(db.Model): 
    employee_contact_id = db.Column(db.Integer, primary_key=True, unique=True)
    employee_contact_name = db.Column(db.String(150), nullable=False)
    contact_phone_number= db.Column(db.String(15), primary_key=True, unique=True, nullable=False)
    contact_type = db.Column(db.String(5), primary_key=True, nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    # Relationships
    employee_emergency_contact = db.relationship('Employee_emergency_contact', backref='employee_contact', uselist=False)
    
    def __repr__(self):
        return f'Employee_contact("{self.employee_contact_id}","{self.employee_contact_name}","{self.contact_phone_number}",{self.contact_type})'

class Employee_emergency_contact(db.Model):
    employee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    employee_emergency_number = db.Column(db.String(10), nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_relation = db.Column(db.String(50))
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    employee_contact_id = db.Column(db.Integer, db.ForeignKey('employee_contact.employee_contact_id'), nullable=False)

    def __repr__(self):
        return f'Employee_emergency_contact("{self.employee_emergency_contact_id}","{self.employee_emergency_number}","{self.contact_name}",{self.emergency_contact_relation})'

class Employee_address(db.Model):
    employee_address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    # Foreign Keys
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))

    def __repr__(self):
        return f'Employee_address("{self.employee_address_id}","{self.street}",{self.city})'

#roles many to many
Roles = db.Table('Employee_roles', db.Model.metadata,
db.Column('employee.employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True),
db.Column('role.role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True))

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    role_description = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.role_name

#departments many to many
Departments = db.Table('Employee_assigned_departments', db.Model.metadata,
db.Column('department.department_id', db.Integer, db.ForeignKey('department.department_id'), primary_key=True),
db.Column('employee.employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True))

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
    evacueeee_phone_numbers = db.relationship('Evacuee_phone_number', backref='evacuee', lazy=True)
    evacuee_contacts = db.relationship('Evacuee_contact', backref='evacuee', lazy=True)
    evacuee_emergency_contacts = db.relationship('Evacuee_emergency_contact', backref='evacuee', lazy=True)
    # One-to-one relationships
    evacuee_address = db.relationship('Evacuee_address', backref='evacuee', uselist=False)

    def __repr__(self):
        return f'Evacuee("{self.evacuee_id}","{self.name}",{self.email})'

class Evacuee_phone_number(db.Model):
    evacuee_phone_number_id = db.Column(db.Integer, primary_key=True)
    evacuee_phone_number = db.Column(db.String(15), nullable=False)
    # Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)
    #
    evacuee_contact_id = db.Column(db.Integer, db.ForeignKey('evacuee_contact.evacuee_contact_id'), nullable=False)

    def __repr__(self):
        return f'Evacuee_phone_number("{self.evacuee_phone_number_id}",{self.evacuee_phone_number})'

class Evacuee_contact(db.Model): 
    evacuee_contact_id = db.Column(db.Integer, primary_key=True, unique=True)
    evacuee_contact_name = db.Column(db.String(150), nullable=False)
    contact_phone_number= db.Column(db.String(15), primary_key=True, unique=True, nullable=False)
    contact_type = db.Column(db.String(5), primary_key=True, nullable=False)
    # Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)
    # Relationships
    evacuee_emergency_contact = db.relationship('Evacuee_emergency_contact', backref='evacuee_contact', uselist=False)
    
    def __repr__(self):
        return f'Evacuee_contact("{self.evacuee_contact_id}","{self.evacuee_contact_name}","{self.contact_phone_number}",{self.contact_type})'

class Evacuee_emergency_contact(db.Model):
    evacuee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    evacuee_emergency_number = db.Column(db.String(10), nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_relation = db.Column(db.String(50))
    # Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)
    evacuee_contact_id = db.Column(db.Integer, db.ForeignKey('evacuee_contact.evacuee_contact_id'), nullable=False)

    def __repr__(self):
        return f'Evacuee_emergency_contact("{self.evacuee_emergency_contact_id}","{self.evacuee_emergency_number}","{self.contact_name}",{self.emergency_contact_relation})'

class Evacuee_address(db.Model):
    evacuee_address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    # Foreign Keys
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'))

    def __repr__(self):
        return f'Evacuee_address("{self.evacuee_address_id}","{self.street}",{self.city})'

#work on evacuee_transfers table next
class Evacuee_Transfer(db.Model):
    evacuee_transfer_id = db.Column(db.Integer, primary_key=True)
    evac_id_1 = db.Column(db.Integer, unique=True)
    evac_id_2 = db.Column(db.Integer, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)

    def __repr__(self):
        return '<Evacuee_transfer %r>' % self.evacuee_transfer_id, self.evac_id_1, self.evac_id_2, self.date_added

#run code
if __name__ == "__main__":
    app.run()
    #write user models here for testing
#SELECT test;
#SELECT * 
#FROM employee
#INNER JOIN Employee_phone_number ON Employee_phone_number.employee_id = employee_phone_number.employee_id 