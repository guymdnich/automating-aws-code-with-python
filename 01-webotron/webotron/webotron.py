#import boto3
#import sys

#session=boto3.Session(profile_name='pythonAutomation')
#s3=session.resource('s3')

#if __name__ == '__main__':
#    print(sys.argv)
#    for bucket in s3.buckets.all():
#        print(bucket)

import boto3
import click

from bucket import BucketManager


session=boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)

@click.group()
def cli():
    "Webotron deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "Lists all s3 buckets"
    for bucket in bucket_manager.all_buckets():
        print(bucket)
#        print(session.region_name)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    "Lists objects in an s3 bucket"
    for obj in bucket_manager.all_objects(bucket):
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket = None
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    "Sync contents of PATHNAME to BUCKET"
    bucket_manager.sync(pathname, bucket)

if __name__ == '__main__':
    cli()
#    list_buckets()
#    list_bucket_objects()
