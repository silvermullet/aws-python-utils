# aws-python-utils

Simplify use of AWS resources in your code with aws-python-utils

### AwsSecretManager

##### get_secret()

Use ENVIRONMENT variable "AWS_SECRET_MANAGER_SECRET" or pass in secret_key name.

###### Example Usage

Via ENVIRONMENT variable
```
In [1]: import os
In [2]: import secretmanager
In [3]: os.environ["AWS_SECRET_MANAGER_SECRET"] = "mysecret"
In [4]: secretmanager = secretmanager.AwsSecretManager()
In [5]: secretmanager.get_secret()
Out[5]: 'supersecretpass'
```

Or pass in secret_key name ..
```
In [1]: import os
In [2]: import secretmanager
In [3]: secretmanager = secretmanager.AwsSecretManager()
In [4]: secretmanager.get_secret(secret_key="mysecret")
Out[4]: 'supersecretpass'
```
