#This script helps generate a detailed report of the ELBs present in the associated AWS account and the instance associations for the ALBs if any.

import boto3
import pandas as pd

client1 = boto3.client('ec2')
client2 = boto3.client('elbv2')

response1 = client2.describe_load_balancers(PageSize = 400)

lb_name = []
lb_name1 = []
lb_arn = []
sg = []
vpc = []
subnetid1 = []
subnetid2 = []
lb_state = []
tg_state = []
lb_type = []
tg_name = []
tg_arn = []
tg_id = []
port = []
av_zone = []
hcp = []
state = []
reason = []
des = []
ins_name = []

dpe = []
als3e = []
als3b = []
als3p = []
h2 = []
it = []


my_dict1 = {}
my_dict2 = {}

def getinstancename(instanceid):
    instances = client1.describe_instances(Filters=[
        {
            'Name': 'instance-id',
            'Values': [
                instanceid
            ]
        },
    ],)
    for instance in instances["Reservations"]:
        for inst in instance["Instances"]:
            for tag in inst["Tags"]:
                if tag['Key'] == 'Name':
                    return (tag['Value'])
    return ('None')


for r1 in response1['LoadBalancers']:		
	response2 = client2.describe_target_groups(LoadBalancerArn = r1['LoadBalancerArn'])
	for r2 in response2['TargetGroups']:
		response3 = client2.describe_target_health(TargetGroupArn = r2['TargetGroupArn'])
		for r3 in response3['TargetHealthDescriptions']:
			for a in r3['TargetHealth']:
				lb_name.append(r1['LoadBalancerName'])
				lb_type.append(r1['Type'])
				vpc.append(r1['VpcId'])
				lb_state.append(r1['State']['Code'])
				subnetid1.append(r1['AvailabilityZones'][0]['SubnetId'])
				subnetid2.append(r1['AvailabilityZones'][1]['SubnetId'])
				if r1['Type'] == 'application':
					sg.append(r1['SecurityGroups'][0])
				else:
					sg.append('None')
				tg_name.append(r2['TargetGroupName'])
				tg_id.append(r3['Target']['Id'])
				port.append(r3['Target']['Port'])
				av_zone.append("all")
				hcp.append(r3['HealthCheckPort'])
				tg_state.append(r3['TargetHealth']['State'])
				ins_name.append(getinstancename(r3['Target']['Id']))
				if r3['TargetHealth']['State'] != 'healthy':
					reason.append(r3['TargetHealth']['Reason'])
					des.append(r3['TargetHealth']['Description'])	
				else:
					reason.append('NA')	
					des.append('NA')
				break
for n in response1['LoadBalancers']:
	response4 = client2.describe_load_balancer_attributes(LoadBalancerArn = n['LoadBalancerArn'])
	for n1 in response4['Attributes']:
		lb_name1.append(n['LoadBalancerName'])
		lb_arn.append(n['LoadBalancerArn'])
		if n1['Key'] == 'deletion_protection.enabled':
			dpe.append(n1['Value'])
		else:
			dpe.append('')
		if n1['Key'] == 'access_logs.s3.enabled':
			als3e.append(n1['Value'])
		else:
			als3e.append('')
		if n1['Key'] == 'access_logs.s3.bucket':
			als3b.append(n1['Value'])
		else:
			als3b.append('')
		if n1['Key'] == 'access_logs.s3.prefix':
			als3p.append(n1['Value'])
		else:
			als3p.append('')
		if n1['Key'] == 'idle_timeout.timeout_seconds':
			it.append(n1['Value'])
		else:
			it.append('')
		if n1['Key'] == 'routing.http2.enabled':
			h2.append(n1['Value'])
		else:
			h2.append('')


my_dict1['Load Balancer Name'] = lb_name
my_dict1['Type'] = lb_type
my_dict1['State'] = lb_state
my_dict1['VPC'] = vpc
my_dict1['Subnet ID 1'] = subnetid1
my_dict1['Subnet ID 2'] = subnetid2
my_dict1['Security Group'] = sg
my_dict1['Target Group'] = tg_name
my_dict1['IP'] = tg_id
my_dict1['Port'] = port
my_dict1['Target Availability Zone'] = av_zone
my_dict1['Health Check Port'] = hcp
my_dict1['Target Group Health State'] = tg_state
my_dict1['Reason'] = reason
my_dict1['Description'] = des
my_dict1['Instance Name'] = ins_name

my_dict2['Load Balancer Name'] = lb_name1
my_dict2['Load Balancer ARN'] = lb_arn
my_dict2['Deletion Protection Enabled'] = dpe
my_dict2['Access Logs S3 Enabled'] = als3e
my_dict2['Access Logs S3 Prefix'] = als3p
my_dict2['Access Logs S3 Bucket'] = als3b
my_dict2['HTTP/2 Routing Enabled'] = h2
my_dict2['Idle Timeout'] = it

df1 = pd.DataFrame(my_dict1, columns = ['Load Balancer Name', 'Type', 'State', 'VPC', 'Subnet ID 1', 'Subnet ID 2', 'Security Group', 'Target Group', 'IP', 'Port', 'Target Availability Zone', 'Health Check Port', 'Target Group Health State', 'Reason', 'Description', 'Instance Name'])
df2 = pd.DataFrame(my_dict2, columns = ['Load Balancer Name', 'Load Balancer ARN', 'Deletion Protection Enabled', 'Access Logs S3 Enabled', 'Access Logs S3 Prefix', 'Access Logs S3 Bucket', 'HTTP/2 Routing Enabled', 'Idle Timeout'])

writer = pd.ExcelWriter(r'ELB_Report.xlsx')

df1.to_excel (writer, sheet_name='Sheet1', index = False, header=True)
df2.to_excel (writer, sheet_name='Sheet2', index = False, header=True)

writer.save()

