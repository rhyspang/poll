#!/bin/bash

echo $PYTHONPATH

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P  )"

echo append $SCRIPTPATH to PYTHONPATH 

export PYTHONPATH="$SCRIPTPATH:$PYTHONPATH"
export FLASK_APP=${SCRIPTPATH}/annotator/run.py
echo install success~
