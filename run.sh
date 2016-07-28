#!/bin/sh --

# Debugging: -x to enable, +x to disable
set +x
# the files logging.yaml, config.yaml, security.yaml can be placed outside of the project as well.
# uncomment the first line after putting the correct path values to both the yaml files. A default value is provided to start the script running.

LOG_CFG=config/logging.yaml python groupsforsections.py
#LOG_CFG=/Users/pushyami/propertyFiles/logging.yaml python groupsforsections.py /Users/pushyami/propertyFiles/config.yaml /Users/pushyami/propertyFiles/security.yaml
