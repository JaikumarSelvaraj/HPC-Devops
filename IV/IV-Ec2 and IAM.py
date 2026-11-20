                        Ec2

What is the difference between Internet Gateway and NAT Gateway?
- Internet Gateway: Allows resources in public subnets to communicate with the internet when routing and public IP requirements are satisfied.
- NAT Gateway: Allows resources in private subnets to initiate outbound internet communication without accepting unsolicited inbound internet connections.

Can you increase the EBS volume size without stopping EC2?
Yes. For supported EBS volumes, you can modify the volume while the instance is running and then extend the partition and filesystem inside Linux.

What is an Elastic IP?
An Elastic IP is a static public IPv4 address that you can associate with an EC2 instance or network interface.

What is an Application Load Balancer (ALB)?
ALB distributes incoming HTTP/HTTPS traffic across multiple targets, such as EC2 instances

What is the difference between ALB and NLB?
ALB	                NLB
Layer 7 	        Layer 4
HTTP/HTTPS	        TCP/UDP/TLS
Content-based routing	Connection-based routing
Host/path routing	High-performance network traffic handling

What is an IAM Role for EC2?

An IAM role allows an EC2 instance to access AWS services securely without storing permanent AWS access keys on the instance.

Example: EC2 accessing S3 buckets.

---------------------------------------------------------------------------------------------------------------------------------------------
                        I AM Role

What is an IAM Role in AWS?                        
An IAM Role is an AWS "" identity "" that provides temporary security credentials to users, applications, or AWS services to access AWS resources.

    
    how to assign IAM role to user
    
        In AWS IAM, you cannot directly assign an IAM role to an IAM user. Instead, you attach IAM policies directly to the user (or add the user to a group), or you allow the user to assume an IAM role to temporarily take on its permissions
        
    how to assign IAM role to application
        Create the IAM Role
        Assign the Role to Your Application's Host
    Refer Google Docs - For More Informatoin

IAM User	                                                        IAM Role
Can have console password or access keys	                        Uses STS temporary credentials
Usually represents a person or application                          identity	Commonly used by AWS services and cross-account access
    
IAM Role	                Associated with	    Permission
EC2-S3-Role	                EC2	                S3 access
Lambda-DynamoDB-Role	    Lambda	            DynamoDB access
CodePipeline-Role	        CodePipeline    	Deployment access

Why do we use IAM Roles?
- Avoid hardcoding AWS access keys.
- Provide temporary credentials.
- Secure EC2 access to AWS services.
- Enable cross-account access.
- Allow AWS services to communicate securely.
        
    
What is a Trust Policy?
    A Trust Policy defines "" who is allowed to assume an IAM Role ""
    
    {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
    ]
    }

Followup Question what is STS
    provide temporary security credentails to users application and aws service. Security Tocken Service 


What is a Permission Policy?
        A Permission Policy defines what actions the role can perform on AWS resources.
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "s3:GetObject",
                "s3:ListBucket"
              ],
              "Resource": [
                "arn:aws:s3:::mybucket",
                "arn:aws:s3:::mybucket/*"
              ]
            }
          ]
        }

Component	        Meaning
Version	            Policy language version
Statement	        Permission rules
Effect	            Allow or Deny
Action	            AWS API operation
Resource        	AWS resource ARN



Trust Policy                        	Permission Policy
Defines who can assume the role	        Defines what the role can access
Controls sts:AssumeRole	                Controls service actions

What is AWS STS?
Security Token Service

Important STS operations:
- AssumeRole
- GetSessionToken

What is Cross-Account IAM Role
Cross-account IAM Role allows one AWS account to "" access resources in another AWS account "" without sharing permanent credentials.

AWS Account A
(Development)
      |
      | AssumeRole
      v
AWS Account B
(Production)
      |
      v
     S3 Bucket
     
Can one EC2 instance have multiple IAM Roles?
An EC2 instance can have only one IAM Role associated through its instance profile at a time.

However, that role can have permissions to access multiple AWS services, and it can assume other roles when authorized.

What is the Principle of Least Privilege?
Instead of giving full S3 access:
    "s3:*"
Provide only the required action:
    "s3:GetObject"

How do you allow EC2 in Account A to access an S3 bucket in Account B?

Answer:
1. Create an IAM Role in Account B.
2. Configure its trust policy to trust the required principal from Account A.
3. Attach an S3 permission policy to the role.
4. Allow the Account A identity to perform sts:AssumeRole.
5. Assume the role and access the S3 bucket.