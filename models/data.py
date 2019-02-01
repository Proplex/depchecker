import json, os, sys, yaml, collections, time, boto3
from threading import Lock
from .fetcher import get_latest

class Data():

  def __init__(self):
    self.config_file = os.getenv('DEPCHECK_CONFIG', "example_config.yml")
    self.internal_data = {'releases': [], 'kits': [], 'last_updated': time.time()}
    
    # mutexes to atomize editing config file and datastore
    self.file_mutex = Lock()
    self.data_mutex = Lock()



  # load configuration for s3, and fetch data from s3
  def load_config(self):
    with self.file_mutex:
      with self.data_mutex:
        info = ""
        with open(self.config_file, 'r') as config:
          info = yaml.safe_load(config)
      sesh = boto3.Session(
        aws_access_key_id=info['s3']['aws_access_key_id'],
        aws_secret_access_key=info['s3']['aws_secret_access_key'],
        region_name=info['s3']['region'])
      s3 = sesh.resource('s3')
      content = s3.Object(
        bucket_name=info['s3']['bucket_name'],
        key='data.yml')
      remote_data = content.get()['Body'].read().decode('utf-8')
      self.internal_data = yaml.safe_load(remote_data)
      print("Successfully loaded data from S3 to memory.")

  def write_config(self):
    with self.file_mutex:
      with self.data_mutex:
        info = ""
        with open(self.config_file, 'r') as config:
          info = yaml.safe_load(config)
      sesh = boto3.Session(
        aws_access_key_id=info['s3']['aws_access_key_id'],
        aws_secret_access_key=info['s3']['aws_secret_access_key'],
        region_name=info['s3']['region'])
      s3 = sesh.resource('s3')
      content = s3.Object(
        bucket_name=info['s3']['bucket_name'],
        key='data.yml')
      s3.Object(
        bucket_name=info['s3']['bucket_name'],
        key='data.yml').put(
          Body=yaml.safe_dump(self.internal_data, default_flow_style=False))
      print("Successfully uploaded data from memory to S3.")

  def write_config_raw(self, file_contents: str):
    with self.file_mutex:
      sesh = boto3.Session(
        aws_access_key_id=info['s3']['aws_access_key_id'],
        aws_secret_access_key=info['s3']['aws_secret_access_key'],
        region_name=info['s3']['region'])
      s3 = sesh.resource('s3')
      content = s3.Object(
        bucket_name=info['s3']['bucket_name'],
        key='data.yml')
      s3.Object(
        bucket_name=info['s3']['bucket_name'],
        key='data.yml').put(
          Body=file_contents)
    print("Successfully uploaded data to S3.")
    self.load_config()


  def update_data(self, data: dict):
    with self.data_mutex:
      dict_merge(self.internal_data, data)
    self.internal_data['last_updated'] = int(time.time())
    print("Successfully updated data in memory.")
    self.write_config()

  def update_versions(self):
    seen_releases = {} # cache releases that are the same across kits
    with self.data_mutex:
      for kit, kit_info in self.internal_data['kits'].items():
        for release, release_info in kit_info['releases'].items():
          self.internal_data['kits'][kit]['releases'][release]['latest_version'] = get_latest(release_info)
          # TODO: reimplement caching layer
          # # check if we've seen this release before, if so,
          # # then used cached version info (reduces GH API calls)
          # if release_info['git'] in seen_releases:
          #   print("Using cached information for \"" + release + "\".")
          #    = seen_releases[release_info['git']]
          # else:
          #   print("Checking release \"" + release + "\".")
          #   latest_release = get_latest(release_info['git'])
          #   seen_releases[release_info['git']] = latest_release
          #   self.internal_data['kits'][kit]['releases'][release]['latest_version'] = latest_release
      print("Loaded " + str(len(self.internal_data['kits'].keys())) + " kits.")
    self.write_config()
  
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