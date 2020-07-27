# -------------------------------------------------------------------------------
# VT Map Service
# Version 1.1.0
# 
# Copyright 2020 Landesamt für Geoinformation und Landesvermessung Niedersachsen
# Licensed under the European Union Public License (EUPL)
# -------------------------------------------------------------------------------

import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import uuid
import sqlite3
import json
import yaml
import requests

import create_db

create_db.init_db()

service = Flask(__name__)

# Read configuration file
with open('vt-map-service.yaml', 'r') as yaml_file:
    config = yaml.full_load(yaml_file)

@service.route("/map", methods=['POST'])
def save_map():
    """Save map style and configuration to database."""
    if not request.json:
        abort(400)
    
    conn = None
    mapId = str(uuid.uuid4())
    response_data = {'error': True}

    try:
        conn = sqlite3.connect(config['storage']['database'])
        cur = conn.cursor()
        cur.execute('''INSERT INTO maps (id,style,configuration) VALUES (?,?,?)''',(mapId, json.dumps(request.json["style"]), json.dumps(request.json["configuration"])))
        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
        mapId = None
    finally:
        if conn is not None:
            conn.close()

    if mapId is not None:
        response_data = {'id': mapId}

    return jsonify(response_data)

@service.route("/config/<string:id>", methods=['GET'])
@cross_origin(methods='GET')
def get_map_config(id):
    """Get map configuration from database."""
    mapConfig = None

    if (is_valid_uuid(id)):
        try:
            conn = sqlite3.connect(config['storage']['database'])
            cur = conn.cursor()
            cur.execute('''SELECT configuration FROM maps WHERE id=?''',(id,))
            data = cur.fetchone()
            mapConfig = json.loads(data[0])
            cur.close()
        except Exception as e:
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
        
        if mapConfig is None or id is None:
            abort(404)
    
    return jsonify(mapConfig)

@service.route("/style/<string:id>", methods=['GET'])
@cross_origin(methods='GET')
def get_map_style(id):
    """Get map style from database."""
    data = None
    conn = None

    if (is_valid_uuid(id)):
        try:
            conn = sqlite3.connect(config['storage']['database'])
            cur = conn.cursor()
            cur.execute('''SELECT style FROM maps WHERE id=?''',(id,))
            data = cur.fetchone()[0]
            cur.close()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
    
    return jsonify(json.loads(data))

@service.route("/suggest", methods=['GET'])
def geocoder_suggest():
    """Get address suggestions"""
    api = getGeocoderApi()
    api_key = getGeocoderApiKey()
    if api != '' or api != '':
        params = config['geocoder']['suggest_params'] if config['geocoder']['suggest_params'] != None else {}
        
        # Define request url and parameters for geocoder service
        geocoder_url = ''
        if api == 'bkg':
            geocoder_url = 'https://sg.geodatenzentrum.de/gdz_geokodierung__' + api_key + '/suggest'
            params['query'] = request.args.get('term', type = str)
            params['outputformat'] = 'json'
        elif api == 'ors':
            geocoder_url = 'https://api.openrouteservice.org/geocode/search'
            params['api_key'] = api_key
            params['text'] = request.args.get('term', type = str)
        
        # Request geocoder
        response = requests.get(geocoder_url, params=params)
        
        # Unify results from different services
        suggestions = []
        if api == 'bkg':
            for item in response.json():
                suggestions.append({'suggestion': item['suggestion']})
        elif api == 'ors':
            for item in json.loads(response.text)['features']:
                suggestions.append({'suggestion': item['properties']['label']})

        return jsonify({'suggestions': suggestions})
    else:
        return jsonify({'error': 'Missing geocoder configuration'}), 500

@service.route("/search", methods=['GET'])
def geocoder_search():
    """Search address"""
    api = getGeocoderApi()
    api_key = getGeocoderApiKey()

    if api != '' or api != '':
        params = config['geocoder']['search_params'] if config['geocoder']['search_params'] != None else {}
        
        # Define request url and parameters for geocoder service
        geocoder_url = ''
        if api == 'bkg':
            geocoder_url = 'https://sg.geodatenzentrum.de/gdz_geokodierung__' + api_key + '/geosearch'
            params['query'] = request.args.get('term', type = str)
            params['outputformat'] = 'json'
        elif api == 'ors':
            geocoder_url = 'https://api.openrouteservice.org/geocode/search'
            params['api_key'] = api_key
            params['text'] = request.args.get('term', type = str)

        # Request geocoder
        response = requests.get(geocoder_url, params=params)

        result = None
        if api == 'bkg':
            result = jsonify(response.json())
        elif api == 'ors':
            result = jsonify(json.loads(response.text))

        return result
    else:
        return jsonify({'error': 'Missing geocoder configuration'}), 500

def is_valid_uuid(mapId):
    """Validate UUID"""
    try:
        uuid.UUID(mapId)
        return True
    except ValueError:
        return False

def is_valid_config(mapConfig):
    """Validate map configuration"""
    mapFunctions = ('navigation', 'info', 'search', 'routing')
    # Check if configuration contains functions
    for func in mapFunctions:
        if mapConfig.get(func) is None or mapConfig.get(func).get('enabled') is None:
            return False 
    if mapConfig.get('routing').get('enabled') == True and mapConfig.get('routing').get('configuration') is None:
        return False
    return True

def getGeocoderApi():
    """Get name of geocoder API from environment variable or configuration file"""
    api = ''
    if os.environ.get('VTMS_SEARCH_API') != None:
        api = os.environ.get('VTMS_SEARCH_API')
    elif config['geocoder']['api'] != None:
        api = config['geocoder']['api']
    return api

def getGeocoderApiKey():
    """Get key for geocoder API from environment variable or configuration file"""
    api_key = ''
    if os.environ.get('VTMS_SEARCH_API_KEY') != None:
        api_key = os.environ.get('VTMS_SEARCH_API_KEY')
    elif config['geocoder']['api_key'] != None:
        api_key = config['geocoder']['api_key']
    return api_key