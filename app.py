import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from models import get_latest, load_config

DEBUG = os.getenv('DEBUG', False)
CONFIG = os.getenv('DEPCHECK_CONFIG', "example_config.yml")

app = Flask(__name__)
Bootstrap(app)
dependencies = {}


@app.route('/')
def index():
  return render_template("index.jinja", releases=dependencies['releases'], kits=dependencies['kits'])

@app.route('/update_git')
def update_git():
  load_config(CONFIG)
  return "OK"

if __name__ == "__main__":
    # load configuration
    dependencies = load_config(CONFIG)
    app.run(host='0.0.0.0', port=8080, debug=DEBUG)