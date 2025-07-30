from flask import Flask
from flask_jwt_extended import JWTManager
from .routes import main_routes, api_routes, file_routes, admin_routes
from .services.directory_manager import DirectoryManager
from .services.token_handler import init_app

jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder='templates/static', static_url_path='/static')
    app.config.from_object('config.Config')

    # Initialize JWT
    jwt.init_app(app)

    # Initialize Cache
    init_app(app)

    # Register blueprints
    app.register_blueprint(main_routes.main)
    app.register_blueprint(api_routes.api)
    app.register_blueprint(file_routes.file)
    app.register_blueprint(admin_routes.admin)

    # Start directory manager
    directory_manager = DirectoryManager(
        folder_path=app.config['UPLOAD_FOLDER'],
        interval=app.config['DIRECTORY_CLEANUP_INTERVAL'],
        lifetime=app.config['DIRECTORY_LIFETIME']
    )
    directory_manager.start()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
