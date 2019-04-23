This library currently supports storage operations in local machine and aws s3 cloud storage service.

#Steps to install library
    -https://github.com/prateekeshwar/storeData.git

    -import module where you want to use

    #install required packages
        -- pip install boto3

#functionality supported

    -rename file or folder in local machine
        --rename_doc('local', old_name, new_name)
    -rename file in aws s3
        --rename_doc('s3', old_name, new_name, bucket_name)
    -delete file or folder in local machine
        --delete('local', file or folder path)
    -delete file or folder in s3
        --delete('s3', file or folder path, bucket_name)
    -get attributes of file or folder in local machine
        --get_attributes('local', file or folder path)
    -get attributes of file  in s3
        --get_attributes('s3', file, bucket_name)
    -get data present inside file from local machine
        --get_doc_data('local', file path)
    -get data present inside file from s3
        --get_doc_data('local', file path, bucket_name)
    -create file with required data inside it and save it locally
        --create_and_store('local', file path with name that need to be created, data to be written inside file)
    -create file with required data inside it and save it to s3 bucket
        --create_and_store('s3', file path with name that need to be created, data to be written inside file, bucket_name, s3 file path where you want your file to get saved, bucket_region='ap-southeast-1')
    -create bucket in s3
        --create_s3_bucket(bucket_name)
    -upload file to s3
        --upload_file_to_s3(file_path, bucket_name, s3_file_path, bucket_region='ap-southeast-1')


#To run test cases
    #install required packages 
        -- pip install pytest
        -- pip install mock
    
    #run test case
        pytest -q test_file_data.py


