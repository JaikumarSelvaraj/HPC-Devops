Resource

CIDR/ IP address

Component
Subnet
Gateway
Routing
NAT
Security Group
Ec2

Subnet

	Public -> Choose the CIDR Address (10.0.0.0/24)
	
	Private -> Choose the CIDR Address (10.0.1.0/24)
	
Internet Gateway

	Just Attach to VPC

Routing Table

	Public -> Attach Public Subnet "Assoication"

		Public - All Source Redirect to IGW
	
	Private -> Attach Private Subnet "Association"
		
		Private - Any source 0.0.0.0/0 to NAT Gateway
		
	NOTE: Every route table associate with one subnet.

Security Group

	Public SG (Inbound all traffic from TCP 0.0.0.0/0)
	
	Private SG (All Traffic coming from Public SecG group as Source)
		
Instance

	Public - Fronent Server -> Attach Public Subnet -> " Also Create Public IP from AWS console to access the machine "
	
	Private -> Backend Server -> Attach Private subnet ->
	
	Note: Since Even private Subent(10.0.0.0/24) connected to IGW it is called Public Subnet
	
Create NAT Gatway

	Associate with Public Subnet
	
	Assign Elastic IP 

AWS Console Role

	Create Role -> Attach a)Ec2 full access b)VPC full access.
--------------------------------------------------------------------------------------------------------------------------
	
What is little bit we have to sense - which is not straight forward
1)Route table
Pub RT -> IGW 
PVT RT -> NAT

2)Security Group
PUB SG -> Any traffic 0.0.0.0/0
PVG SG -> allowed only from PUB SG
if it is terraform
""add egress(Outbound allow all traffic)""

3)NAT
attach public subnet & Elastic IP

--------------------------------------------------------------------------------------------------------------------------

While Troubleshooting

1)We have to understand on which component issue is occur on the complex ecosystem. if doesn't know the ""workflow"" or logic
with little sense, we will lose the clarity. if know the component where is issue lies, we need to investigate close to the attributes/parameters.


2)ChatGPT we have to ask the question with little sense.
NOTE: With logic try to understand workflow in chatgpt, that will make our troubleshooting simpler.

----------------------------------------------------------------------------------------------------------------------------
	
	
One custom VPC (10.0.0.0/16)
One public subnet
One private subnet
Internet Gateway (IGW)
Public route table
Elastic IP (EIP)
NAT Gateway
Private route table
Two Security Groups
Two EC2 instances (public and private)

Same way we have to create order in Terraform Code.

----------------------------------------------------------------------------------------------------------------------------

Question 
1)without Public IP can we able to access Pub-server
Not possibe, we have to attach public ip.

1)VPC from where it will assign the IP address
From Subnet it will assign the IP address.

2)while trying to access from public server to privateserver, if connection is not success, what are things you will trying
a)Security group
b)routing table b.1)NAT Gateway
NAT Gateway -> Associate with Public subnet + Elastic IP
Reall issue found in Security grup (outbound rule is not added properly)

Note: Since this kind of complet env, In which component problem lies to identify that is tricky.

3)How Packet will travel

Route table redirect packet to the specific subnet

Security Group -> Act as firewall

----------------------------------------------------------------------------------------------------------------------------
