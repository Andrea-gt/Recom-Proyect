from flask import Flask
from config import Config
from neo4j import GraphDatabase

app = Flask(__name__)
app.config.from_object(Config)
driver = GraphDatabase.driver(uri='bolt://44.204.96.68:7687', auth=('neo4j','warship-service-fare'))
from app import routes