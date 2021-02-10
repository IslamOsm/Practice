import sys
import os
import configparser

"""
Get config variables for using in Robot Framework tests
"""
try:

    config_file = "mqtt_config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    datamqtt = config['MQTT']

except (configparser.Error, configparser.NoSectionError,
        configparser.NoOptionError) as e:
    sys.stderr.write("Error: {0}.\n".format(e))
    sys.exit()
