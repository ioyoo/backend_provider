# backend_provider
Backend to obtain info about data gatherer in local storage

# Prerequisites:
Install aws cli : https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

# configure aws cli with credentials; run following on cwd
aws configure 

# Start
have .env in the backend_provider dirrectory
# generate zip
From backend_provider directory
Compress-Archive -Path .\.env\Lib\site-packages\* -DestinationPath .\backend_provider\deployment_package.zip  

# update zip
From ioyoo directory
Compress-Archive -Path .\.env\Lib\site-packages\* -Update -DestinationPath .\backend_provider\deployment_package.zip 

# function code files to root 
Compress-Archive -update .\lambda_function.py .\deployment_package.zip

# upload example
aws lambda update-function-code --function-name backend_provider --zip-file fileb://deployment_package.zip

# link to more info
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

# or simply run upload.sh