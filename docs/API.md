# API

Default credentials are `bober:pleasechange`. Please do what the
password asks.


### `POST /update_versions` (auth required)

Payload body is expected to be `'Content-Type': 'application/json'`
with the following format:

{"kits": {"kit_name": {"releases": {"release_name": {"version":
"###"}}}}}

An example: 

`curl -d '{"kits": {"blacksmith": {"releases": {"blacksmith":
{"version": "555"}}}}}' -H "Content-Type: application/json" -u
USER:PASS -X POST http://localhost:8080/update_version`


### `GET /update_git` (auth required)

No payload body expected. Calling this endpoint will refresh the
latest upstream versions from GitHub.


### `POST /update_config` (auth required)

Payload body is a YAML file (binary).

An example:

`curl --data-binary @config.yml -u USER:PASS -X POST
http://localhost:8080/update_config`


### `GET /get_config`

Returns the configuration file in YAML text.