#!/bin/bash
set -e

# Run the bootstrap command to setup the persistence layer
/app/bin/polaris-service bootstrap polaris-server.yml

# Now run the main application
/app/bin/polaris-service server polaris-server.yml