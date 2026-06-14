variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "real-state"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "raw_data_bucket_name" {
  type        = string
  description = "Scraped raw data bucket"
}
