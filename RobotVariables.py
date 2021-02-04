import sys
import os
import configparser

"""
Get config variables for using in Robot Framework tests
"""
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(dir_path, 'mqtt_config.ini')

    config = configparser.ConfigParser()
    config.read(config_file)
    data = config['MQTT']

except (configparser.Error, configparser.NoSectionError,
        configparser.NoOptionError) as e:
    sys.stderr.write("Error: {0}.\n".format(e))
    sys.exit()
