from flask import Blueprint, jsonify, request
from tables import UserAccount
from security import hash_password, generate_salt
from db_setup import db

register_blueprint = Blueprint('register_blueprint', __name__)


# Define your routes here, for example:
@register_blueprint.route('/register', methods=['POST'])
def register():
    # Get data from request
    data = request.get_json()
    user_email = data['email']
    user_pass = data['password']
    security_question_id = int(data['securityQuestion'])  # Convert to int
    answer = data['securityAnswer']

    # Here you would check if the email already exists and if not, add the user to the table
    # For example:
    user = UserAccount.query.filter_by(email=user_email).first()
    if user:
        return jsonify({'message': 'Registration Failed'}), 409
    else:
        salt = generate_salt()
        hashed_pw = hash_password(user_pass, salt)

        new_user = UserAccount(
            email=user_email,
            hashed_password=hashed_pw,
            salt=salt,
            security_question=security_question_id,
            security_answer=answer
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201