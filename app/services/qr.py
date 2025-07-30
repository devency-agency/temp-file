from flask import current_app
import qrcode
from io import BytesIO
from PIL import Image
import base64

"""
QR code generation utility.

Generates a QR code image based on the given data and Flask app configuration,
and returns it as a base64-encoded data URI for use in web applications.
"""

def generate_qr_code_base64(data: str) -> str:
    """
    Generates a base64-encoded QR code image from the given data.

    The QR code's size and format are taken from the Flask app config:
        - QR_CODE_SIZE: (int) size in pixels (e.g. 256)
        - QR_CODE_FORMAT: (str) format (e.g. "PNG")

    Args:
        data (str): The string to encode into the QR code.

    Returns:
        str: A base64-encoded data URI representing the QR code image.
    """
    size = current_app.config.get('QR_CODE_SIZE', 256)
    format = current_app.config.get('QR_CODE_FORMAT', 'PNG')

    qr = qrcode.make(data).resize((size, size), Image.Resampling.LANCZOS)
    buffered = BytesIO()
    qr.save(buffered, format=format)

    encoded = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{encoded}"
