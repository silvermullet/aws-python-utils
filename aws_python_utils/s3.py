import boto3, re
import pandas as pd
from . import logger
from io import BytesIO, StringIO


class AwsS3():
    """AWS Secret Manager class"""

    s3_client = boto3.client("s3")
    LOG = logger.getLogger("S3Util")

    def get_bucket_and_key_from_s3_path(s3_path):
        """returns tuple representing (bucket,key)"""
        res = re.search("s3://(.*?)/(.*)", s3_path)
        if not res:
            # try without s3 protocol
            res = re.search("(.*?)/(.*)", s3_path)
            if not res:
                raise ValueError("could not extract bucket and key from s3_path=%s", s3_path)

        return res.group(1),res.group(2)

    def download_s3_file(s3_path, header=None, sep=',', dtype=None, index=None):
        """returns a panda DataFrame"""
        LOG.info("downloading %s" % s3_path)
        bucket,key = get_bucket_and_key_from_s3_path(s3_path)
        obj = s3_client.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(BytesIO(obj['Body'].read()), dtype=dtype, header=header, sep=sep)
        if index is not None:
            df.set_index(index, inplace=True)

        return df

    def upload_to_s3(s3_out_path, io_buffer):
        """uploads contents in io_buffer.  should be instance of StringIO()"""
        LOG.info("uploading to %s" % s3_out_path)
        bucket,key = get_bucket_and_key_from_s3_path(s3_out_path)
        s3_client.put_object(Bucket=bucket, Key=key, Body=io_buffer.getvalue())
