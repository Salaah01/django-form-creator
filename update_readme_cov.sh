#!/usr/bin/env bash

# Updates the README.md file with the coverage information adding a coverage
# shield.

set -e

# Get the coverage information.
make test-coverage
cov=$(coverage report | tail -n1 | awk '{print $4}')
percent=${cov%?}

# Set the colour
if [ $percent -lt 50 ]; then
  colour='red';
elif [ $percent -lt 90 ]; then  
  colour='yellow';
else
  colour='green';
fi

# Build the shield link
shield="![coverage: $cov](https://img.shields.io/badge/coverage-$percent%25-$colour.svg)"



# Update the README.md file.
sed -E "s@\!\[coverage.*?\)@${shield}@" -i README.md 