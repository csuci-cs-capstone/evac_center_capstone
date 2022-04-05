#appconfig section
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///evaccenters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#database section
class Evaccenter(db.Model):
    evaccenter_id = db.Column(db.Integer, primary_key=True)
    evac_num = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(6), nullable=False)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)
    #
    supplies = db.relationship('Supply', backref='evaccenter', lazy=True)
    evacuee_transfers = db.relationship('Evacuee_Transfer', backref='evaccenter', lazy=True)
    evacuee_phone_numbers = db.relationship('Evacuee_phone_number', backref='evaccenter', lazy=True)
    evacuee_emergency_contacts = db.relationship('Evacuee_emergency_contact', backref='evaccenter', lazy=True)
    evacuee_contacts = db.relationship('Evacuee_contact', backref='evaccenter', lazy=True)

    def __repr__(self):
        return '<evac_num %r>' % self.evac_num

class Supply(db.Model):
    supply_id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(100))
    supply_count = db.Column(db.Integer)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), nullable=False)
    
    def __repr__(self):
        return '<supply_name %r>' % self.supply_name, self.supply_count

class Evacuee_Transfer(db.Model):
    evacuee_transfer_id = db.Column(db.Integer, primary_key=True)
    evac_id_1 = db.Column(db.Integer, unique=True)
    evac_id_2 = db.Column(db.Integer, unique=True)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)

    def __repr__(self):
        return '<Evacuee_transfer %r>' % self.evacuee_transfer_id, self.evac_id_1, self.evac_id_2, self.date_added

class Evacuee(db.Model):
    evacuee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    evacuee_relationship = db.Column(db.String(50))
    #
    evacuee_phone_number = db.Column(db.Integer, db.ForeignKey('evacuee_phone_number.evacuee_phone_number'), nullable=False)
    evacuee_contact_id = db.Column(db.Integer, db.ForeignKey('evacuee_contact.evacuee_contact_id'), unique=True, nullable=False)
    evacuee_address_id = db.Column(db.Integer, db.ForeignKey('evacuee_address.evacuee_address_id'), nullable=False)
    evacuee_emergency_contact = db.Column(db.String(50), db.ForeignKey('evacuee_emergency_contact.evacuee_emergency_contact_id'), nullable = False)
    #
    evac_nums = db.relationship('Evaccenter', backref='evacuee', lazy=True)

    def __repr__(self):
        return '<Evacuee %r>' % self.name, self.email, self.date_added

class Evacuee_address(db.Model):
    evacuee_address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(6))
    #
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), unique=True, nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), unique=True, nullable=False)

    def __repr__(self):
        return '<Evacuee_address %r>' % self.street

class Evacuee_phone_number(db.Model):
    evacuee_phone_id = db.Column(db.Integer, primary_key=True) 
    evacuee_phone_number = db.Column(db.String(15)) 
    contact_name = db.Column(db.String(100))
    #
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), nullable=False)

    def __repr__(self):
        return '<Evacuee_phone_number %r>' % self.evacuee_phone_number, self.contact_name

class Evacuee_emergency_contact(db.Model):
    evacuee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    contact_number = db.Column(db.String(10))
    evacuee_contact_relationship = db.Column(db.String(50))
    #
    evacuee_contact_name = db.Column(db.String(100), db.ForeignKey('evacuee_contact.name'), nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), unique=True, nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), unique=True, nullable=False)

    def __repr__(self):
        return '<Employee_emergency_contact %r>' % self.contact_number, self.evacuee_contact_relationship

class Evacuee_contact(db.Model):
    evacuee_contact_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), primary_key=True)
    type = db.Column(db.String(10), primary_key=True)
    #
    evacuee_phone_number = db.Column(db.String(10), db.ForeignKey('evacuee_phone_number.evacuee_phone_number'), unique=True, nullable=False)
    evacuee_id = db.Column(db.Integer, db.ForeignKey('evacuee.evacuee_id'), nullable=False)
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), nullable=False)
    #
    evacuee_emergency_contacts = db.relationship('Evacuee_emergency_contact', backref='evacuee_contact', lazy=True)

    def __repr__(self):
        return '<Evacuee_contact %r>' % self.name, self.type

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    dob = db.Column(db.String(10))
    age = db.Column(db.Integer)
    email = db.Column(db.String(200), unique=True)
    #
    evaccenter_id = db.Column(db.Integer, db.ForeignKey('evaccenter.evaccenter_id'), unique=True, nullable=False)
    employee_phone_number_id = db.Column(db.String(10), db.ForeignKey('employee_phone_number.employee_phone_number_id'), unique=True)
    address_id = db.Column(db.Integer, db.ForeignKey('employee_address.employee_address_id'), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), unique=True, nullable=False)
    employee_contact_id = db.Column(db.Integer, db.ForeignKey('employee_contact.employee_contact_id'), unique=True, nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('user.user_id'), unique=True, nullable=False)
    emergency_contact_id = db.Column(db.String(10), db.ForeignKey('employee_emergency_contact.employee_emergency_contact_id'), nullable=False)

    def __repr__(self):
        return '<Employee %r>' % self.name, self.email, self.date_added

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    role_description = db.Column(db.String(200), unique=True)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.role_name

class Employee_address(db.Model):
    employee_address_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)

    def __repr__(self):
        return '<Employee_address %r>' % self.name, self.street, self.city, self.zipcode

class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), unique=True)
    department_description = db.Column(db.String(200))
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)

    def __repr__(self):
        return '<Department %r>' % self.department_name

class Employee_phone_number(db.Model):
    employee_phone_number_id = db.Column(db.Integer, primary_key=True)
    employee_phone_number = db.Column(db.String(15))
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    employee_contact_id = db.Column(db.Integer, db.ForeignKey('employee_contact.employee_contact_id'), nullable=False)

    def __repr__(self):
        return '<Employee_phone_number %r>' % self.employee_phone_number_id, self.employee_phone_numbe

class Employee_emergency_contact(db.Model):
    employee_emergency_contact_id = db.Column(db.Integer, primary_key=True)
    employee_emergency_number = db.Column(db.String(10))
    contact_name = db.Column(db.String(150))
    emergency_contact_relation = db.Column(db.String(50))
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    #
    employee_contact_names = db.relationship('Employee_contact', backref='employee_emergency_contact', lazy=True)

    def __repr__(self):
        return '<Employee_emergency_contact %r>' % self.employee_emergency_number, self.contact_name

class Employee_contact(db.Model): 
    employee_contact_id = db.Column(db.Integer, primary_key=True, unique=True)
    employee_contact_name = db.Column(db.String(150))
    contact_phone_number= db.Column(db.String(15), primary_key=True, unique=True, nullable=False)
    contact_type = db.Column(db.String(5), primary_key=True, nullable=False)
    #
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    emergency_contact_id = db.Column(db.String(10), db.ForeignKey('employee_emergency_contact.employee_emergency_contact_id'), nullable=False)

    def __repr__(self):
        return '<Employee_contact %r>' % self.contact_name

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

if __name__ == "__main__":
    app.run() 
    #write user models here for testing
