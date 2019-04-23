import os
import shutil
import json
import boto3


def rename_doc(location, src_path, dst_path, bucket_name=None):
    """
    This function renames files.Currently supports local machine and s3.

    location: str
           location where to store created file with input data
    src_path: str
           old name file path in local machine or in s3
    dst_path: str
           new name file path in local machine or in s3
    bucket_name: str
           Name of the bucket to which the file is to be uploaded
    """
    if location == 'local':
        if os.path.isfile(src_path):
            os.rename(src_path, dst_path)
            return "file successfully renamed"
    if location == 's3':
        if bucket_name == None:
            return "Pass bucket name in argument"
        s3 = boto3.resource('s3')
        s3.Object(bucket_name, dst_path).copy_from(CopySource=bucket_name + '/' + src_path)
        s3.Object(bucket_name, src_path).delete()
        return "file successfully renamed"


def delete(location, src_path, bucket_name=None):
    """
    This function deletes files or folder.Currently supports local machine and s3.

    location: str
           location where to store created file with input data
    src_path: str
           path of file in local machine or in s3
    bucket_name: str
           Name of the bucket to which the file is to be uploaded
    """
    if location == 'local':
        if os.path.isfile(src_path):
            os.remove(src_path)
            return "file successfully deleted"
        else:
            shutil.rmtree(src_path)
            return "folder successfully deleted"
    if location == 's3':
        if bucket_name == None:
            return "Pass bucket name in argument"
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        bucket.objects.filter(Prefix=src_path).delete()


def get_attributes(location, src_path, bucket_name=None):
    """
    This function return a dictionary containing last modified and size of file.Currently
    it supports local machine file and files stored in s3.

    location: str
           location where to store created file with input data
    src_path: str
           path of file in local machine or in s3
    bucket_name: str
           Name of the bucket to which the file is to be uploaded
    """
    attr_dict = dict()
    if location == 'local':
        attr_dict['last_modified'] = os.path.getmtime(src_path)
        if os.path.isfile(src_path):
            attr_dict['size'] = os.path.getsize(src_path)
        else:
            attr_dict['size'] = getFolderSize(src_path)
        return attr_dict
    if location == 's3':
        if bucket_name == None:
            return "Pass bucket name in argument"
        s3_response_object = get_s3_file_content(src_path, bucket_name)
        attr_dict['last_modified'] = s3_response_object['LastModified']
        attr_dict['size'] = s3_response_object['ContentLength']
        return attr_dict



def getFolderSize(folder):
    """
    This function calculate the size of folder and returns it.

    ----------
    Parameters
    folder: str
            path of folder

    ----------
    Return
    total_size: int
            size of folder
    """
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size


def get_doc_data(location, src_path, bucket_name=None):
    """
    This read and return data inside the file.Currently it supports for local machine
    and for s3.

    location: str
           location where to store created file with input data
    src_path: str
           path of file in local machine or in s3
    bucket_name: str
           Name of the bucket to which the file is to be uploaded

    Return
    -----------
    data: file data
            return data inside file
    """
    if location == 'local':
        with open(src_path, 'r') as f:
            data = f.read()
            return data
    if location == 's3':
        if bucket_name == None:
            return "Pass bucket name in argument"
        s3_response_object = get_s3_file_content(src_path, bucket_name)
        data = s3_response_object['Body'].read()
        return data



def get_s3_file_content(src_path, bucket_name):
    """
    This function return the file data and content from s3

    Parameters
    -----------
    src_path: str
           file location in s3
    bucket_name: str
           s3 bucket name

    Return
    -----------
    s3_response_object: object
            s3 file object
    """
    s3_client = boto3.client('s3')
    s3_response_object = s3_client.get_object(Bucket=bucket_name, Key=src_path)
    return s3_response_object



def create_and_store(location, src_path, data, bucket_name=None, s3_file_path='', bucket_region='ap-southeast-1'):
    """
    This function creates and save file with incoming file data to desired location depending on input

    Note - right now support create and save file for local machine and s3 bucket. 
    Parameters
    -----------
    location: str
           location where to store created file with input data
    src_path: str
           path of file in local machine
    data: str
        data to be be written in newly created file
    bucket_name: str
           Name of the bucket to which the file is to be uploaded
    s3_file_path: str
           destination in s3.
    """
    dir_path = os.path.dirname(src_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(src_path, 'w') as fb:
        fb.write(data)
    if location == 's3':
        if bucket_name == None:
            return "Pass bucket name in argument"
        upload_file_to_s3(src_path, bucket_name, s3_file_path, bucket_region)
        shutil.rmtree(dir_path)


def create_s3_bucket(bucket_name):
    """
    This function creates a new bucket with name 'bucket_name' is
    already not exists.
    Parameters
    -----------
    bucket_name: str
           Name of bucket to be created
    """
    res = boto3.resource("s3")
    my_session = boto3.session.Session()
    my_region = my_session.region_name
    if not my_region:
        my_region = os.getenv('AWS_REGION')
    if res.Bucket(bucket_name) not in res.buckets.all():
        s3_client = boto3.client("s3", region_name=my_region)
        s3_client.create_bucket(Bucket=bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': my_region})


def upload_file_to_s3(file_path, bucket_name, s3_file_path='', bucket_region='ap-southeast-1'):
    """
    This function uploads a file to the bucket with name 'bucket_name'
    Parameters
    -----------
    file_path: str
           zip file to be uploaded to bucket
    bucket_name: str
           Name of the bucket to which the file is to be uploaded
    s3_file_path: str
           destination in s3.
    """
    if s3_file_path == '':
        s3_file_path = os.path.basename(file_path)
    s3_client = boto3.client('s3', region_name=bucket_region)
    s3_client.upload_file(file_path, bucket_name, s3_file_path)


