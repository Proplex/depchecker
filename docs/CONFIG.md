# Config

The configuration file is a key-value based YAML file split into two
separate fields; `kits` and `releases`. Kits are used to track all the
dependencies in a single Genesis Kit, while `releases` are used to
track one-off releases that don't fit anywhere.

An in-use, valid example can be found in the
[example_config.yml](example_config.yml) file of this repo.


## Releases

Both one-off releases and releases found within kits are configured
the same way.

### Tracking a GitHub-based Release
The `git:` field indicates this is a GitHub-based release and should
be tracked accordingly. The `git:` value is the location of the repo
in `org/repo` format.

The `version:` field is the current in-use version of the release.

```
name-of-release:
  git: organization/repository
  version: version number
```

### Tracking an HTTP Index Release
The `http_index:` field indicates this is an HTTP index directory
(such as those found on Apache and Nginx servers). The `http_index:`
value is the URL of the index listing. *NOTE: this currently only
works with Apache and Nginx using standard directory listings*

The `regex:` field is a required field that specifies how to extract
the version number from a file name in the index directory. The
fetcher expects the first result the regex finds to be the version.

The `version:` field is the current in-use version of the release.


```
name-of-release:
  http_index: https://ftp.gnu.org/gnu/wget/
  regex: \d+(\.\d+)+
  version: version number
```

## Kits

Kits are a group of releases with a name to tie everything together.
The releases field is configured as stated above.


```
kits:
  name-of-kit
    display: Display Name For Kit
    releases:
      [releases here]
  cf:
    display: Cloud Foundry
    releases:
      [releases here]
```