# backend_provider
Backend to obtain info about data gatherer in local storage

# Prerequisites:
Install aws cli : https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

# configure aws cli with credentials; run following on cwd
aws configure 

# Start
have .env in the backend_provider directory
# generate zip
From backend_provider directory
cd .env/lib/python3.8/site-packages
zip -r ../../../../deployment_package.zip . 

# update zip
cd ../../../../
zip -r deployment_package.zip data
zip -r deployment_package.zip private
zip -g my-deployment-package.zip lambda_function.py

# upload example
aws lambda update-function-code --function-name backend_provider --zip-file fileb://deployment_package.zip

# link to more info
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

# or simply run upload.sh