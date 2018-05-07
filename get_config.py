import yaml
import os

workingDir = os.path.os.path.dirname( __file__ )

with open(workingDir + "/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
