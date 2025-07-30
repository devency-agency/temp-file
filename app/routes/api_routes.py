from flask import request, jsonify, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.token_handler import generate_token, verify_token
from ..services.qr import generate_qr_code_base64
from ..services.captcha import verify_recaptcha
from ..services.file_handler import create_random_upload_directory, save_uploaded_file
from ..services.log_handler import setup_logging
import os
import json
import random

api = Blueprint('api', __name__)
# logging logic is not implemented in this public verison
logger = setup_logging()

def get_client_ip():
    """
    Helper function to retrieve the client's IP address from the request.
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

@api.route('/api/captcha', methods=['POST'])
def captcha():
    try:
        g_recaptcha_response = request.json.get('g-recaptcha-response')
        if not g_recaptcha_response or not verify_recaptcha(g_recaptcha_response):
            return jsonify({'status': 'error', 'message': 'Invalid captcha'}), 400
        
        return jsonify({'status': 'success', 'access_token': generate_token()}), 200
    except Exception:
        return jsonify({'status': 'error', 'message': 'Internal error'}), 500

@api.route('/api/upload', methods=['POST'])
@jwt_required()
def upload():
    try:
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
        if not verify_token(get_jwt_identity()):
            return jsonify({'status': 'error', 'message': 'Invalid or expired token'}), 401

        if 'files' not in request.files or not request.files.getlist('files'):
            return jsonify({'status': 'error', 'message': 'No files provided'}), 400

        files = request.files.getlist('files')
        random_str, random_dir = create_random_upload_directory(UPLOAD_FOLDER)

        for file in files:
            encoded_filename, error = save_uploaded_file(file, random_dir)
            if error:
                return jsonify({'status': 'error', 'message': error}), 400

        qr_code_url = f"https://{request.host}/{random_str}"

        return jsonify({
            "status": "success",
            "message": "Upload successful",
            "url": random_str,
            "qr": generate_qr_code_base64(qr_code_url)
        }), 200
    except Exception:
        return jsonify({'status': 'error', 'message': 'Internal error'}), 500

@api.route('/api/contact', methods=['POST'])
def contact():
    try:
        user_ip = get_client_ip()

        try:
            data = request.get_json()
            if not data:
                raise ValueError("Empty JSON payload")
        except Exception as e:
            return jsonify({'error': 'Invalid or missing JSON payload'}), 400

        name, email, message, g_recaptcha_response = data.get('name'), data.get('email'), data.get('message'), data.get('g-recaptcha-response')

        if not all([name, email, message, g_recaptcha_response]):
            return jsonify({'error': 'Missing fields'}), 400
        
        if not verify_recaptcha(g_recaptcha_response):
            return jsonify({'error': 'Invalid captcha'}), 400

        """Saving messages is hidden in this public version"""
        # ..
        # ..

        return jsonify({'message': 'Contact message saved successfully'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Internal error'}), 500
