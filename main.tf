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

module "main" {
  source = "./terraform"
  iam_user_name = aws_iam_user.power_rankings.name
}


output "git_password" {
  sensitive = true
  value = "${module.main.git_password}"
}
output "git_user" {
  sensitive = true
  value = "${module.main.git_user}"
}


resource "aws_iam_user" "power_rankings" {
  name = "power_rankings"
  path = "/system/"

  tags = {
    power-rankings-hackathon = "2023"
  }
}

resource "aws_iam_user_login_profile" "power_rankings" {
  user    = aws_iam_user.power_rankings.name
}

output "password" {
  value = aws_iam_user_login_profile.power_rankings.password
}



resource "aws_iam_access_key" "power_rankings_key" {
  user = aws_iam_user.power_rankings.name
}

data "aws_iam_policy_document" "power_rankings_policy" {
  statement {
    effect    = "Allow"
    actions   = ["ec2:Describe*", "codecommit:*"]
    resources = ["*"]
  }
}

resource "aws_iam_user_policy" "power_rankings_user_policy" {
  name   = "power_rankings_user_policy"
  user   = aws_iam_user.power_rankings.name
  policy = data.aws_iam_policy_document.power_rankings_policy.json
}