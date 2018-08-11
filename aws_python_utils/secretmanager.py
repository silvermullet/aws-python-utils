import boto3
import os
from . import logger
from botocore.exceptions import ClientError


class AwsSecretManager():
    """AWS Secret Manager class"""

    def __init__(self, profile_name=None,
                 endpoint_url="https://secretsmanager.us-west-2.amazonaws.com",
                 region_name="us-west-2"):
        self.session = boto3.Session(profile_name=profile_name)
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.secretmanager_client = self.session.client(
            service_name='secretsmanager',
            region_name=self.region_name,
            endpoint_url=self.endpoint_url
            )
        self.LOG = logger.getLogger("SecretManagerUtil")

    def get_secret(self, secret_key=None, endpoint_url, region_name):
        """AWS secret get_secret"""

        if secret_key == None:
            self.secret_key = os.environ.get("AWS_SECRET_MANAGER_SECRET", None)
        else:
            self.secret_key = secret_key
        self.secret_value = None
        self.binary_secret_data = None

        try:
            get_secret_value_response = self.secretmanager_client.get_secret_value(
                SecretId=self.secret_key
            )

        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.LOG.error(
                    f'The requested secret {self.secret_key} was not found')
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                self.LOG.error(f'The request was invalid due to: {e}')
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                self.LOG.error(f'The request had invalid params: {e}')
        else:
            # Decrypted secret using the associated KMS CMK
            # Depending on whether the secret was a string or binary,
            # one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                self.secret_value = get_secret_value_response['SecretString']
                return self.secret_value
            else:
                self.binary_secret_data = get_secret_value_response['SecretBinary']
                return self.binary_secret_data
