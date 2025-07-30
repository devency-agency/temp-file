from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def ui_index():
    return render_template('./pages/index.html')

@main.route('/contact-us')
def ui_contact():
    return render_template('./pages/contact.html')

@main.route('/tos')
def ui_tos():
    return render_template('./pages/tos.html')

@main.route('/about')
def ui_about():
    return render_template('./pages/about.html')

@main.route('/admin/dashboard')
def ui_admin():
    return render_template('./pages/admin.html')

@main.route('/admin/login')
def ui_admin_login():
    return render_template('./pages/admin_login.html')