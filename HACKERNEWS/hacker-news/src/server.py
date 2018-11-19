import logging

from dotenv import load_dotenv
from flask import Flask, request

from controllers.user import user
from controllers.post import post
from database.base import Base

load_dotenv(verbose=True)
logging.basicConfig(
    level="DEBUG",
    format="%(levelname)s %(asctime)s %(message)s",
    datefmt="%Y%m%d %I:%M:%S %p",
)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user)
    app.register_blueprint(post)
    return app
    

if __name__ == "__main__":
    Base.metadata.create_all()
    app = create_app()
    app.run(debug=True)
