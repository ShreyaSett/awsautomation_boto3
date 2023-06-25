#This script can be used as Lambda Function to send out email notifications to existing IAM users whose access/secret keys are expiring as per AWS Security Standards. The script uses IAM user tags where the user email id needs to be mentioned. E.g.: IAM user Tag Key: Email, Value: xyz@dom1.com
#AWS Security Standard expects IAM user access/secret key rotation in every 90 days. Here, the users would be sent 2 different emails, one when the older key has not been rotated for the last 75 days and another if the age of the old key is between 85 and 90 days.
import boto3
import botocore
from datetime import datetime
from datetime import date
import json

iam_client = boto3.client('iam')
ses_client = boto3.client('ses')
response1 = iam_client.list_users()
def lambda_handler(event, context):
	for i in response1['Users']:
		response7 = iam_client.get_user(UserName = i['UserName'])
		response2 = iam_client.list_access_keys(UserName = i['UserName'])
		for j in response2['AccessKeyMetadata']:
			try:
				response3 = iam_client.get_access_key_last_used(AccessKeyId = j['AccessKeyId'])
				for k in response7['User']['Tags']:
					elapsed_days = (date.today() - j['CreateDate'].date()).days
					user_name = j['UserName']
					access_key_id = j['AccessKeyId']
					last_used = response3['AccessKeyLastUsed'].get('LastUsedDate')
					#The below conditional holds for users who have already used the old keys at least once at their respective endpoints.
					if 'LastUsedDate' in response3['AccessKeyLastUsed']:
						print(user_name, '\t', access_key_id, '\t', j['Status'], '\t', j['CreateDate'], '\t', elapsed_days, '\t', last_used, '\t', k['Key'], '\t', k['Value'])
						if elapsed_days == 75:
							if k['Key'] == 'Email':
								ses_client.send_email(
									Source = 'abcd@dom1.com', #Mention the email address of the user who is sending out the email. Make sure the domain and email adresses of the sender and receiver are already verified by SES.
    								Destination = {
        								'ToAddresses': [
        									k['Value']
        								],
   									},
    								Message={
        								'Subject': {
        									'Data': f'Security Alert!!! ***HIGH*** IAM USER [{user_name}] Access Key Nearing Age Threshold',
            								'Charset': 'UTF-8'
            								},
        								'Body': {
        									'Text': {
        										'Data': f"The Access key and Secret key associated with your IAM user has not been rotated in the last {elapsed_days} days.\n\nPlease update the new keys in the respective endpoints at the earliest.\n\nIAM Username: {user_name}\nAccess Key ID: {access_key_id}\nLast Accessed Date: {last_used}\n\nThank You!",
                								'Charset': 'UTF-8'
                							},
            							}
        							}
        						)
						elif elapsed_days>=85 or elapsed_days<=90:
							if k['Key'] == 'Email':
								ses_client.send_email(
									Source = 'abcd@dom1.com', #Mention the email address of the user who is sending out the email. Make sure the domain and email adresses of the sender and receiver are already verified by SES.
    								Destination = {
        								'ToAddresses': [
        									k['Value']
        								],
   									},
    								Message={
        								'Subject': {
        									'Data': f'Security Alert!!! ***URGENT*** IAM USER [{user_name}] Access Key Nearing Age Threshold',
            								'Charset': 'UTF-8'
            								},
        								'Body': {
        									'Text': {
        										'Data': f"The Access key and Secret key associated with your IAM user has not been rotated in the last {elapsed_days} days.\n\nPlease update the new keys in the respective endpoints at the earliest.\n\nIAM Username: {user_name}\nAccess Key ID: {access_key_id}\nLast Accessed Date: {last_used}\n\nThank You!",
                								'Charset': 'UTF-8'
                							},
            							}
        							}
        						)
					#The below conditional holds for users who have never ever used the old keys at their respective endpoints.
					else:
						print(j['UserName'], '\t', j['AccessKeyId'], '\t', j['Status'], '\t', j['CreateDate'], '\t', elapsed_days, '\t', 'Access Key never used', '\t', k['Key'], '\t', k['Value'])
						if elapsed_days == 75:
							if k['Key'] == 'Email':
								ses_client.send_email(
									Source = 'abcd@dom1.com', #Mention the email address of the user who is sending out the email. Make sure the domain and email adresses of the sender and receiver are already verified by SES.
    								Destination = {
        								'ToAddresses': [
        									k['Value']
        								],
   									},
    								Message={
        								'Subject': {
        									'Data': f'Security Alert!!! ***HIGH*** IAM USER [{user_name}] Access Key Nearing Age Threshold',
            								'Charset': 'UTF-8'
            								},
        								'Body': {
        									'Text': {
        										'Data': f"The Access key and Secret key have never been used since they were last generated and it has been {elapsed_days} days since.\n\nPlease update the new keys in the respective endpoint at the earliest.\n\nIAM Username: {user_name}\nAccess Key ID: {access_key_id}\nLast Accessed Date: Never\n\nThank You!",
                								'Charset': 'UTF-8'
                							},
            							}
        							}
        						)
						elif elapsed_days>=85 or elapsed_days<=90:
							if k['Key'] == 'Email':
								ses_client.send_email(
									Source = 'abcd@dom1.com', #Mention the email address of the user who is sending out the email. Make sure the domain and email adresses of the sender and receiver are already verified by SES.
    								Destination = {
        								'ToAddresses': [
        									k['Value']
        								],
   									},
    								Message={
        								'Subject': {
        									'Data': f"Security Alert!!! ***URGENT*** IAM USER [{user_name}] Access Key Nearing Age Threshold",
            								'Charset': 'UTF-8'
            								},
        								'Body': {
        									'Text': {
        										'Data': f"The Access key and Secret key have never been used since they were last generated and it has been {elapsed_days} days since.\n\nPlease update the new keys in the respective endpoint at the earliest.\n\nIAM Username: {user_name}\nAccess Key ID: {access_key_id}\nLast Accessed Date: Never\n\nThank You!",
                								'Charset': 'UTF-8'
                							},
            							}
        							}
        						)
			except botocore.exceptions.ClientError as err:
				print('Error message: {}'.format(err.response['Error']['Message']))
				if err.response['Error']['Code'] in ['Access Denied', 'NoSuchEntityException']:
					continue
				


