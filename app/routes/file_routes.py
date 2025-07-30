from flask import Blueprint, render_template, send_file, current_app
from ..services.file_handler import is_valid_unique_string, get_safe_directory, list_real_files, get_download_file_path

file = Blueprint('file', __name__)

@file.route('/<unique_string>')
def serve_files(unique_string):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
    if not is_valid_unique_string(unique_string):
        return render_template('./pages/error.html'), 400

    directory_path = get_safe_directory(UPLOAD_FOLDER, unique_string)
    if not directory_path:
        return render_template('./pages/error.html'), 404

    real_files = list_real_files(directory_path)
    if not real_files:
        return render_template('./pages/error.html'), 404

    return render_template('./pages/download.html', files=real_files, unique_string=unique_string)

@file.route('/<unique_string>/<filename>', methods=['GET'])
def download_file(unique_string, filename):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
    file_path = get_download_file_path(UPLOAD_FOLDER, unique_string, filename)
    if not file_path:
        return render_template('./pages/error.html'), 404

    return send_file(file_path, as_attachment=True, download_name=filename)
