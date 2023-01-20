#!/bin/bash

echo "Updating zip file with new dependencies..."
cd .env/lib/python3.8/site-packages
zip -r ../../../../deployment_package.zip . 

echo "Adding new lambda function and local dependencies to deployment_package..."
cd ../../../../
zip -r deployment_package.zip data
zip -r deployment_package.zip private
zip -g my-deployment-package.zip lambda_function.py

echo "Publishing deployment_package to aws!"
aws lambda update-function-code --function-name backend_provider --zip-file fileb://deployment_package.zip

echo "Deployment Complete!!!"