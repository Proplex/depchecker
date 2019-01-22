import os, json, yaml
from flask import Flask, render_template, current_app, request, send_file
from flask_bootstrap import Bootstrap
from flask_basicauth import BasicAuth
from models.data import Data

# get envvars
DEBUG = os.getenv('DEBUG', False)
AUTH_USER = os.getenv('BASIC_AUTH_USERNAME', 'bober')
AUTH_PASS = os.getenv('BASIC_AUTH_PASSWORD', 'pleasechange')

# bootstrap the app
app = Flask(__name__)

# configure app before libraries
app.config['BASIC_AUTH_USERNAME'] = AUTH_USER
app.config['BASIC_AUTH_PASSWORD'] = AUTH_PASS

# attach libraries
Bootstrap(app)
basic_auth = BasicAuth(app)
store = Data()

@app.route('/')
def index():
  deps = store.get_data()
  print(deps)
  return render_template("index.jinja", releases=deps['releases'], kits=deps['kits'])

@app.route('/update_git')
@basic_auth.required
def update_git():
  store.update_versions()
  return "OK"

@app.route('/update_version', methods=['POST'])
@basic_auth.required
def update_version():
  if request.is_json:
    data = request.get_json()
    print(data)
    try: # sanity check just a wee bit
      for kit, kit_info in data['kits'].items():
        print("Updating kit \"" + kit + "\".")
        for release, release_info in data['kits'][kit]['releases'].items():
          if 'version' in release_info:
            continue
    except:
      print("Received invalid update payload.")
      return "MALFORMED", 400

    store.update_data(data)
    return "OK"
  return "BAD", 400

@app.route('/get_config')
def get_config():
  return send_file(store.config_file, "depchecker_config.yml")

@app.route('/update_config', methods=['POST'])
@basic_auth.required
def update_config():
  try:
    # check to see if this is a valid YAML config.
    test_yaml = yaml.safe_load(request.get_data())
    # make sure uploaded YAML file is current. don't want to roll back.
    if test_yaml['last_updated'] <= store.get_data()['last_updated']:
      print("File uploaded is an out-of-date config.")
      return "OUT-OF-DATE", 400
  except:
    print("Didn't get a valid YML file")
    return "BAD", 400
  store.write_config_raw(request.get_data())
  return "OK"

if __name__ == "__main__":
  store.load_config()
  if not DEBUG:
    # only auto load config if not debugging. this is to prevent
    # massive API hits caused each time a src file edit is saved to disk.
    # to update dependency info while developing, hit the `/update_git`
    # endpoint
    store.update_versions()
  app.run(host='0.0.0.0', port=8080, debug=DEBUG)