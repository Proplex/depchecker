import urllib.request, json, os, sys, regex
from operator import attrgetter
from .utils import htmllistparse

API_TOKEN = os.getenv('GITHUB_TOKEN', False)
if not API_TOKEN:
  print("Need GitHub API token as 'GITHUB_TOKEN' envvar.")
  sys.exit(-1)

HEADERS = {'Authorization': 'token ' + API_TOKEN,
           'User-Agent': 'DepChecker (issues: proplex/depchecker)' # be a good web-citizen
        }

# detect what tracking method is used and use appropriate function
def get_latest(release: dict) -> str:
  if 'git' in release:
    return get_latest_git(release['git'])
  if 'csv' in release:
    return get_latest_csv(release['git'])
  if 'http_index' in release:
    # grab latest release from a apache/nginx index and regex version
    latest_release = get_latest_http_index(release['http_index'])
    return extract_version(latest_release, release['regex'])


# get latest release/tag based on availability
# TODO: implement some tag/release merging for repos
# that use a combo of releases and tags.
def get_latest_git(git: str) -> str:
  print("[FETCHER:GIT] Grabbing release info for " + git)
  api = urllib.request.Request("https://api.github.com/repos/" + git + "/releases", headers=HEADERS)
  try:
    with urllib.request.urlopen(api) as url:
      data = json.load(url)
      try:
        return data[0]['tag_name'][1:] if data[0]['tag_name'][0] == "v" else data[0]['tag_name']
      except IndexError:
        print("--> \"" + git + "\" doesn't use releases, falling back on latest tag.")
  except Exception as err:
    print("--> \"" + git + "\" threw an error: " + str(err) + ", skipping.")
    return "NULL"
  api = urllib.request.Request("https://api.github.com/repos/" + git + "/tags", headers=HEADERS)
  try:
    with urllib.request.urlopen(api) as url:
      data = json.load(url)
      try:
        return data[0]['name'][1:] if data[0]['name'][0] == "v" else data[0]['name']
      except IndexError:
        print("\"" + git + "\" doesn't use releases or tags. I give up.")
        return "NULL"
      except Exception as err:
        print("--> \"" + git + "\" threw an error: " + str(err) + ", skipping.")
        return "NULL"
  except Exception as err:
    print("--> \"" + git + "\" threw an error: " + str(err) + ", skipping.")
    return "NULL"


def get_latest_http_index(url: str) -> str:
  print("[FETCHER:HTTP_INDEX] Grabbing release info from " + url)
  cwd, listing = htmllistparse.fetch_listing(url, timeout=30)
  recents = sorted(listing, key=attrgetter('modified'), reverse=True)
  if "latest" in recents[0].name:
    return recents[1].name
  return recents[0].name


def extract_version(name: str, reg: str) -> str:
  # run provided regex on filename, used 
  version = regex.search(reg, name)
  try:
    print("--> Extracted: " + version[0])
  except IndexError:
    print("--> Regex failed to apply; regex used was " + reg)
    return "Invalid Regex!"
  return version[0]
    
  