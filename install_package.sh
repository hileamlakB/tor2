#!/bin/sh

pip install "$@"
pipreqs . --force
