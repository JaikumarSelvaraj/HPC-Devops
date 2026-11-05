Terraform

Docker CMD and Entrypoint difference

Copy Vs Add (Docker file)

Multistager Dockerfile


Subnet

	Public -> Choose the CIDR Address (10.0.0.0/24)
	
	Private -> Choose the CIDR Address (10.0.1.0/24)
	
Internet Gateway

	Just Attach to VPC
	
----------------------------------------------------------------------------------------------------------------------------

Terrarform.io -> Register -> Cloud Provider -> Choose Resource followed by one by one.

	-> VPC
	-> aws_vpc
	-> aws_subnet (add region)
		-> availability_zone = "ab-south-1a" #ad-hoc take it from Additonal resource
	-> aws_internet_gateway
	-> aws_route_table
	-> aws_route_table_association
	-> aws_
	
Note: 
1)Terraform .io filter we have to search
2)Withing code we have to change
a)resource name
Inside { env=value } By reading value we can easily identify which resource we have to change name.
Example
  env 			 = value
  allocation_id = aws_eip.example.id
  subnet_id     = aws_subnet.example.id
 1)eip = elastic ip
 2)subnet  = subnet By konwing value and env we can easliy understand understand structure of code.

----------------------------------------------------------------------------------------------------------------------------
 
Terraform Statefile -> Memory
terraform state list (will not stored on locally & )
When we are adding new resource -> it will track with existing and apply only new.

What are possiblity error
1)Region 
2)Role association

----------------------------------------------------------------------------------------------------------------------------

Terraform Code -> Make the robust System Env

AWS Console -> Change the configuration to test Env, After Changes, if we want back to the origin state

Terraform plan -> it will cross verify with realtime dashboard and what are the recent changes which needs to rollback
it will show, once we apply it will automcatilly restore to that stage

----------------------------------------------------------------------------------------------------------------------------