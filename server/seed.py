from app import db, Employee, Assignment, app
from datetime import datetime
from faker import Faker
import os

fake = Faker()


def create_fake_assignment(count=5):
    with app.app_context():

        assignment_data = [
            {'name': 'Security', 'number': 1},
            {'name': 'Garage', 'number': 2},
            {'name': 'Finance', 'number': 3},
            {'name': 'Sales', 'number': 4},
            {'name': 'Hygiene and Santitaion', 'number': 5},

        ]

        for assignment_data in assignment_data:
            assignment = Assignment(
                assignmentNumber=assignment_data['number'],
                assignmentDepartment=assignment_data['name'],
                DepartmentHead=fake.name(),
                Location=fake.city()
            )
            db.session.add(assignment)

        db.session.commit()


def upload_file(filename):
    # For demonstration, print the filename
    print(f"Uploading file: {filename}")


def create_fake_employee(count=15):
    with app.app_context():
        department_numbers = [1, 2, 3, 4, 5]

        for _ in range(count):
            firstname = fake.first_name()
            lastname = fake.last_name()
            IdentificationNumber = fake.unique.random_number(8)
            Dateofbirth = fake.date_of_birth(minimum_age=18, maximum_age=65)
            Contact = fake.unique.random_number(10)
            DateOfEmployement = fake.date_time_between(
                start_date='-5y', end_date='now')
            DepartmentNumber = fake.random_element(elements=department_numbers)
            ContractPeriod = fake.random_int(min=1, max=5)
            passport_filename = f"{firstname}_{lastname}_passport.jpg"
            id_copy_filename = f"{firstname}_{lastname}_id_copy.pdf"
            chief_letter_filename = f"{firstname}_{lastname}_chief_letter.pdf"
            clearance_letter_filename = f"{firstname}_{lastname}_clearance_letter.pdf"
            referees_filename = f"{firstname}_{lastname}_referees.pdf"

            employee = Employee(
                FirstName=firstname,
                LastName=lastname,
                IdentificationNumber=IdentificationNumber,
                DateOfBirth=Dateofbirth,
                Contact=Contact,
                DateOfEmployement=DateOfEmployement,
                DepartmentNumber=DepartmentNumber,
                ContractPeriod=ContractPeriod,
                Passport=passport_filename,
                IdCopy=id_copy_filename,
                ChiefLetter=chief_letter_filename,
                ClearanceLetter=clearance_letter_filename,
                Referees=referees_filename
            )
            db.session.add(employee)

            # Upload documents
            upload_file(passport_filename)
            upload_file(id_copy_filename)
            upload_file(chief_letter_filename)
            upload_file(clearance_letter_filename)
            upload_file(referees_filename)

        db.session.commit()


if __name__ == "__main__":
    create_fake_employee()
    create_fake_assignment()

    print("Seeding completed successfully.")
