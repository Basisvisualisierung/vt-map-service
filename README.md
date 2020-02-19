# VT Map Service

Backend python service for VT Map Editor.

## Configuration

See [configuration documentation](docs/configuration.adoc) for configuration options.

## Installation

Install python packages.

`pip install Flask`\
`pip install flask-cors`\
`pip install gunicorn`\
`pip install pyyaml`

For development purposes you can run the service by a simple built-in server with debug mode. You should not use this in a production environment.

`export FLASK_APP=vt-map-service.py`\
`export FLASK_ENV=development`\
`export FLASK_DEBUG=1`\
`python -m flask run`

For a production environment you should deploy the service by a WSGI Server like _gunicorn_.

`gunicorn -b :5000 vt-map-service:service` 

## Docker

**Edit configuration file**:

`./src/vt-map-service.yaml`

**Build a Docker image:**

`docker build -t vt-map-service .`

**Start the container:**

`docker run --rm -v ${PWD}/data:/service/data -p 5000:5000 vt-map-:latest`

## License
Licensed under the European Union Public License (EUPL). For more information see [LICENSE.txt](LICENSE.txt).

Copyright 2020 Landesamt für Geoinformation und Landesvermessung Niedersachsen