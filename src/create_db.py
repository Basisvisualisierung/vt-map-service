import os
import sqlite3
import yaml

# Read configuration file
with open('vt-map-service.yaml', 'r') as yaml_file:
    config = yaml.full_load(yaml_file)

def init_db():
    """Create Database"""

    # Create non-existing folders
    if ('/') in config['storage']['database']:
        path = config['storage']['database']
        path = path[0:path.rfind('/')]

        if not os.path.exists(path):
            os.makedirs(path)

    # Create database and table
    conn = sqlite3.connect(config['storage']['database'])
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maps (
            id TEXT PRIMARY KEY,
            style TEXT,
            configuration TEXT,
            creation_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
