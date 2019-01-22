# DepChecker

DepChecker is a web application for specific use in tracking remote
dependencies. We maintain a lot of software that has large dependency
trees and tracking upstream, much less updating the software, is a
serious chore.

The goal of this webapp is to take in a configuration file of known
releases and to systematically discover A) current in-use version as
well as B) current upstream latest version. Through periodic checking
of upstream versions, the webapp will then notify maintainers that a
new version is available, to which a maintainer can go out and do the
needful.

There's significant work still to be done in order to achieve it's
intended goal. Feel free to open issues with feature requests. Right
now, I'm focusing on the parsing of various upstream tracking methods.


## Configuration

Configuring DepChecker is (hopefully) straightforward, an example can
be found on [example_config.yaml](example_config.yaml), and a more
in-depth explanation can be found in [docs/CONFIG.md](docs/CONFIG.md).

## API

DepChecker has a simple API right now, and you can view documentation
about it in the [API.md](docs/API.md) doc.