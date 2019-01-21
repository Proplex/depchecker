import os, json, yaml, urllib.request, json, sys
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from models import get_latest

DEBUG = os.getenv('DEBUG', False)

app = Flask(__name__)
Bootstrap(app)
dep_status = {}


@app.route('/')
def index():
  return render_template("index.jinja", releases=dep_status['releases'], kits=dep_status['kits'])


if __name__ == "__main__":
    # load configuration
    with open('example_config.yml') as config:
      dep_status = yaml.safe_load(config)
      for k_index, kit in enumerate(dep_status['kits']):
        for r_index, release in enumerate(kit['releases']):
          print("Checking release \"" + release['name'] + "\".")
          dep_status['kits'][k_index]['releases'][r_index]['latest_version'] = get_latest(release['git'])
    print("Loaded dependencies: " + str(dep_status))
    app.run(host='0.0.0.0', port=8080, debug=DEBUG)