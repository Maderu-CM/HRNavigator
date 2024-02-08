from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Relationship

app= Flask(__name__)

#configure SQLALCHEMY
app.config ['SQLAlCHEMY_DATABASE_URI']= os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLAlCHEMY_MODIFICATIONS_TRACKING']= False

#Initialize SQLAlchemy
db= SQLAlchemy(app)
CORS(app)

migrate=Migrate(app,db)

#models

class Employee (db.Model):
    __tablename__ = 'employee'

    id= db.Column(db.Integer, primary_key=True, nullable= False,unique=True)
    FirstName= db.Column(db.String, nullable=False )
    LastName= db.Column(db.String,nullable=False)
    IdentificationNumber= db.Column(db.Integer, nullable=False,unique=True)
    DateOfBirth= db.Column(db.DateTime, nullable=False)
    Contact= db.Column(db.Integer, nullable=False,unique= False)
    DateOfEmployement= db.Column(db.DateTime, nullable=False)
    DepartmentNumber= db.Column(db.Integer, nullable=False)
    ContractPeriod= db.Column(db.Integer,nullable=False)
    Passport= db.Column (db.String,nullable=False)
    IdCopy=db.Column (db.String, nullable=False)
    ChiefLetter= db.Column(db.String, nullable=False)
    ClearanceLetter= db.Column(db.String, nullable=False)
    Referees= db.Column(db.String, nullable=False)

    #relationship
    assignment= db.relationship('Assignment', backref='assignment_relation',lazy= True)

class Assignment (db.Model):
    __tablename__= 'assignment'

    DepartmentNumber =db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    Department= db.Column(db.String, nullable=False,unique=True)
    DepartmentHead= db.Column(db.String,nullable=False)
    Location= db.Column(db.String, nullable=False)

#relationship
    employees= db.relationship('Employee',backref='employee_relation',lazy=True,cascade='all, delete-orphan')

    
if __name__== '__main__':
    app.run(debug=True)