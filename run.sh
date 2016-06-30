#!/bin/sh --

# Debugging: -x to enable, +x to disable
set +x
# the files logging.yaml and config.yaml can be placed outside of the project as well.
# uncomment the first line after putting the correct path values to both the yaml files. A default value is provided to start the script running.

#LOG_CFG=/path/to/logging.yaml python groupsforsections.py /path/to/config.yaml
LOG_CFG=config/logging.yaml python groupsforsections.py config/config.yaml
