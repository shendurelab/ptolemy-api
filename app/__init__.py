from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_ECHO'] = False  # os.environ['FLASK_ENV'] == 'development'

app.secret_key = os.environ['SECRET_KEY']

# fmt: off
from app.model import get_cell, get_gene
db = SQLAlchemy(app)
cell = get_cell(db.Model)
gene = get_gene(db.Model)
migrate = Migrate(app, db)
from app import routes, schema
# fmt: on
