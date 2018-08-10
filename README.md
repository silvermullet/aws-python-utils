# aws-python-utils

Simplify use of AWS resources in your code with aws-python-utils

### Install

```
pip install aws-python-util
```

### SecretManager Util
* Easy secret retrieval

##### get_secret()

Use ENVIRONMENT variable "AWS_SECRET_MANAGER_SECRET" or pass in secret_key name.

###### Example Usage

Via ENVIRONMENT variable
```python
from aws_python_utils import secretmanager
import os

os.environ["AWS_SECRET_MANAGER_SECRET"] = "mysecret"
secretmanager = secretmanager.AwsSecretManager()
mysecret = secretmanager.get_secret()
```

Or pass in secret_key name ..
```python
from aws_python_utils import secretmanager
import os

secretmanager = secretmanager.AwsSecretManager()
mysecret = secretmanager.get_secret(secret_key="mysecret")
```

### S3 Util
* Streams an s3 object directly into a pandas DataFrame to avoid writing to disk and then loading from disk
* Uploads a DataFrame directly to s3

###### Example Usage
```python
from aws_python_utils import s3
from io import BytesIO
import pandas as pd
import numpy as np

bucket,key = s3.AwsS3.get_bucket_and_key_from_s3_path("s3://my-bucket/mypath/to/object")

print("bucket = " + bucket)  # my-bucket
print("key = " + key)        # mypath/to/object

# download a tab separated file schema: id    val1  val2
df = s3.AwsS3.download_s3_file(s3_path, header=0, sep='\t', index='id')

df2 = pd.DataFrame(np.random.randint(low=0, high=10, size=(5, 5)), columns=['a', 'b', 'c', 'd', 'e'])
io_buffer = BytesIO()
df2.to_csv(io_buffer, columns=['a', 'c', 'e'], sep='\t', index=False)

s3.AwsS3.upload_to_s3("s3://your-bucket/path/to/object.tsv", io_buffer)
```
