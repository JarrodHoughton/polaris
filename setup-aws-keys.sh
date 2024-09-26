#!/bin/bash

# Define the location of the AWS credentials file
AWS_CREDENTIALS_FILE=~/.aws/credentials

# Parse the AWS credentials for the default profile
AWS_ACCESS_KEY_ID=$(grep -A 2 '\[default\]' $AWS_CREDENTIALS_FILE | grep 'aws_access_key_id' | awk '{print $3}')
AWS_SECRET_ACCESS_KEY=$(grep -A 2 '\[default\]' $AWS_CREDENTIALS_FILE | grep 'aws_secret_access_key' | awk '{print $3}')

# Check if the values were found
if [[ -z "$AWS_ACCESS_KEY_ID" || -z "$AWS_SECRET_ACCESS_KEY" ]]; then
  echo "Error: AWS credentials not found in $AWS_CREDENTIALS_FILE"
  exit 1
fi

# Export the AWS credentials as environment variables
export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export AWS_REGION=eu-west-1

export JUPYTER_WORKSPACE_LOCATION=./notebooks
export PROFILE_NAME=default

# Confirm that the variables are set
echo "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY have been set."