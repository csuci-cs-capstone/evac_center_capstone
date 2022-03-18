from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaccenters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class EvacCenter(db.Model):
    evac_id = db.Column(db.Integer, primary_key=True)
    supplies_id = db.Column
    employee_id = db.Column
    evacuee_id = db.Column
    evac_num = db.Column
    name = db.Column
    city = db.Column
    zipcode = db.Column

class Supplies(db.Model):
    supplies_id = db.Column
    evac_id = db.Column
    supply_name = db.Column
    supply_count = db.Column

class Evacuee_Transfer(db.Model):
    transfer_id = db.Column
    evac_id = db.Column
    evac_id_1 = db.Column
    evac_id_2 = db.Column
    evacuee_id = db.Column
    employee_id = db.Column
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Evacuee(db.Model):
    evacuee_id = db.Column
    evac_id = db.Column
    evacuee_address = db.Column
    evacuee_phone_number = db.Column
    evacuee_contact_id = db.Column
    fname = db.Column
    lname = db.Column
    email = db.Column
    evacuee_relationship = db.Column
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Evacuee_address(db.Model):
    evacuee_address = db.Column
    evacuee_id = db.Column
    evac_id = db.Column
    name = db.Column
    street = db.Column
    city = db.Column
    zipcode = db.Column

class Evacuee_phone_number(db.Model):
    Evacuee_phone_number = db.Column
    evacuee_id = db.Column
    evac_id = db.Column
    contact_name = db.Column

class evacuee_emergency_contact(db.Model):
    evacuee_contact_id = db.Column
    evac_id = db.Column
    evacuee_id = db.Column
    contact_name = db.Column
    e_contact_relationship = db.Column

class Evacuee_contact(db.Model):
    evacuee_contact_name = db.Column
    phone_num_type = db.Column
    contact_type = db.Column
    evacuee_id = db.Column
    evac_id = db.Column

class Employee(db.Model):
    employee_id = db.Column
    evac_id = db.Column
    employee_address = db.Column
    department_id = db.Column
    role_id = db.Column
    employee_phone_number = db.Column
    employee_contact_id = db.Column
    username = db.Column
    password = db.Column
    fname = db.Column
    lname = db.Column
    dob = db.Column
    age = db.Column
    email = db.Column
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Role(db.Model):
    role_id = db.Column
    employee_id = db.Column
    role_name = db.Column
    role_description = db.Column

class Employee_address(db.Model):
    Employee_address = db.Column
    employee_id = db.Column
    name = db.Column
    street = db.Column
    city = db.Column
    zipcode = db.Column

class Department(db.Model):
    department_id = db.Column
    employee_id = db.Column
    department_name = db.Column
    department_description = db.Column

class Phone_Number(db.Model):
    Phone_Number = db.Column
    employee_id = db.Column
    contact_name = db.Column

class Emergency_contact(db.Model):
    emergency_contact_id = db.Column
    employee_id = db.Column
    contact_name = db.Column
    emergency_contact_relationship = db.Column
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    contact_name = db.Column
    phone_number_type = db.Column
    contact_type = db.Column
    employee_id = db.Column
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Login(db.Model):
    login_id = db.Column
    employee_id = db.Column
    username = db.Column
    password = db.Column

    def __rep__(self):
        return '<Name %r>' % self.name