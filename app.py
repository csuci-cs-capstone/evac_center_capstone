#appconfig section
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaccenters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#database section
class EvacCenter(db.Model):
    evac_id = db.Column(db.Integer, primary_key=True)
    supply_id = db.Column(db.Integer, unique=True)
    employee_id = db.Column(db.Integer, unique=True)
    evacuee_id = db.Column(db.Integer, unique=True)
    evac_num = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(6), nullable=False)
    #supplies = db.relationship('Supply', backref='EvacCenter', lazy=True)

class Supply(db.Model):
    supply_id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, db.ForeignKey('evac_id'),nullable=False)
    supply_name = db.Column(db.String(100))
    supply_count = db.Column(db.Integer)

class Evacuee_Transfer(db.Model):
    transfer_id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, db.ForeignKey('evac_id'),nullable=False)
    evac_id_1 = db.Column(db.Integer, unique=True)
    evac_id_2 = db.Column(db.Integer, unique=True)
    evacuee_id = db.Column(db.Integer, unique=True)
    employee_id = db.Column(db.Integer, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Evacuee(db.Model):
    evacuee_id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, db.ForeignKey('evac_id'),nullable=False)
    address_id = db.Column(db.Integer, nullable=False)
    evacuee_phone_number = db.Column(db.Integer, unique=True)
    evacuee_contact_id = db.Column(db.Integer, unique=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    evacuee_relationship = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Evacuee_address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    evacuee_id = db.Column(db.Integer, unique=True, nullable=False)
    evac_id = db.Column(db.Integer, unique=True, nullable=False)
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(6))

class Evacuee_phone_number(db.Model):
    Evacuee_phone_number = db.Column(db.String(15), primary_key=True)
    evacuee_id = db.Column(db.Integer, unique=True, nullable=False)
    evac_id = db.Column(db.Integer, unique=True, nullable=False)
    contact_name = db.Column(db.String(100))

class evacuee_emergency_contact(db.Model):
    evacuee_contact_id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, nullable=False)
    evacuee_id = db.Column(db.Integer, nullable=False)
    contact_name = db.Column(db.String(100))
    evacuee_contact_relationship = db.Column(db.String(50))

class Evacuee_contact(db.Model):
    evacuee_contact_name = db.Column(db.Integer, primary_key=True)
    evacuee_phone_number = db.Column(db.String(15))
    evacuee_id = db.Column(db.Integer, nullable=False)
    evac_id = db.Column(db.Integer,nullable=False)

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    evac_id = db.Column(db.Integer, nullable=False)
    employee_address = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    employee_phone_number = db.Column(db.String(15), unique=True)
    employee_contact_id = db.Column(db.Integer)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(15), unique=True)
    employee_fname = db.Column(db.String(30))
    employee_lname = db.Column(db.String(30))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    role_name = db.Column(db.String(50), unique=True)
    role_description = db.Column(db.String(200), unique=True)

class Employee_address(db.Model):
    Employee_address = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(50),nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)

class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    department_name = db.Column(db.String(50), unique=True)
    department_description = db.Column(db.String(200))

class Phone_Number(db.Model):
    Phone_Number = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)

class Emergency_contact(db.Model):
    emergency_contact_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    contact_name = db.Column(db.String(150), nullable=False)
    emergency_contact_relationship = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    contact_name = db.Column(db.Integer, primary_key=True)
    contact_phone_number= db.Column(db.String(15), unique=True, nullable=False)
    contact_type = db.Column(db.string(5), nullable=False)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Login(db.Model):
    login_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=True, nullable=False)

    def __rep__(self):
        return '<Name %r>' % self.name