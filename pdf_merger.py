import os
import boto3
from packages.PyPDF2 import PdfFileMerger, PdfFileReader
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_dir(prefix, local, bucket):
    client = boto3.client("s3")
    keys = []
    dirs = []
    next_token = ""
    base_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != "":
            kwargs.update({"ContinuationToken": next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get("Contents")
        for i in contents:
            k = i.get("Key")
            if k[-1] != "/":
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get("NextContinuationToken")
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        client.download_file(bucket, k, dest_pathname)


def copy_files_from_s3(bucket_name, prefix):
    s3_client = boto3.client("s3")

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    objects = sorted(response["Contents"], key=lambda obj: obj["LastModified"])
    print(objects)
    pass


def copy_files_to_s3(bucket_name, prefix):
    pass


def merge_pdfs(file_path_str):
    """
    the file_path_str is either absolute or relative file path as a string to the file where
    all your pdfs are saved (and where we'll export the merged file to. examples:
    './file_folder_relative_to_where_I_am/'
    or
    '/Users/joesmith/Desktop/pdf_reports/'
    """
    # gather list of all the pds in the folder:
    pdf_list = os.listdir(file_path_str)
    # make sure you don't pick up any system files or other non-pdfs:
    pdf_list = [pdf for pdf in pdf_list if ".pdf" in pdf]

    # sort the pdfs by file name:
    pdf_list.sort()

    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()

    # Loop through all of the single pdfs and append them into one document
    for file in pdf_list:
        fullpath = os.path.join(file_path_str, file)
        mergedObject.append(PdfFileReader(fullpath, "rb"))

    # Write all the files into a file which is named as shown below
    output = os.path.join(file_path_str, "merged_pdfs.pdf")
    mergedObject.write(output)


def lambda_handler(event, context):
    ## Copy all files from S3 - prefix to /tmp
    download_dir("pdf/", "/tmp", "myrhapdf")
    ## stich all files
    print(os.listdir("/tmp"))
    merge_pdfs("/tmp/pdf")
    print(os.listdir("/tmp/pdf"))
    ## upload file to s3
    os.chdir("/tmp/pdf")
    upload_file("merged_pdfs.pdf", "myrhapdf", "tmp/output/file.pdf")


# def main():
#     print("Hello World!")
#     merge_pdfs('/mnt/chromeos/MyFiles/Downloads/pdf')

# if __name__ == "__main__":
#    main()
