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
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'), nullable=False)
    supplies = db.relationship('Supply', backref='evaccenter', lazy=True)
    evacuees = db.relationship('Evacuee', backref='evaccenter', lazy=True)
    evacuee_transfers = db.relationship('Evacuee_Transfer', backref='evaccenter', lazy=True)
    
class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(100))
    supply_count = db.Column(db.Integer)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)

class Evacuee_Transfer(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    evac_id_1 = db.Column(db.Integer, unique=True)
    evac_id_2 = db.Column(db.Integer, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.id'),nullable=False)

class Evacuee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evacuee_phone_number = db.Column(db.Integer, unique=True) #fk
    evacuee_contact_id = db.Column(db.Integer, unique=True) #fk
    evacuee_address_id = db.Column(db.Integer) #fk
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    evacuee_relationship = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.id'), nullable=False)
    
class Evacuee_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evacuee_id = db.Column(db.Integer, unique=True, nullable=False) #fk
    evac_id = db.Column(db.Integer, unique=True, nullable=False) #fk
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(6))

class Evacuee_phone_number(db.Model):
    Evacuee_phone_numbe = db.Column(db.String(15), primary_key=True) 
    evacuee_id = db.Column(db.Integer, unique=True, nullable=False) #fk
    evac_id = db.Column(db.Integer, unique=True, nullable=False) #fk
    contact_name = db.Column(db.String(100))

class Evacuee_emergency_contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, nullable=False) #fk
    evacuee_id = db.Column(db.Integer, nullable=False) #fk
    contact_name = db.Column(db.String(100)) #fk
    evacuee_contact_relationship = db.Column(db.String(50))

class Evacuee_contact(db.Model):
    evacuee_contact_name = db.Column(db.Integer, primary_key=True)
    evacuee_phone_number = db.Column(db.String(15)) #fk
    evacuee_id = db.Column(db.Integer, nullable=False) #fk
    evac_id = db.Column(db.Integer,nullable=False) #fk

class Employee(db.Model): #many to many?
    id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, nullable=False) #fk
    employee_address = db.Column(db.Integer, nullable=False) #fk
    department_id = db.Column(db.Integer) #fk
    role_id = db.Column(db.Integer) #fk
    employee_phone_number = db.Column(db.String(15), unique=True) #fk
    employee_contact_id = db.Column(db.Integer) #fk
    username = db.Column(db.String(30), unique=True) #fk
    password = db.Column(db.String(15), unique=True) 
    employee_fname = db.Column(db.String(30))
    employee_lname = db.Column(db.String(30))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    evacuee_transfers = db.relationship('Evacuee_transfer', backref='employee', lazy=True)
    evaccenters = db.relationship('Evaccenter', backref='employee', lazy=True)
    #
    roles = db.relationship('Role', backref='employee', lazy=True)
    employee_addresses = db.relationship('Employee_address', backref='employee', lazy=True)
    departments = db.relationship('Department', backref='employee', lazy=True)
    phone_numbers = db.relationship('Phone_Number', backref='employee', lazy=True)
    emergency_contacts = db.relationship('Emergency_contact', backref='employee', lazy=True)
    contacts = db.relationship('Contact', backref='employee', lazy=True)
    logins = db.relationship('Login', backref='employee', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    role_description = db.Column(db.String(200), unique=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

class Employee_address(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), unique=True)
    department_description = db.Column(db.String(200))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

class Phone_Number(db.Model):
    Phone_Number = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(150), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

class Employee_emergency_contact(db.Model):
    __tablename__ = 'employee_emergency_contact'
    id = db.Column(db.Integer, primary_key=True)
    employee_emergency_contact = db.Column(db.String(10))
    emergency_contact_relation = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    contacts = db.relationship('Contact', backref='employee_emergency_contact', lazy=True)

class Contact(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    contact_phone_number= db.Column(db.String(15), primary_key=True, unique=True, nullable=False)
    contact_type = db.Column(db.String(5), primary_key=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee_emergency_contact_id = db.Column(db.String(10), db.ForeignKey('employee_emergency_contact.id'), nullable=False)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), primary_key=True, unique=True)
    password = db.Column(db.String(15), unique=True, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name