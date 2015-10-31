
from flask import Flask
from flask.ext.mongoengine import MongoEngine

import config


app = Flask(__name__)
app.config.from_object(config)

db = MongoEngine(app)

# Jinja2 templates commenting tags
app.jinja_env.line_statement_prefix = '#'
app.jinja_env.line_comment_prefix = '##'


