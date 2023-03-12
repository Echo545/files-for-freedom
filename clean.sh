#!/bin/bash

# Read FILENAME from .readerName
FILENAME=$(cat .readerName)

# Delete public/FILENAME
rm -f public/"$FILENAME.html"

# Delete .readerName
rm -f .readerName