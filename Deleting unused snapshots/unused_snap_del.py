# Installing dependencies: Install boto3 module in your local: pip install boto3; pip install botocore(optional).
# Configue the aws credentials and snapshot location in .aws folder before running script.

import boto3
import botocore
client = boto3.client('ec2')

"""
Mention the text file name, where the snapshotids are captured. The txt file should contain the snapshot IDs in the below format:
snapshot01
snapshot02
snapshot03

"""

my_file = open("myindprd_snapids.txt", "r")
data = my_file.read()
list_of_snapshots = data.split("\n")

my_file.close()
for i in list_of_snapshots:
	try:
		response = client.delete_snapshot(SnapshotId= i)
	except botocore.exceptions.ClientError as err:
		print('Snapshot ID: {} Error Message: {}'.format(i, err.response['Error']['Message']))
		if err.response['Error']['Code'] in ['Access Denied', 'BadRequest', 'InternalServerError', 'SnapshotNotFound']:
			continue