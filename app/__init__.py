from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Ініціалізація об'єктів
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name="config"):
    app = Flask(__name__)
    app.config.from_object(config_name)  # налаштування з об'єкта config

    # Ініціалізація db та migrate
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Імпортуємо блюпринти
        from .posts import post_bp
        from .users import bp as user_bp

        # Реєструємо блюпринти
        app.register_blueprint(post_bp)
        app.register_blueprint(user_bp, url_prefix="/users")

    return app
