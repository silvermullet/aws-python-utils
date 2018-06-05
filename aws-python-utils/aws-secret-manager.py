# Use this code snippet in your app.
import boto3
import os
from botocore.exceptions import ClientError

class AwsSecretManager:
"""AWS Secret Manager class"""

    def get_secret():
        """AWS secret get_secret"""

        # todo, offer inputs for these and/or environment variables
        secret_name = os.environ.get('AWS_SECRET_MANAGER_SECRET')
        endpoint_url = "https://secretsmanager.us-west-2.amazonaws.com"
        region_name = "us-west-2"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name,
            endpoint_url=endpoint_url
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + secret_name + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
        else:
            # Decrypted secret using the associated KMS CMK
            # Depending on whether the secret was a string or binary,
            # one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                return secret
            else:
                binary_secret_data = get_secret_value_response['SecretBinary']
                return binary_secret_data
