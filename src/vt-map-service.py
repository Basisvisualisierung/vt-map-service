# -------------------------------------------------------------------------------
# VT Map Service
# Version 0.5.0
# 
# Copyright 2020 Landesamt für Geoinformation und Landesvermessung Niedersachsen
# Licensed under the European Union Public License (EUPL)
# -------------------------------------------------------------------------------

from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import uuid
import sqlite3
import json
import yaml

import create_db

create_db.init_db()

service = Flask(__name__)

# Read configuration file
with open('vt-map-service.yaml', 'r') as yaml_file:
    config = yaml.load(yaml_file)

@service.route(config['services']['root_path']  + "/map", methods=['POST'])
@cross_origin(origins='http://localhost:4200', methods='POST')
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
        response_data = {'id': mapId,
                         'style_url': config['services']['root_url'] + config['services']['root_path']  +  '/style/' + mapId, 
                         'application_url': config['services']['map_view_url'] + '/' + mapId}

    return jsonify(response_data)

@service.route(config['services']['root_path'] + "/config/<string:id>", methods=['GET'])
@cross_origin(methods='GET')
def get_map_config(id):
    """Get map configuration from database."""
    mapConfig = None

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

@service.route(config['services']['root_path'] + "/style/<string:id>", methods=['GET'])
@cross_origin(methods='GET')
def get_map_style(id):
    """Get map style from database."""
    data = None
    conn = None
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