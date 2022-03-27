#appconfig section
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaccenters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#database section
class Evaccenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evac_num = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(6), nullable=False)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'), nullable=False)
    #supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)
    #
    supplies = db.relationship('Supply', backref='evaccenter', lazy=True)
    evacuees = db.relationship('Evacuee', backref='evaccenter', lazy=True)
    evacuee_transfers = db.relationship('Evacuee_Transfer', backref='evaccenter', lazy=True)
    evacuee_phone_numbers = db.relationship('Evacuee_phone_number', backref='evaccenter', lazy=True)
    Evacuee_emergency_contacts = db.relationship('Evacuee_emergency_contacts', backref='evaccenter', lazy=True)
    Evacuee_contacts = db.relationship('Evacuee_contact', backref='evaccenter', lazy=True)
    employees = db.relationship('Employee', backref='evaccenter', lazy=True)
    
class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(100))
    supply_count = db.Column(db.Integer)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    #
    #evaccenters = db.relationship('Evaccenter', backref='supply', lazy=True)

class Evacuee_Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evac_id_1 = db.Column(db.Integer, unique=True)
    evac_id_2 = db.Column(db.Integer, unique=True)
    #date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'),nullable=False)

class Evacuee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    evacuee_relationship = db.Column(db.String(50))
    #date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #
    evacuee_phone_number = db.Column(db.Integer, db.ForeignKey('evacuee_phone_number.evacuee_phone_number'), nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    evacuee_contact_id = db.Column(db.Integer, db.ForeignKey('evacuee_contact.id'), unique=True, nullable=False)
    evacuee_address_id = db.Column(db.Integer, db.ForeignKey('evacuee_address.id'), nullable=False)
    #
    evacuee_ids = db.relationship('evacuee_id', backref='evacuee', lazy=True)
    evaccenter_ids = db.relationship('evaccenter_id', backref='evacuee', lazy=True)
    evacuee_phone_numbers = db.relationship('Evacuee_phone_number', backref='evacuee', lazy=True)
    evacuee_emergency_contacts = db.relationship('Evacuee_emergency_contact', backref='evacuee', lazy=True)
    Evacuee_contacts = db.relationship('Evacuee_contact', backref='evacuee', lazy=True)

class Evacuee_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(6))
    #
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'), unique=True, nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), unique=True, nullable=False)
    #
    evacuees = db.relationship('Evacuee', backref='Evacuee_address', lazy=True)

class Evacuee_phone_number(db.Model):
    evacuee_phone_number = db.Column(db.String(15), primary_key=True) 
    contact_name = db.Column(db.String(100))
    #
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'), nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    #
    evacuees = db.relationship('Evacuee', backref='evacuee_phone_number', lazy=True)
    evacuee_contacts = db.relationship('Evacuee_contacts', backref='evacuee_phone_number', lazy=True)

class Evacuee_emergency_contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_number = db.Column(db.String(10))
    evacuee_contact_relationship = db.Column(db.String(50))
    #
    evacuee_contact_name = db.Column(db.String(100), db.ForeignKey('evacuee_contact.name'), nullable=False)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), unique=True, nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'), unique=True, nullable=False)

class Evacuee_contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    type = db.Column(db.String(10), primary_key=True)
    #
    evacuee_phone_number = db.Column(db.String(10), db.ForeignKey('evacuee_phone_number.evacuee_phone_number'), unique=True, nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'), nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    #
    evacuee_emergency_contacts = db.relationship('Evacuee_emergency_contact', backref='evacuee_contact', lazy=True)
    evacuees = db.relationship('Evacuee', backref='evacuee_contact', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_fname = db.Column(db.String(30))
    employee_lname = db.Column(db.String(30))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    #date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), unique=True, nullable=False)
    address = db.Column(db.Integer, db.ForeignKey('employee.address'), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), unique=True, nullable=False)
    employee_contact_id = db.Column(db.Integer, db.ForeignKey('employee_contact.id'), unique=True, nullable=False)
    login_id = db.Column(db.String(30), db.ForeignKey('login.id'), unique=True, nullable=False)
    #
    evacuee_transfers = db.relationship('Evacuee_transfer', backref='employee', lazy=True)
    evaccenters = db.relationship('Evaccenter', backref='employee', lazy=True)
    roles = db.relationship('Role', backref='employee', lazy=True)
    employee_addresses = db.relationship('Employee_address', backref='employee', lazy=True)
    departments = db.relationship('Department', backref='employee', lazy=True)
    phone_numbers = db.relationship('Phone_Number', backref='employee', lazy=True)
    emergency_contacts = db.relationship('Emergency_contact', backref='employee', lazy=True)
    employee_contacts = db.relationship('Employee_Contact', backref='employee', lazy=True)
    logins = db.relationship('Login', backref='employee', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    role_description = db.Column(db.String(200), unique=True)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #
    employees = db.relationship('employee', backref='role', lazy=True)

class Employee_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #
    employees = db.relationship('Employee', backref='employee_address', lazy=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), unique=True)
    department_description = db.Column(db.String(200))
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #
    employees = db.relationship('Employee', backref='department', lazy=True)

class Employee_Phone_Number(db.Model):
    Phone_Number = db.Column(db.String(10), primary_key=True, unique=True)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #contact_name = db.Column(db.String(150), db.ForeignKey('contact.name'), nullable=False)
    #
    employees = db.relationship('Employee', backref='employee_phone_number', lazy=True)

class Employee_emergency_contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_emergency_contact = db.Column(db.String(10))
    #contact_name = db.Column(db.String(150))
    emergency_contact_relation = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #
    employee_contacts = db.relationship('Employee_Contact', backref='employee_emergency_contact', lazy=True)

class Employee_contact(db.Model): 
    id = db.Column(db.Integer, primary_key=True, unique=True)
    #contact_name = db.Column(db.String(150))
    contact_phone_number= db.Column(db.String(15), primary_key=True, unique=True, nullable=False)
    contact_type = db.Column(db.String(5), primary_key=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee_emergency_contact_id = db.Column(db.String(10), db.ForeignKey('employee_emergency_contact.id'), nullable=False)
    #
    employees = db.relationship('Employee', backref='employee_contact', lazy=True)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), primary_key=True, unique=True)
    password = db.Column(db.String(15), unique=True, nullable=False)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    #
    employees = db.relationship('Employee', backref='login', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name