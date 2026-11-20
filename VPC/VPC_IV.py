What is VPC in AWS?
Answer: VPC stands for Virtual Private Cloud. It is a logically isolated virtual network in AWS where we can launch AWS resources such as EC2, RDS, ECS, and EKS.

What is CIDR?
CIDR stands for Classless Inter-Domain Routing. It defines the IP address range of a network.

What is Subnet?
A subnet (short for subnetwork) is a logical subdivision of an IP network that splits a larger network into smaller, more manageable sections.


Public subnet	                    Private subnet
Route to Internet Gateway	        No direct Internet Gateway route
Can host internet-facing resources	Usually hosts internal resources
Can support public IP connectivity	Does not require public IP
Example: Web server	                Example: Application server, database

Q5. What is an Internet Gateway (IGW)?
An Internet Gateway is an that enables communication between resources in a VPC and the internet.

Q6. What is a NAT Gateway?
A NAT Gateway allows resources in a private subnet to initiate outbound internet connections without exposing those resources directly to inbound internet connections.
Example: A private EC2 instance downloads Linux packages from the internet through NAT Gateway.

Q7. What is a Route Table?
A route table contains routing rules that determine where network traffic is directed.
Destination       Target
10.0.0.0/16       Local
0.0.0.0/0         Internet Gateway

Q8. What is an Elastic IP?
An Elastic IP is a static public IPv4 address allocated to your AWS account.
It can be associated with supported AWS resources such as EC2 instances and public NAT Gateways.

Q9.What is an Availability Zone?
An Availability Zone is an isolated location within an AWS Region containing one or more data centers.

Q10.What is the difference between a VPC and a subnet?
- VPC: Your complete isolated virtual network.
- Subnet: A smaller IP network inside your VPC.

Q12. What is VPC Peering?
VPC Peering connects two VPCs so that resources can communicate using private IP addresses.

VPC-A (10.0.0.0/16)
        |
    VPC Peering
        |
VPC-B (10.1.0.0/16)

Q14. What is VPC Flow Logs?
VPC Flow Logs capture information about IP traffic going to and from network interfaces in a VPC, subnet, or network interface.
They are useful for troubleshooting network connectivity and security issues.

Q15. What is Transit Gateway?
AWS Transit Gateway is a network hub that connects multiple VPCs and on-premises networks.
Instead of creating multiple individual VPC peerings, we can use Transit Gateway for centralized connectivity.

Q16. What is the difference between VPC Peering and Transit Gateway?
VPC Peering	                        Transit Gateway
Point-to-point connectivity	        Hub-and-spoke connectivity
No transitive routing	            Supports transitive routing
Suitable for a smaller number of VPCs	Suitable for many VPCs

Q20. Can we have multiple CIDR blocks in one VPC?
Yes. A VPC supports one primary IPv4 CIDR block and additional secondary IPv4 CIDR blocks, subject to AWS limits.

Q25. What is the default VPC?
A default VPC is automatically created by AWS in each Region when applicable. It includes default subnets, an Internet Gateway, and associated routing configuration.

Q26. Can we attach multiple Internet Gateways to one VPC?
No. A VPC can have only one attached Internet Gateway at a time.