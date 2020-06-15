from flask import Flask
from .config import Development

app = Flask(__name__)
app.config.from_object(Development)

# import controllers
from . import controllers