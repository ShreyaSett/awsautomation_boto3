import boto3
import botocore
from datetime import datetime
from datetime import date
import time
import pytz
import pandas as pd
client = boto3.client('iam')
#Declare resources
resource_role = boto3.resource('iam')
resource_group = boto3.resource('iam')
resource_user = boto3.resource('iam')

date_today = date.today()
#tn = datetime.now()
#time_now = tn.strftime("%H:%M:%S")
#current = date_today + " " + time_now


#Store role inline policy in a dictionary and convert the same into dataframe
my_dict_1 = {}
rn1 = []
rin = []

for r1 in resource_role.roles.all():
    response1 = client.list_role_policies(RoleName = r1.name)
    if len(response1['PolicyNames'])!=0:
        for i1 in response1['PolicyNames']:
            rn1.append(r1.name)
            rin.append(i1)
    else:
        rn1.append(r1.name)
        rin.append('NA')
        
my_dict_1['Role Name'] = rn1
my_dict_1['Role Inline Policy'] = rin
df1 = pd.DataFrame(my_dict_1, columns = ['Role Name', 'Role Inline Policy'])

#Store role attached policy in a dictionary and convert the same into dataframe
my_dict_2 = {}
rn2 = []
rp = []
rpr = []
rpm = []
rpv = []
rpdes = []

for r2 in resource_role.roles.all():
    try:
        response2 = client.list_attached_role_policies(RoleName = r2.name)
        for i2 in response2['AttachedPolicies']:
            response3 = client.get_policy(PolicyArn = i2['PolicyArn'])
            response4 = client.get_policy_version(
                PolicyArn = i2['PolicyArn'],
                VersionId = response3['Policy']['DefaultVersionId']
            )
            if ((i2['PolicyArn']).split('::')[-1].split(':')[0]) == 'aws':
                rn2.append(r2.name)
                rp.append(i2['PolicyName'])
                rpr.append(i2['PolicyArn'])
                rpm.append('AWS Managed Policy')
                rpv.append(response3['Policy']['DefaultVersionId'])
                rpdes.append('NA')
            else:
                rn2.append(r2.name)
                rp.append(i2['PolicyName'])
                rpr.append(i2['PolicyArn'])
                rpm.append('Customer Managed Policy')
                rpv.append(response3['Policy']['DefaultVersionId'])
                rpdes.append(response4['PolicyVersion']['Document'])
    except botocore.exceptions.ClientError as err:
        rn2.append(r2.name)
        rp.append(err.response['Error']['Message'])
        rpr.append('NA')
        rpm.append('NA')
        rpv.append('NA')
        rpdes.append('NA')

my_dict_2['Role Names'] = rn2
my_dict_2['Role Attached Policy Name'] = rp
my_dict_2['Role Attached Policy ARN'] = rpr
my_dict_2['Role Attached Policy Management'] = rpm
my_dict_2['Role Attached Policy Default Version'] = rpv
my_dict_2['Role Attached Policy Document'] = rpdes
df2 = pd.DataFrame(my_dict_2, columns = ['Role Names', 'Role Attached Policy Name', 'Role Attached Policy ARN', 'Role Attached Policy Management', 'Role Attached Policy Default Version', 'Role Attached Policy Document'])

#Store user inline policy in a dictionary and convert the same into dataframe
my_dict_3 = {}
un1 = []
uin = []

for r3 in resource_user.users.all():
    response5 = client.list_user_policies(UserName = r3.name)
    if len(response5['PolicyNames'])!=0:
        for i3 in response5['PolicyNames']:
            un1.append(r3.name)
            uin.append(i3)
    else:
        un1.append(r3.name)
        uin.append('NA')

my_dict_3['User Name'] = un1
my_dict_3['User Inline Policy'] = uin
df3 = pd.DataFrame(my_dict_3, columns = ['User Name', 'User Inline Policy'])

#Store user attached policy in a dictionary and convert the same into dataframe
my_dict_4 = {}
un2 = []
up = []
upr = []
upm = []
upv = []
updes = []

for r4 in resource_user.users.all():
    try:
        response6 = client.list_attached_user_policies(UserName = r4.name)
        for i4 in response6['AttachedPolicies']:
            response7 = client.get_policy(PolicyArn = i4['PolicyArn'])
            response8 = client.get_policy_version(
                PolicyArn = i4['PolicyArn'],
                VersionId = response7['Policy']['DefaultVersionId']
            )
            if ((i4['PolicyArn']).split('::')[-1].split(':')[0]) == 'aws':
                un2.append(r4.name)
                up.append(i4['PolicyName'])
                upr.append(i4['PolicyArn'])
                upm.append('AWS Managed Policy')
                upv.append(response7['Policy']['DefaultVersionId'])
                updes.append('NA')
            else:
                un2.append(r4.name)
                up.append(i4['PolicyName'])
                upr.append(i4['PolicyArn'])
                upm.append('Customer Managed Policy')
                upv.append(response7['Policy']['DefaultVersionId'])
                updes.append(response8['PolicyVersion']['Document'])
    except botocore.exceptions.ClientError as err:
        un2.append(r4.name)
        up.append(err.response['Error']['Message'])
        upr.append('NA')
        upm.append('NA')
        upv.append('NA')
        updes.append('NA')

my_dict_4['User Names'] = un2
my_dict_4['User Attached Policy Name'] = up
my_dict_4['User Attached Policy ARN'] = upr
my_dict_4['User Attached Policy Management'] = upm
my_dict_4['User Attached Policy Default Version'] = upv
my_dict_4['User Attached Policy Document'] = updes
df4 = pd.DataFrame(my_dict_4, columns = ['User Names', 'User Attached Policy Name', 'User Attached Policy ARN', 'User Attached Policy Management', 'User Attached Policy Default Version', 'User Attached Policy Document'])

#Store user inherited group inline policy in a dictionary and convert the same into dataframe
my_dict_5 = {}
ug1 = []
gn1 = []
gin = []

for r5 in resource_user.users.all():
    response9 = client.list_groups_for_user(UserName = r5.name)
    for i5 in response9['Groups']:
        response10 = client.list_group_policies(GroupName = i5['GroupName'])
        if len(response10['PolicyNames'])!=0:
            for i6 in response10['PolicyNames']:
                ug1.append(r5.name)
                gn1.append(i5['GroupName'])
                gin.append(i6)
        else:
            ug1.append(r5.name)
            gn1.append(i5['GroupName'])
            gin.append('NA')

my_dict_5['User Names'] = ug1
my_dict_5['Group Names'] = gn1
my_dict_5['User Inherited Group Inline Policy'] = gin
df5 = pd.DataFrame(my_dict_5, columns = ['User Names', 'Group Names', 'User Inherited Group Inline Policy'])


#Store user inherited group attached policy in a dictionary and convert the same into dataframe
my_dict_6 = {}
ug2 = []
gn2 = []
gp = []
gpr = []
gpm = []
gpv = []
gpdes = []

for r6 in resource_user.users.all():
    response11 = client.list_groups_for_user(UserName = r6.name)
    for i7 in response11['Groups']:
        response12 = client.list_attached_group_policies(GroupName = i7['GroupName']) 
        for i8 in response12['AttachedPolicies']:
            response13 = client.get_policy(PolicyArn = i8['PolicyArn'])
            response14 = client.get_policy_version(
                PolicyArn = i8['PolicyArn'],
                VersionId = response13['Policy']['DefaultVersionId']
            )
            if ((i8['PolicyArn']).split('::')[-1].split(':')[0]) == 'aws':
                ug2.append(r6.name)
                gn2.append(i7['GroupName'])
                gp.append(i8['PolicyName'])
                gpr.append(i8['PolicyArn'])
                gpm.append('AWS Managed Policy')
                gpv.append(response13['Policy']['DefaultVersionId'])
                gpdes.append('NA')
            else:
                ug2.append(r6.name)
                gn2.append(i7['GroupName'])
                gp.append(i8['PolicyName'])
                gpr.append(i8['PolicyArn'])
                gpm.append('Customer Managed Policy')
                gpv.append(response13['Policy']['DefaultVersionId'])
                gpdes.append(response14['PolicyVersion']['Document'])
        
my_dict_6['Users'] = ug2
my_dict_6['Groups'] = gn2
my_dict_6['Group Attached Policy Name'] = gp
my_dict_6['Group Attached Policy ARN'] = gpr
my_dict_6['Group Attached Policy Management'] = gpm
my_dict_6['Group Attached Policy Default Version'] = gpv
my_dict_6['Group Attached Policy Document'] = gpdes
df6 = pd.DataFrame(my_dict_6, columns = ['Users', 'Groups', 'Group Attached Policy Name', 'Group Attached Policy ARN', 'Group Attached Policy Management', 'Group Attached Policy Default Version', 'Group Attached Policy Document'])


writer = pd.ExcelWriter(fr'IAMUSER&ROLEPOLICYREPORT_{date_today}.xlsx', datetime_format = 'dd-mm-yyyy')

df1.to_excel (writer, sheet_name='Role Inline Policies', index = False, header=True)
df2.to_excel (writer, sheet_name='Role Attached Policies', index = False, header=True)
df3.to_excel (writer, sheet_name='User Inline Policies', index = False, header=True)
df4.to_excel (writer, sheet_name='User Direct Attached Policies', index = False, header=True)
df5.to_excel (writer, sheet_name='User Inherited Group Inline Policies', index = False, header=True)
df6.to_excel (writer, sheet_name='User Inherited Group Attached Policies', index = False, header=True)

writer.save()
