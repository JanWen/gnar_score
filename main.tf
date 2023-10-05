terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}


# TARGET s3 bucket
resource "aws_s3_bucket" "power_rankings_hackathon" {
  bucket = "power-rankings-hackathon"

  tags = {
    power-rankings-hackathon = "2023"
  }
}

resource "aws_s3_object" "object" {
  bucket = aws_s3_bucket.power_rankings_hackathon.bucket
  key    = "generate_rankings.py"
  source = "generate_rankings.py"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = filemd5("generate_rankings.py")
}


resource "aws_glue_job" "glue_job_power_rankings" {
  name     = "generate_rankings"
  role_arn = aws_iam_role.power_rankings_service_role.arn
  glue_version      = "1.0"
  max_capacity = 1
  command {
    name            = "pythonshell"
    python_version  = "3.9"
    script_location = "s3://${aws_s3_bucket.power_rankings_hackathon.bucket}/generate_rankings.py"
  }
}


###########################################################################


data "aws_iam_policy_document" "power_rankings_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "power_rankings_service_role" {
  name               = "AWSGlueServiceRole_power_rankings"
  assume_role_policy = data.aws_iam_policy_document.power_rankings_assume_role.json
}

data "aws_iam_policy" "aws_glue_service_role" {
  name = "AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "power_rankings_service_attach" {
  role       = aws_iam_role.power_rankings_service_role.name
  policy_arn = data.aws_iam_policy.aws_glue_service_role.arn
}