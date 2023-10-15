# TARGET s3 bucket
resource "aws_s3_bucket" "power_rankings_hackathon" {
  bucket = "power-rankings-hackathon"

  tags = {
    power-rankings-hackathon = "2023"
  }
}
