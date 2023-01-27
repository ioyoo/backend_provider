#!/bin/bash

export LAMBDA=$1

deactivate

echo "Updating zip file with new dependencies..."
cd .env/lib/python3.8/site-packages
zip -r ../../../../deployment_package.zip .

echo "Adding new lambda function and local dependencies to deployment_package..."
cd ../../../../
zip -r deployment_package.zip data
zip -r deployment_package.zip private
zip -g deployment_package.zip lambdas/$LAMBDA/lambda_function.py
mv deployment_package.zip lambdas/$LAMBDA 

echo "Publishing deployment_package to aws!"
aws lambda update-function-code --function-name $LAMBDA --zip-file fileb://lambdas/$LAMBDA/deployment_package.zip

echo "Deployment Complete!!!"

source .env/bin/activate