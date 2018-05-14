import boto3

client = boto3.client("ec2")

##Below lines will give us all the security groups associated with an ENI##

response = client.describe_network_interface_attribute(
    Attribute='groupSet',
    NetworkInterfaceId='eni',
)

##Below lines will look at the security GroupIds in the Security groups, check if the security group that you're going to put in is already in it's list and if it's not then it would add all of the security groups (including the new one) to the ENI. This is because Boto currently cannot add individual security groups, it can only replace. So this way, the old and the new security groups are added##

##This method is very safe as it will never delete an existing security group##

glist=response['Groups']

add_sg=list()

if any("security group" not in i['GroupId'] for i in glist):
    for i in glist:
       add_sg.append(i['GroupId'])        
    add_sg=add_sg+['security group']
    client.modify_network_interface_attribute(
        Groups= add_sg,
    NetworkInterfaceId='eni',
)

else :print "no change required"
