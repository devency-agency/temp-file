import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER_DIR = os.path.join(BASE_DIR, 'uploads')

class Config:
    DEBUG_MODE = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 864000
    QR_CODE_SIZE = 150
    QR_CODE_FORMAT = 'PNG'
    CAPTCHA_SECRET_KEY = os.getenv('CAPTCHA_SECRET_KEY')
    DIRECTORY_CLEANUP_INTERVAL = 3600
    DIRECTORY_LIFETIME = 50400
