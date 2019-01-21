import json, os, sys, yaml
from threading import Lock
from .fetcher import get_latest

class Data():

  def __init__(self):
    self.config_file = os.getenv('DEPCHECK_CONFIG', "example_config.yml")
    self.internal_data = {'releases': [], 'kits': []}
    self.file_mutex = Lock()
    self.data_mutex = Lock()

  # load configuration from disk to memory
  def load_config(self):
    with self.file_mutex:
      with self.data_mutex:
        with open(self.config_file) as config:
          self.internal_data = yaml.safe_load(config)
          print("Successfully loaded configuration to memory.")

  def write_config(self):
    with self.file_mutex:
      with self.data_mutex:
        with open(self.config_file, 'w') as config:
          config.write(yaml.safe_dump(self.internal_data))
          print("Successfully saved configuration to disk.")

  def update_data(self, data: dict):
    with self.data_mutex:
      self.internal_data.update(data)

  def update_versions(self):
    seen_releases = {} # cache releases that are the same across kits
    with self.data_mutex:
      for k_index, kit in enumerate(self.internal_data['kits']):
        for r_index, release in enumerate(kit['releases']):
          if release['git'] in seen_releases:
            print("Using cached information for \"" + release['name'] + "\".")
            self.internal_data['kits'][k_index]['releases'][r_index]['latest_version'] = seen_releases[release['git']]
          else:
            print("Checking release \"" + release['name'] + "\".")
            latest_release = get_latest(release['git'])
            seen_releases[release['git']] = latest_release
            self.internal_data['kits'][k_index]['releases'][r_index]['latest_version'] = latest_release
      print("Loaded dependencies: " + str(self.internal_data))
  
  def get_data(self) -> dict:
    with self.data_mutex:
      return self.internal_data



