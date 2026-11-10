terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}
# --------------------------------
# 1. Get Default VPC and Subnet
# --------------------------------

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# --------------------------------
# 2. Security Group
# --------------------------------

resource "aws_security_group" "web_sg" {
  name        = "${var.project_name}-sg"
  description = "Allow HTTP access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow all TCP traffic"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --------------------------------
# 6. EC2 Instance
# --------------------------------

resource "aws_instance" "prometheus" {
  ami                         = data.aws_ami.amazon_linux.id 
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  key_name                    = "Nov_sing"
  tags = {
    Name = "${var.project_name}-Prometheus"
  }
}

  resource "aws_instance" "grafana" {
  ami                         = data.aws_ami.amazon_linux.id 
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  key_name                    = "Nov_sing"
  tags = {
    Name = "${var.project_name}-Grafana"
  }
  }