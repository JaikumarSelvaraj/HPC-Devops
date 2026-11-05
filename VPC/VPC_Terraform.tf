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
resource "aws_subnet" "pubsub" {
  vpc_id     = aws_vpc.myvpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-southeast-1a"

  tags = {
    Name = "My_Public_subnet"
  }
}
resource "aws_subnet" "prvsub" {
  vpc_id     = aws_vpc.myvpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-southeast-1b"

  tags = {
    Name = "My_Private_subnet"
  }
}
resource "aws_internet_gateway" "IGW" {
  vpc_id = aws_vpc.myvpc.id

  tags = {
    Name = "My_Internet_GW"
  }
}
resource "aws_route_table" "pubrt" {
  vpc_id = aws_vpc.myvpc.id

  route {
    cidr_block = "0.0.0.0/0" #anywhere
    gateway_id = aws_internet_gateway.IGW.id
  }

  tags = {
    Name = "Public_RT"
  }
}
resource "aws_route_table_association" "pubrt_ass" {
  subnet_id      = aws_subnet.pubsub.id
  route_table_id = aws_route_table.pubrt.id
}



resource "aws_eip" "eib" { }

resource "aws_nat_gateway" "NatGW" {
  allocation_id = aws_eip.eib.id
  subnet_id     = aws_subnet.pubsub.id

  tags = {
    Name = "NatGW"
  }
}

resource "aws_route_table" "prvrt" {
  vpc_id = aws_vpc.myvpc.id

  route {
    cidr_block = "0.0.0.0/0" 
    gateway_id = aws_nat_gateway.NatGW.id
  }

  tags = {
    Name = "Private_RT"
  }
}
resource "aws_route_table_association" "prvrt_ass" {
  subnet_id      = aws_subnet.prvsub.id
  route_table_id = aws_route_table.prvrt.id
}

resource "aws_security_group" "Public_SG" {
  name        = "Public_Security Group"
  description = "Allow all Incoming Traffic"
  vpc_id      = aws_vpc.myvpc.id

    ingress {
    description = "Allow All Traffic"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] #Allow ALL Incoming Traffic
  }

    egress {
    description = "Allow All Outgoing Traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Public Security Group"
  }
}

resource "aws_security_group" "Private_SG" {
  name        = "Private_Security Group"
  description = "Allow all Incoming Traffic"
  vpc_id      = aws_vpc.myvpc.id

    ingress {
    description = "Allow All Traffic"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    #cidr_blocks = ["10.0.1.0/24"]
    security_groups = [aws_security_group.Public_SG.id] #All Public Security group
    
  }

    egress {
    description = "Allow All Outgoing Traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Private Security Group"
  }
}

resource "aws_instance" "my-public-server" {
  ami                         = "ami-04def3298c5e62a7f"
  instance_type               = "t3.micro"
  availability_zone           = "ap-southeast-1a"
  associate_public_ip_address = "true"
  vpc_security_group_ids      = [aws_security_group.Public_SG.id]
  subnet_id                   = aws_subnet.pubsub.id
  key_name                    = "Nov_sing"

  tags = {
    Name = "Front-ent-Server"
  }
}

resource "aws_instance" "my-private-server" {
  ami                         = "ami-04def3298c5e62a7f"
  instance_type               = "t3.micro"
  availability_zone           = "ap-southeast-1b"
  associate_public_ip_address = "false"
  vpc_security_group_ids      = [aws_security_group.Private_SG.id]
  subnet_id                   = aws_subnet.prvsub.id
  key_name                    = "Nov_pem_sing"

  tags = {
    Name = "Backend-Server"
  }
}