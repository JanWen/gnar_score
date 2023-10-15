variable iam_user_name {
  type        = string
}

resource "aws_iam_service_specific_credential" "power_rankings" {
  service_name = "codecommit.amazonaws.com"
  user_name    = var.iam_user_name
}

output "git_password" {
  sensitive = true
  value = aws_iam_service_specific_credential.power_rankings.service_password
}
output "git_user" {
  sensitive = true
  value = aws_iam_service_specific_credential.power_rankings.service_user_name
}