import boto3
from datetime import datetime, timedelta
from typing import List
from . import logger

class AwsEC2:
    def __init__(self, session=boto3.Session()):
        self.LOG = logger.getLogger("AwsEC2")
        self.session = session
        self.ec2 = self.session.client('ec2')


    def get_images(self, image_name_list: List[str]=['*'], sort_by_date=True):
        images = self.ec2.describe_images(
            Owners=[
                self.session.client('sts').get_caller_identity().get('Account')
            ],
            Filters=[
                {
                    'Name': 'name',
                    "Values": image_name_list
                }
            ]
        )['Images']

        if sort_by_date:
            images.sort(key=lambda i: i['CreationDate'], reverse=True)

        return images


    def clean_images(self, image_name_pattern: str, num_to_keep: int, cutoff_date: datetime=None, images_to_keep=[]):
        images = self.get_images(image_name_list=[image_name_pattern], sort_by_date=True)
        deletion_candidates = images[num_to_keep:]
        for image in reversed(deletion_candidates):
            # use cutoff date if present else use num to keep and keeper list
            if cutoff_date is not None:
                created_at = datetime.strptime(image['CreationDate'], '%Y-%m-%dT%H:%M:%S.000Z')
                time_delta = (cutoff_date - created_at)
                if time_delta.total_seconds() > 0 and image['ImageId'] not in images_to_keep:
                    self.deregister_image(image)
            else:
                if image['ImageId'] not in images_to_keep:
                    self.deregister_image(image)



    def deregister_image(self, image: boto3.resource('ec2').Image):
        self.LOG.info("deleting image:  name=%s  id=%s  created at %s\n" % (image['Name'], image['ImageId'], image['CreationDate']))
        self.ec2.deregister_image(ImageId=image['ImageId'])
