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

variable "user_name" {
  type    = string
  description = "Name to identify developer"
}
