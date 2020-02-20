# VT Map Service

Back end python service for VT Map Editor.

## Getting started

You can follow these instructions to run VT Map Service on your local machine. Alternatively you can create a Docker image as described below.

### Prerequisites

First you need to install a current version of Python 3 and the pip.

### Installation

For configuration options see [configuration file documentation](docs/configuration.adoc).

Install python packages.

```
pip install Flask
pip install flask-cors
pip install gunicorn
pip install pyyaml
```

For development purposes you can run the service by a simple built-in server with debug mode. You should not use this in a production environment.

```
export FLASK_APP=vt-map-service.py
export FLASK_ENV=development
export FLASK_DEBUG=1
python -m flask run
```

For a production environment you should deploy the service by a WSGI server like _gunicorn_.

```
gunicorn -b :5000 vt-map-service:service
``` 

## Docker

First customize the [configuration file](docs/configuration.adoc).

Open a command prompt, navigate to the project folder and build a Docker image:

```
docker build -t vt-map-service .
```

Start a container:

```
docker run --rm -v ${PWD}/data:/service/data -p 5000:5000 vt-map-service:latest
```

## License
Licensed under the European Union Public License (EUPL). For more information see [LICENSE.txt](LICENSE.txt).

Copyright 2020 Landesamt für Geoinformation und Landesvermessung Niedersachsen