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
# 3. S3 Bucket
# --------------------------------

resource "aws_s3_bucket" "cdcp_bucket" {
  bucket_prefix = "${var.project_name}-"

  tags = {
    Name = "${var.project_name}-bucket"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.cdcp_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket                  = aws_s3_bucket.cdcp_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --------------------------------
# 4. Upload Initial Web Application
# --------------------------------

resource "aws_s3_object" "webapp" {
  bucket = aws_s3_bucket.cdcp_bucket.id
  key    = "webapp.zip"
  source = var.package_path

  etag = filemd5(var.package_path)
}

# --------------------------------
# 5. IAM Role for EC2
# --------------------------------

resource "aws_iam_role" "ec2_role" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "ec2.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "ec2_policy" {
  name = "${var.project_name}-ec2-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Action = [
        "s3:GetObject",
        "s3:GetObjectVersion"   
      ]

      Resource = [
        "${aws_s3_bucket.cdcp_bucket.arn}/*",
        "arn:aws:s3:::aws-codedeploy-ap-southeast-1/*",
        "${aws_s3_bucket.pipeline_artifacts.arn}/*"
      ]
    }]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-instance-profile"
  role = aws_iam_role.ec2_role.name
}

# --------------------------------
# 6. EC2 Instance
# --------------------------------

resource "aws_instance" "web" {
  ami                         = data.aws_ami.amazon_linux.id 
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  associate_public_ip_address = true
  key_name                    = "Nov_sing"
  user_data = <<-EOF
    #!/bin/bash
    set -e

    dnf install -y ruby wget httpd

    systemctl enable httpd
    systemctl start httpd

    cd /home/ec2-user

    wget https://aws-codedeploy-ap-southeast-1.s3.ap-southeast-1.amazonaws.com/latest/install

    chmod +x install

    ./install auto

    systemctl enable codedeploy-agent
    systemctl start codedeploy-agent
  EOF

  tags = {
    Name = "${var.project_name}-web-server"
  }

  depends_on = [
    aws_iam_role_policy.ec2_policy
  ]
}

# --------------------------------
# 7. IAM Role for CodeDeploy
# --------------------------------

resource "aws_iam_role" "codedeploy_role" {
  name = "${var.project_name}-codedeploy-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "codedeploy.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "codedeploy_policy" {
  role = aws_iam_role.codedeploy_role.name

  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole"
}

# --------------------------------
# 8. CodeDeploy Application
# --------------------------------

resource "aws_codedeploy_app" "app" {
  name             = "${var.project_name}-app"
  compute_platform = "Server"
}

# --------------------------------
# 9. CodeDeploy Deployment Group    
# --------------------------------

resource "aws_codedeploy_deployment_group" "group" {
  app_name              = aws_codedeploy_app.app.name
  deployment_group_name = "${var.project_name}-deployment-group"

  service_role_arn = aws_iam_role.codedeploy_role.arn

  deployment_config_name = "CodeDeployDefault.OneAtATime"

  ec2_tag_filter {
    key   = "Name"
    type  = "KEY_AND_VALUE"
    value = "${var.project_name}-web-server"
  }
    
  depends_on = [
    aws_instance.web,
    aws_iam_role_policy_attachment.codedeploy_policy
  ]
}



# --------------------------------
# 11. CodePipeline Artifact S3 Bucket
# --------------------------------

resource "aws_s3_bucket" "pipeline_artifacts" {
  bucket_prefix = "${var.project_name}-artifacts-"

  tags = {
    Name = "${var.project_name}-pipeline-artifacts"
  }
}

resource "aws_s3_bucket_public_access_block" "pipeline_artifacts_block" {
  bucket                  = aws_s3_bucket.pipeline_artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --------------------------------
# 12. IAM Role for CodePipeline
# --------------------------------

resource "aws_iam_role" "codepipeline_role" {
  name = "${var.project_name}-codepipeline-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "codepipeline.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })
}

# --------------------------------
# 13. CodePipeline IAM Policy
# --------------------------------

resource "aws_iam_role_policy" "codepipeline_policy" {

  name = "${var.project_name}-codepipeline-policy"
  role = aws_iam_role.codepipeline_role.id

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      # Source S3 Bucket Permissions
      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:GetBucketVersioning",
          "s3:GetBucketAcl",
          "s3:GetBucketLocation",
          "s3:GetObjectTagging",
          "s3:GetObjectVersionTagging"
        ]

        Resource = [
          aws_s3_bucket.cdcp_bucket.arn,
          "${aws_s3_bucket.cdcp_bucket.arn}/*"
        ]
      },

      # Pipeline Artifact Bucket Permissions
      {
        Effect = "Allow"

        Action = [
          "s3:GetBucketLocation",
          "s3:ListBucket",
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject",
          "s3:DeleteObject"
        ]

        Resource = [
          aws_s3_bucket.pipeline_artifacts.arn,
          "${aws_s3_bucket.pipeline_artifacts.arn}/*"
        ]
      },

      # CodeDeploy Permissions
      {
        Effect = "Allow"

        Action = [
          "codedeploy:CreateDeployment",
          "codedeploy:GetApplication",
          "codedeploy:GetApplicationRevision",
          "codedeploy:RegisterApplicationRevision",
          "codedeploy:GetDeployment",
          "codedeploy:GetDeploymentConfig",
          "codedeploy:GetDeploymentGroup",
          "codedeploy:ListApplications",
          "codedeploy:ListDeploymentGroups",
          "codedeploy:ListDeployments"
        ]

        Resource = "*"
      },

      # Allow CodePipeline to pass CodeDeploy service role
      {
        Effect = "Allow"

        Action = [
          "iam:PassRole"
        ]

        Resource = aws_iam_role.codedeploy_role.arn

        Condition = {
          StringEquals = {
            "iam:PassedToService" = "codedeploy.amazonaws.com"
          }
        }
      }
    ]
  })
}

# --------------------------------
# 14. AWS CodePipeline
# --------------------------------

resource "aws_codepipeline" "pipeline" {

  name = "${var.project_name}-pipeline"

  role_arn = aws_iam_role.codepipeline_role.arn

  # Pipeline execution setting
  execution_mode = "SUPERSEDED"

  # Artifact storage location
  artifact_store {
    location = aws_s3_bucket.pipeline_artifacts.bucket
    type     = "S3"
  }

  # --------------------------------
  # Stage 1: Source - Amazon S3
  # --------------------------------

  stage {
    name = "Source"

    action {

      name             = "S3_Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "S3"
      version          = "1"

      output_artifacts = ["SourceArtifact"]

      configuration = {

        S3Bucket = aws_s3_bucket.cdcp_bucket.id

        S3ObjectKey = "webapp.zip"

        PollForSourceChanges = "true"
      }
    }
  }

  # --------------------------------
  # Stage 2: Deploy - AWS CodeDeploy
  # --------------------------------

  stage {
    name = "Deploy"

    action {

      name             = "CodeDeploy_Application"
      category         = "Deploy"
      owner            = "AWS"
      provider         = "CodeDeploy"
      version          = "1"

      input_artifacts = ["SourceArtifact"]

      configuration = {

        ApplicationName = aws_codedeploy_app.app.name

        DeploymentGroupName = aws_codedeploy_deployment_group.group.deployment_group_name
      }
    }
  }

  depends_on = [
    aws_iam_role_policy.codepipeline_policy,
    aws_s3_object.webapp,
    aws_codedeploy_deployment_group.group
  ]

  tags = {
    Name = "${var.project_name}-pipeline"
  }
}
