#!/usr/local/bin/python3
import sys, json, base64, os, ssl
from urllib import request, parse

if os.getenv("DEPCHECKER_USER") is None or os.getenv("DEPCHECKER_PASS") is None:
  print("You need to set DEPCHECKER_USER and DEPCHECKER_PASS")
  sys.exit(1)

ssl._create_default_https_context = ssl._create_unverified_context
if __name__ == '__main__':
  auth = base64.b64encode((os.getenv("DEPCHECKER_USER") + ':' + os.getenv("DEPCHECKER_PASS")).encode("utf-8"))

  # sys.argv[1]: name of kit
  # sys.argv[2]: name of release
  # sys.argv[3]: new version
  version = json.dumps({ 'kits': { str(sys.argv[1]): { "releases": { str(sys.argv[2]): { "version": str(sys.argv[3]) } } } } }).encode('utf8')

  post_info = {'Content-Type': 'application/json', 'Content-Length': len(version), 'Authorization': "Basic " + auth.decode('utf8')}

  req = request.Request('https://depchecker.run.cf.lab.starkandwayne.com/update_version', data=version, headers=post_info)

  request.urlopen(req)