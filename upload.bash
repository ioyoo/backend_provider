#!/bin/bash

export LAMBDA=$1
RED='\033[0;31m'
GREEN='\033[0;32m'

if [ -z "$LAMBDA" ]; then
    echo -e "${RED} Error: No lambda given to upload, add it as first argument in upload call!"
    exit 1
fi

deactivate

echo "Updating zip file with new dependencies..."
cd .env/lib/python3.8/site-packages
zip -r ../../../../deployment_package.zip .

echo "Adding new lambda function and local dependencies to deployment_package..."
cd ../../../../
zip -r deployment_package.zip data
zip -r deployment_package.zip private
zip -g -j deployment_package.zip ./lambdas/$LAMBDA/lambda_function.py
mv deployment_package.zip lambdas/$LAMBDA 

echo "Publishing deployment_package to aws!"
aws lambda update-function-code --function-name $LAMBDA --zip-file fileb://lambdas/$LAMBDA/deployment_package.zip

retval=$?
if [ $retval -ne 0 ]; then
    echo -e "${RED} Error: could not complete upload..."
    exit 1
fi
echo -e "${GREEN} Deployment Complete!!!"

source .env/bin/activate