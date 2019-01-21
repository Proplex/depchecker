import os
from flask import Flask, render_template, current_app
from flask_bootstrap import Bootstrap
from models.data import Data

DEBUG = os.getenv('DEBUG', False)

app = Flask(__name__)
Bootstrap(app)
store = Data()

@app.route('/')
def index():
  deps = store.get_data()
  release_list = sorted(deps['releases'], key=lambda k: k['name']) 
  kit_list = sorted(deps['kits'], key=lambda k: k['name']) 
  return render_template("index.jinja", releases=release_list, kits=kit_list)

@app.route('/update_git')
def update_git():
  store.update_versions()
  return "OK"
  

if __name__ == "__main__":
  store.load_config()
  if not DEBUG:
    # automatically load config if not debugging. this is to prevent
    # massive API hits caused each time a src file edit is saved to disk.
    # to update dependency info while developing, hit the `/update_git`
    # endpoint
    store.update_versions()
  app.run(host='0.0.0.0', port=8080, debug=DEBUG)