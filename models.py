import urllib.request, json, os, sys, yaml

API_TOKEN = os.getenv('GITHUB_TOKEN', False)

if not API_TOKEN:
  print("Need GitHub API token as 'GITHUB_TOKEN' envvar.")
  sys.exit(-1)

def get_latest(git: str) -> str:
  api = urllib.request.Request("https://api.github.com/repos/" + git + "/releases")
  api.add_header('Authorization', 'token ' + API_TOKEN)
  with urllib.request.urlopen(api) as url:
    data = json.load(url)
    try:
      return data[0]['tag_name'][1:] if data[0]['tag_name'][0] == "v" else data[0]['tag_name']
    except IndexError:
      print("\"" + git + "\" doesn't use releases, falling back on latest tag.")
  
  api = urllib.request.Request("https://api.github.com/repos/" + git + "/tags")
  api.add_header('Authorization', 'token ' + API_TOKEN)
  with urllib.request.urlopen(api) as url:
    data = json.load(url)
    try:
      return data[0]['name'][1:] if data[0]['name'][0] == "v" else data[0]['name']
    except IndexError:
      print("\"" + git + "\" doesn't use releases or tags. I give up.")
      return "NULL"

def load_config(file: str) -> dict:
  with open(file) as config:
    dep_status = yaml.safe_load(config)
    for k_index, kit in enumerate(dep_status['kits']):
      for r_index, release in enumerate(kit['releases']):
        print("Checking release \"" + release['name'] + "\".")
        dep_status['kits'][k_index]['releases'][r_index]['latest_version'] = get_latest(release['git'])
  print("Loaded dependencies: " + str(dep_status))
  return dep_status