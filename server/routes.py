from flask import jsonify, request
from app import db, Employee, app
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

CORS(app)

app.config['JWT_SECRET_KEY'] = 'kjsfhiuyrnAUTdjhddjlkjfeadDAlHgDM'

@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        # Check if all required fields are provided and not empty
        required_fields = ['first_name', 'last_name', 'identification_number', 'date_of_birth', 'contact', 'date_of_employment', 'department_number', 'contract_period']
        for field in required_fields:
            if field not in request.form or not request.form[field]:
                return jsonify({'error': f'Missing or empty required field: {field}'}), 400
        
        # Extracting uploaded files
        uploaded_files = {}
        for field_name in ['passport', 'id_copy', 'chief_letter', 'clearance_letter', 'referees']:
            uploaded_file = request.files.get(field_name)
            if not uploaded_file:
                return jsonify({'error': f'Missing document file: {field_name}'}), 400
            uploaded_files[field_name] = uploaded_file

        # Save uploaded files
        uploaded_filenames = {}
        for field_name, uploaded_file in uploaded_files.items():
            filename = secure_filename(uploaded_file.filename)
            uploaded_filenames[field_name] = filename
            uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                uploaded_file.save(uploaded_file_path)
            except Exception as e:
                return jsonify({'error': f'Error saving {field_name} file: {str(e)}'}), 500

        # Create new employee instance
        new_employee_data = {field: request.form[field] for field in required_fields}
        new_employee_data.update(uploaded_filenames)  
        new_employee = Employee(**new_employee_data)

        # Add employee to database
        try:
            db.session.add(new_employee)
            db.session.commit()
        except Exception as e:
            # If an error occurs during database operations, delete uploaded files to prevent orphaned files
            for filename in uploaded_filenames.values():
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            return jsonify({'error': f'Error adding employee to database: {str(e)}'}), 500

        return jsonify({'message': 'Employee added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
