import urllib.request, json, os, sys

API_TOKEN = os.getenv('GITHUB_TOKEN', False)
if not API_TOKEN:
  print("Need GitHub API token as 'GITHUB_TOKEN' envvar.")
  sys.exit(-1)

HEADERS = {'Authorization': 'token ' + API_TOKEN,
           'User-Agent': 'DepChecker (issues: proplex/depchecker)' # be a good web-citizen
        }

# get latest release/tag of a github
def get_latest(git: str) -> str:
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




