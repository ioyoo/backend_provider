#!/bin/bash

echo "Updating zip file with new dependencies..."
Compress-Archive -Path .\.env\Lib\site-packages\* -Update -DestinationPath .\deployment_package.zip

echo "Adding new lambda function to deployment_package..."
Compress-Archive -update .\lambda_function.py .\deployment_package.zip

echo "Publishing deployment_package to aws!"
aws lambda update-function-code --function-name backend_provider --zip-file fileb://deployment_package.zip

echo "Deployment Complete!!!"