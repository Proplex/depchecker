import json, os, sys, yaml, collections
from threading import Lock
from .fetcher import get_latest

class Data():

  def __init__(self):
    self.config_file = os.getenv('DEPCHECK_CONFIG', "example_config.yml")
    self.internal_data = {'releases': [], 'kits': []}
    
    # mutexes to atomize editing config file and datastore
    self.file_mutex = Lock()
    self.data_mutex = Lock()

  # load configuration from disk to memory
  def load_config(self):
    with self.file_mutex:
      with self.data_mutex:
        with open(self.config_file, 'r') as config:
          self.internal_data = yaml.safe_load(config)
          print("Successfully loaded configuration to memory.")

  def write_config(self):
    with self.file_mutex:
      # ensure datastore isn't updated while writing to disk
      with self.data_mutex:
        with open(self.config_file, 'w') as config:
          config.write(yaml.safe_dump(self.internal_data, default_flow_style=False))
          print("Successfully saved configuration to disk.")

  def write_config_raw(self, file_contents: str):
    with self.file_mutex:
      with open(self.config_file, 'wb') as config:
        config.write(file_contents)
        print("Successfully overwrote configuration.")
    self.load_config()
  
  def get_config_raw(self):
    with self.file_mutex:
        with open(self.config_file, 'r') as config:
          return config.read()

  def update_data(self, data: dict):
    with self.data_mutex:
      dict_merge(self.internal_data, data)
    self.write_config()

  def update_versions(self):
    seen_releases = {} # cache releases that are the same across kits
    with self.data_mutex:
      for kit, kit_info in self.internal_data['kits'].items():
        for release, release_info in kit_info['releases'].items():
          # check if we've seen this release before, if so,
          # then used cached version info (reduces GH API calls)
          if release_info['git'] in seen_releases:
            print("Using cached information for \"" + release + "\".")
            self.internal_data['kits'][kit]['releases'][release]['latest_version'] = seen_releases[release_info['git']]
          else:
            print("Checking release \"" + release + "\".")
            latest_release = get_latest(release_info['git'])
            seen_releases[release_info['git']] = latest_release
            self.internal_data['kits'][kit]['releases'][release]['latest_version'] = latest_release
      print("Loaded dependencies: " + str(self.internal_data))
  
  def get_data(self) -> dict:
    with self.data_mutex:
      return self.internal_data



def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]