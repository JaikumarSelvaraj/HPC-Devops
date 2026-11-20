Terraform -3

1)Terrafor Part -3 

1. Immutable Infrastructure – Mutable vs Immutable

2. Terraform Plan – Understanding Resource Changes and Replacement

3. Terraform State Management – terraform state list

4. Python Interview Preparation – List, Tuple 

5. Terraform Meta-Arguments – Introduction

6. Count Meta-Argument

7. For_each Meta-Argument – Map and Set

8. Count vs For_each – Differences and Use Cases

9. Terraform Resource Force Replacement

10. Terraform Lifecycle Meta-Argument

11. create_before_destroy – Resource Replacement

12. ignore_changes – Ignoring Manual Resource Changes

Imutable

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_vpc" "myvpc" { #Reference Name
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "My_Own_VPC" #console display name
  }
}

From 

	10.0.0.0/16 -> VPC

To 

	11.0.0.0/16 -> VPC

Terraform with Source Code -> Current State Validate

	it is IMUTABLE (doesn't modify but replace(Destroy and add))
	
	When #terraform plan 
	
	Notification "1 to add and, 0 to change, 1 to destory"

#terraform state list
List VPC

Python Question definitely they will ask
list,tuble (difference) decorators

Q: When should you use a List and when should you use a Tuple?

Answer:
- Use a List when you need to add, remove or modify elements.
- Use a Tuple when you want to store a fixed collection of elements that should not be modified.

Remember this simple concept:
- List = Mutable = Changeable
- Tuple = Immutable = Not changeable

HPC / DevOps Real-Time Example
Imagine you have 10 HPC compute nodes.
- Mutable: Update the existing compute nodes by installing new NVIDIA drivers or changing configuration.
- Immutable: Create a new golden image(new node) with updated NVIDIA drivers, launch new compute nodes using that image, validate them, and retire the old nodes.

Symbol	Meaning
~	Update in place (mutable-style change)
-/+	Destroy and recreate (replacement)
+	Create new resource
-	Destroy resource

Mutable:
~ resource "aws_instance" "web" {
    ~ instance_type = "t2.micro" -> "t2.small"
}

Immutable:
-/+ resource "aws_instance" "web" {
    ~ ami = "ami-old" -> "ami-new" # forces replacement
}
-------------------------------
					META Arguments 
					
Count and For Each
					
"Do ChatGPT and study - "meta argument count terraform code""

COUT and FOR each

UseCase: if we want to create 5 VPC.we are using count

   
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-xxxxxxxx"
  instance_type = "t2.micro"

  tags = {
    Name = "Web-Server-${count.index}" #web-server-0 web-server-1 webserver-2
  }
}   

3 - Resources will create

COUNT
x= s u m a i y 
   0 1 2 3 4 5 -> Index value
-------------------------------
				for_each

UseCase: if we want to create VPC with stable and Meantiful Naming conversion.

For_EACH - Use Case 
dev = my-dapp-bucket-jkumar
qa  = my-qapp-bucket-jkumar
uat = my-uapp-bucket-jkumar
NOTE: Bucket name should unique


# Create 3 S3 Buckets
resource "aws_s3_bucket" "mys3bucket" {

  # for_each Meta-Argument
  for_each = {
    dev = "my-dapp-bucket-111"
    qa  = "my-qapp-bucket-111"
    uat = "my-uapp-bucket-111"
  }

  bucket = "${each.key}-${each.value}"  # dev-my-dapp-bucket-111

  acl = "private"

  tags = {
    Environment = "MY-${each.key}-111"       # MY-dev-111
    bucketname  = "${each.key}-${each.value}" # dev-my-dapp-bucket-111
    eachvalue   = each.value                 # my-dapp-bucket-111
  }
}

			---------------------------------
			To Set(for_each)
			
for_each = toset(["TJack","TJames","Tmadhu","TDave"])  -> List[] (Square Bracket)

We cannot directly pass list to for_each that is reason, we have introduce toset.	

Why we have declare or convert into set

	-> Because, we need to remove index to assign into key value.
	
	-> for_each require stable unique key.

List =[10,20,30,40] -> Order

set = {10,20,30,40} -> Unorder

print(x) -> [10,20,30,40]
print(y) -> {40,10,30,10}

print(x[0]) -> 10
print(y[0]) -> we can't access like will get error -> Index Not support

list convert to set we have to use "" toset ""
-------------------------------		

resource "aws_instance" "web" {

  for_each = toset(["web1", "web2", "web3"])

  ami           = "ami-xxxxxxxx"
  instance_type = "t2.micro"

  tags = {
    Name = each.key
  }
}

		--------- InQuestion -------------------

for_each = toset(["web1", "web3"])

Terraform destroys only the web2 instance. The web1 and web3 instances retain their resource addresses.

UseCase : Count vs foreach : This is one major advantage of for_each over count, where removing an item in the middle of a list can cause index shifting and unnecessary resource replacement. (Important question during interview)

forcereplacement
-------------------------------
			LifeCycle
	
create_before_destroy = true 

Demonstration

1)First Create VPC with CIDR block 10.0.0.0/16

Change

1)Change CIDR block 11.0.0.0/16

Terraform apply (forcereplacement will happen)

resource "aws_vpc" "myvpc" { #Reference Name
  cidr_block       = "11.0.0.0/16"
  instance_tenancy = "default"

  lifecycle {
    create_before_destroy = true

  }
}

Sequence - create_before_destroy
1)Create
2)Destroy

-------------------------------
				ignore_changes
				
Demonstration

1)Create VPC with tag 

	Name = tag-vpc (Add it through console)
		
	new_name = change_tag (Add it manually from console)
	
After manually add tag it from console 	

	#terraform plan #get terraform notificaion about changes

Refer Screenshot

lifecycle {
	ignore_changes = [tags]
}

ignore_changes -> ignore changes to specified attribute during update planning.

Even change present, it will ignore

----------------------------------------------------------------------------------------------------------------------------